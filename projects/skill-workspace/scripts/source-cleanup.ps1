# source-cleanup.ps1 — Skill 源码工作区安全清理工具 (Windows PowerShell 5.1+)
#
# 用途：清理 skill-workspace 在「搜索 / 开发 / 审查 / 合并」流程中 git clone 下来的临时源码。
# 设计：两段式回收 —— 先 stage（移入 .trash，可恢复），再 purge（真正删除，默认 7 天冷静期）。
#
# 用法：
#   .\source-cleanup.ps1 list [-Root DIR]
#   .\source-cleanup.ps1 stage <name|all> [-Root DIR] [-Skill NAME] [-Yes]
#   .\source-cleanup.ps1 release <name> [-Root DIR]        # 标记 status=releasable
#   .\source-cleanup.ps1 restore <staged-name> [-Root DIR]
#   .\source-cleanup.ps1 purge [-Root DIR] [-OlderThan N] [-Yes] [-DryRun]
#   .\source-cleanup.ps1 auto [-Root DIR] [-DryRun]
#
# 安全红线（脚本强制，不可绕过）：
#   1. 只允许操作 Root 的直接子目录，拒绝 ".."、绝对路径、符号链接逃逸
#   2. 目标必须含标记文件 .skill-workspace-source 且 marker 匹配，否则拒绝
#   3. 禁止删除 Root 自身、.trash 之外的任何路径
#   4. purge 默认 DryRun，必须显式 -Yes 才真删

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateSet('list', 'stage', 'release', 'restore', 'purge', 'auto')]
    [string]$Command = 'list',

    [Parameter(Position = 1)]
    [string]$Target,

    [string]$Root = '.cache/sources',
    [string]$Skill,
    [int]$OlderThan = 7,
    [switch]$Yes,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$MARKER_FILE  = '.skill-workspace-source'
$MARKER_KEY   = 'skill-workspace-source'
$TRASH_DIR    = '.trash'

function Write-Fail([string]$msg) { Write-Host "错误：$msg" -ForegroundColor Red; exit 1 }
function Write-WarnMsg([string]$msg) { Write-Host "警告：$msg" -ForegroundColor Yellow }
function Write-Ok([string]$msg) { Write-Host $msg -ForegroundColor Green }

# ---------- 安全工具 ----------

function Assert-SafeName([string]$name) {
    if ([string]::IsNullOrWhiteSpace($name)) { Write-Fail '目标名为空' }
    if ($name -eq '.' -or $name -eq '..') { Write-Fail "非法目标名: $name" }
    if ($name.Contains('/') -or $name.Contains('\')) { Write-Fail "目标名不允许包含路径分隔符: $name" }
    if ($name.StartsWith('.')) { Write-Fail "拒绝操作隐藏目录: $name" }
}

function Resolve-UnderRoot([string]$root, [string]$name) {
    if (-not (Test-Path -LiteralPath $root -PathType Container)) {
        Write-Fail "根目录不存在: $root（先用 list 确认，或传 -Root）"
    }
    $itemPath = Join-Path $root $name
    if (-not (Test-Path -LiteralPath $itemPath)) { Write-Fail "目标不存在: $itemPath" }

    $rootReal   = (Resolve-Path -LiteralPath $root).ProviderPath.TrimEnd('\')
    $targetReal = (Resolve-Path -LiteralPath $itemPath).ProviderPath.TrimEnd('\')

    if ($targetReal -eq $rootReal) { Write-Fail '拒绝操作根目录自身' }
    if (-not $targetReal.StartsWith($rootReal + '\', [StringComparison]::OrdinalIgnoreCase)) {
        Write-Fail "安全拒绝：目标真实路径逃逸出根目录 → $targetReal"
    }
    return $targetReal
}

function Require-Marker([string]$dir) {
    $marker = Join-Path $dir $MARKER_FILE
    if (-not (Test-Path -LiteralPath $marker -PathType Leaf)) {
        Write-Fail "安全拒绝：目标缺少标记文件 $MARKER_FILE，不是 skill-workspace 创建的源码工作区 → $dir"
    }
    $content = Get-Content -LiteralPath $marker -Raw -ErrorAction SilentlyContinue
    if ([string]::IsNullOrWhiteSpace($content) -or $content -notmatch "marker=$MARKER_KEY") {
        Write-Fail "安全拒绝：标记文件内容不匹配（marker=$MARKER_KEY）→ $dir"
    }
}

function Read-Field([string]$dir, [string]$key) {
    $marker = Join-Path $dir $MARKER_FILE
    if (-not (Test-Path -LiteralPath $marker -PathType Leaf)) { return '' }
    foreach ($line in (Get-Content -LiteralPath $marker)) {
        if ($line -match "^\s*$key\s*=\s*(.*)$") { return $Matches[1].Trim() }
    }
    return ''
}

function Set-Field([string]$dir, [string]$key, [string]$value) {
    $marker = Join-Path $dir $MARKER_FILE
    $lines = @()
    if (Test-Path -LiteralPath $marker -PathType Leaf) { $lines = @(Get-Content -LiteralPath $marker) }
    $replaced = $false
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match "^\s*$key\s*=") { $lines[$i] = "$key=$value"; $replaced = $true }
    }
    if (-not $replaced) { $lines += "$key=$value" }
    Set-Content -LiteralPath $marker -Value $lines -Encoding UTF8
}

function Get-DirSizeMB([string]$dir) {
    try {
        $bytes = (Get-ChildItem -LiteralPath $dir -Recurse -File -Force -ErrorAction SilentlyContinue |
            Measure-Object -Property Length -Sum).Sum
        if ($null -eq $bytes) { $bytes = 0 }
        return [math]::Round($bytes / 1MB, 1)
    } catch { return 0 }
}

function Get-Workspaces([string]$root) {
    if (-not (Test-Path -LiteralPath $root -PathType Container)) { return @() }
    Get-ChildItem -LiteralPath $root -Directory -Force |
        Where-Object { $_.Name -ne $TRASH_DIR }
}

# ---------- 命令实现 ----------

function Invoke-List {
    if (-not (Test-Path -LiteralPath $Root -PathType Container)) {
        Write-Host "源码根目录不存在：$Root（尚无 git 下载的源码，无需清理）"
        return
    }

    Write-Host ("{0,-42} {1,-10} {2,-9} {3,-16} {4}" -f '工作区', '状态', '占用', '关联', '来源')
    Write-Host ('-' * 100)

    $managed = 0; $unmanaged = 0; $totalMB = 0.0; $unmanagedMB = 0.0

    foreach ($dir in (Get-Workspaces $Root)) {
        $marker = Join-Path $dir.FullName $MARKER_FILE
        if (-not (Test-Path -LiteralPath $marker -PathType Leaf)) {
            $unmanaged++
            $unmanagedMB += (Get-DirSizeMB $dir.FullName)
            Write-Host ("{0,-42} {1}" -f $dir.Name, '(无标记 · 非本工具创建 · 不会自动清理)') -ForegroundColor DarkGray
            continue
        }
        $managed++
        if ($Skill) {
            $sn = Read-Field $dir.FullName 'skill_name'
            if ($sn -ne $Skill) { continue }
        }
        $status = Read-Field $dir.FullName 'status'; if (-not $status) { $status = 'in-use' }
        $skill  = Read-Field $dir.FullName 'skill_name'; if (-not $skill) { $skill = '-' }
        $url    = Read-Field $dir.FullName 'source_url'; if (-not $url) { $url = '-' }
        $sizeMB = Get-DirSizeMB $dir.FullName
        $totalMB += $sizeMB
        Write-Host ("{0,-42} {1,-10} {2,-9} {3,-16} {4}" -f $dir.Name, $status, "$sizeMB MB", $skill, $url)
    }

    Write-Host ('-' * 100)
    Write-Host "受管工作区：$managed 个，合计 $([math]::Round($totalMB,1)) MB"
    if ($unmanaged -gt 0) {
        Write-WarnMsg "发现 $unmanaged 个无标记目录（约 $([math]::Round($unmanagedMB,1)) MB），非本工具创建，已跳过不动"
    }

    $trash = Join-Path $Root $TRASH_DIR
    if (Test-Path -LiteralPath $trash -PathType Container) {
        $staged = @(Get-ChildItem -LiteralPath $trash -Directory -Force -ErrorAction SilentlyContinue)
        Write-Host "回收暂存区：$($staged.Count) 个，占用 $([math]::Round((Get-DirSizeMB $trash),1)) MB（可用 purge 真正释放）"
    }
}

function Invoke-StageOne([string]$name) {
    Assert-SafeName $name
    $dir = Resolve-UnderRoot $Root $name
    Require-Marker $dir

    $status = Read-Field $dir 'status'; if (-not $status) { $status = 'in-use' }

    if ($status -eq 'in-use' -and -not $Yes) {
        Write-WarnMsg "工作区状态为 in-use（可能仍在使用）：$name"
        $ans = Read-Host '确认移入回收暂存区？[y/N]'
        if ($ans -notmatch '^[Yy]') { Write-Host "已跳过：$name"; return $false }
    }

    $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $trash = Join-Path $Root $TRASH_DIR
    $dest  = Join-Path $trash "$name-$stamp"

    if (-not (Test-Path -LiteralPath $trash)) {
        New-Item -ItemType Directory -Path $trash -Force | Out-Null
    }

    if ($DryRun) {
        Write-Host "[dry-run] 将移动：$dir → $dest"
        return $true
    }

    Set-Field $dir 'status' 'staged'
    Set-Field $dir 'staged_at' (Get-Date -Format 'yyyy-MM-ddTHH:mm:sszzz')
    Set-Field $dir 'staged_from' $name

    try {
        Move-Item -LiteralPath $dir -Destination $dest -Force -ErrorAction Stop
        Write-Ok "已移入回收暂存区：$name → $dest（可用 restore 恢复）"
        return $true
    } catch {
        Set-Field $dir 'status' $status
        Write-Fail "移动失败：$name（可能是文件被占用，关闭相关程序后重试）"
    }
}

function Invoke-Stage {
    if (-not (Test-Path -LiteralPath $Root -PathType Container)) { Write-Fail "源码根目录不存在：$Root" }

    if ([string]::IsNullOrWhiteSpace($Target) -or $Target -eq 'all') {
        $count = 0
        foreach ($dir in (Get-Workspaces $Root)) {
            $marker = Join-Path $dir.FullName $MARKER_FILE
            if (-not (Test-Path -LiteralPath $marker -PathType Leaf)) { continue }
            if ($Skill) {
                $sn = Read-Field $dir.FullName 'skill_name'
                if ($sn -ne $Skill) { continue }
            }
            $status = Read-Field $dir.FullName 'status'; if (-not $status) { $status = 'in-use' }
            if ($status -eq 'releasable' -or $Yes) {
                if (Invoke-StageOne $dir.Name) { $count++ }
            } else {
                Write-Host "跳过（状态 $status）：$($dir.Name)"
            }
        }
        Write-Host "完成：共移入 $count 个"
    } else {
        Invoke-StageOne $Target | Out-Null
    }
}

function Invoke-Release {
    if ([string]::IsNullOrWhiteSpace($Target)) { Write-Fail '用法：release <name>' }
    Assert-SafeName $Target
    $dir = Resolve-UnderRoot $Root $Target
    Require-Marker $dir

    if ($DryRun) { Write-Host "[dry-run] 将标记 releasable：$Target"; return }

    Set-Field $dir 'status' 'releasable'
    Set-Field $dir 'releasable_at' (Get-Date -Format 'yyyy-MM-ddTHH:mm:sszzz')
    Write-Ok "已标记为可释放：$Target（下次 auto 或 stage all 会被回收）"
}

function Invoke-Restore {
    if ([string]::IsNullOrWhiteSpace($Target)) {
        Write-Fail '用法：restore <staged-name>（名称见 .trash 目录，形如 xxx-20260904-221000）'
    }
    Assert-SafeName $Target
    $trash = Join-Path $Root $TRASH_DIR
    $src = Join-Path $trash $Target
    if (-not (Test-Path -LiteralPath $src -PathType Container)) { Write-Fail "暂存区中不存在：$src" }

    $orig = Read-Field $src 'staged_from'
    if (-not $orig) { $orig = $Target -replace '-\d{8}-\d{6}$', '' }
    Assert-SafeName $orig

    $dest = Join-Path $Root $orig
    if (Test-Path -LiteralPath $dest) { Write-Fail "目标位置已存在同名目录：$dest（先处理后再恢复）" }

    if ($DryRun) { Write-Host "[dry-run] 将恢复：$src → $dest"; return }

    try {
        Move-Item -LiteralPath $src -Destination $dest -Force -ErrorAction Stop
        Set-Field $dest 'status' 'in-use'
        Write-Ok "已恢复：$dest（状态重置为 in-use）"
    } catch { Write-Fail "恢复失败：$Target" }
}

function Invoke-Purge {
    $trash = Join-Path $Root $TRASH_DIR
    if (-not (Test-Path -LiteralPath $trash -PathType Container)) {
        Write-Host '暂存区为空，无需清理'
        return
    }

    $cutoff = (Get-Date).AddDays(-1 * $OlderThan)
    $entries = @(Get-ChildItem -LiteralPath $trash -Directory -Force -ErrorAction SilentlyContinue |
        Where-Object { $_.LastWriteTime -lt $cutoff })

    if ($entries.Count -eq 0) {
        Write-Host "暂存区中没有超过 $OlderThan 天的条目（冷静期未到，保留以防误删）"
        return
    }

    Write-Host "以下条目将被永久删除（已在暂存区超过 $OlderThan 天）："
    $totalMB = 0.0
    foreach ($e in $entries) {
        $mb = Get-DirSizeMB $e.FullName
        $totalMB += $mb
        Write-Host ("  {0}  {1} MB" -f $e.Name, $mb)
    }
    Write-Host "合计释放：约 $([math]::Round($totalMB,1)) MB"

    if ($DryRun) { Write-Host '[dry-run] 未执行删除。确认后加 -Yes'; return }

    if (-not $Yes) {
        $ans = Read-Host '永久删除以上内容？此操作不可恢复。[y/N]'
        if ($ans -notmatch '^[Yy]') { Write-Host '已取消'; return }
    }

    $trashReal = (Resolve-Path -LiteralPath $trash).ProviderPath.TrimEnd('\')
    $freed = 0.0; $count = 0
    foreach ($e in $entries) {
        $real = (Resolve-Path -LiteralPath $e.FullName).ProviderPath.TrimEnd('\')
        if (-not $real.StartsWith($trashReal + '\', [StringComparison]::OrdinalIgnoreCase)) {
            Write-WarnMsg "跳过（路径校验未通过）：$($e.Name)"
            continue
        }
        $mb = Get-DirSizeMB $e.FullName
        try {
            Remove-Item -LiteralPath $e.FullName -Recurse -Force -ErrorAction Stop
            $count++
            $freed += $mb
        } catch {
            Write-WarnMsg "删除失败（可能被占用）：$($e.Name)"
        }
    }
    Write-Ok "已永久删除 $count 个条目，释放约 $([math]::Round($freed,1)) MB"
}

function Invoke-Auto {
    if (-not (Test-Path -LiteralPath $Root -PathType Container)) {
        Write-Host "源码根目录不存在：$Root（无需清理）"
        return
    }
    Write-Host '自动释放：扫描 status=releasable 的源码工作区…'
    $count = 0; $skipped = 0
    foreach ($dir in (Get-Workspaces $Root)) {
        $marker = Join-Path $dir.FullName $MARKER_FILE
        if (-not (Test-Path -LiteralPath $marker -PathType Leaf)) { continue }
        $status = Read-Field $dir.FullName 'status'; if (-not $status) { $status = 'in-use' }
        if ($status -eq 'releasable') {
            if (Invoke-StageOne $dir.Name) { $count++ }
        } else { $skipped++ }
    }
    Write-Host "自动释放完成：移入暂存 $count 个，保留 $skipped 个（仍标记为 in-use）"
    if ($count -gt 0) {
        Write-Host "提示：这些内容仍在 .trash 中，$OlderThan 天后 purge 才会真正释放磁盘；如需立即回收请执行 purge -OlderThan 0 -Yes"
    }
}

# ---------- 入口 ----------

if ($Root -eq '.' -or $Root -eq '/' -or $Root -eq $HOME) { Write-Fail "拒绝使用危险根目录: $Root" }
if ($OlderThan -lt 0) { Write-Fail '-OlderThan 必须是非负整数' }

switch ($Command) {
    'list'    { Invoke-List }
    'stage'   { Invoke-Stage }
    'release' { Invoke-Release }
    'restore' { Invoke-Restore }
    'purge'   { Invoke-Purge }
    'auto'    { Invoke-Auto }
}
