# release-clean.ps1 — Skill 发布前清洗工具 (Windows PowerShell 5.1+)
#
# 用途：删除开发期产物、剥离版本号与升级纪要，让发布包只保留运行必需内容。
# 清单见 flows/release-clean.md，本脚本是该清单的可执行版本。
#
# 用法：
#   .\release-clean.ps1 -Path <skill目录> [-DryRun] [-KeepMemory]
#
# 安全红线：
#   1. 目标必须是已存在的目录，且直接包含 SKILL.md
#   2. 只删除清单内列出的目录/文件，不做目录树遍历删除
#   3. .dev-memory.md 归档而非删除（除非 -KeepMemory）
#   4. 默认 DryRun，显式 -Apply 才实际改动

[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)][string]$Path,
  [switch]$Apply,
  [switch]$KeepMemory
)

$ErrorActionPreference = 'Stop'

function Die($msg)  { Write-Host "错误：$msg" -ForegroundColor Red; exit 1 }
function Ok($msg)   { Write-Host $msg -ForegroundColor Green }
function Info($msg) { Write-Host $msg }

$root = (Resolve-Path -LiteralPath $Path).Path
if (-not (Test-Path -LiteralPath (Join-Path $root 'SKILL.md'))) {
  Die "目标目录缺少 SKILL.md，不是 skill 目录：$root"
}

$dryRun = -not $Apply

# ---- 1. 删除开发期目录 ----
Info "【1/4】删除开发期目录"
$devDirs = @('.research', 'artifacts', '__pycache__', '.pytest_cache', 'node_modules', 'dist', 'build')
foreach ($d in $devDirs) {
  $hits = Get-ChildItem -LiteralPath $root -Recurse -Directory -Force -Filter $d -ErrorAction SilentlyContinue
  foreach ($h in $hits) {
    if ($dryRun) { Info "  [dry-run] 将删除目录 $($h.FullName)" }
    else { Remove-Item -LiteralPath $h.FullName -Recurse -Force; Ok "  已删除目录 $($h.FullName)" }
  }
}

# ---- 2. 删除开发期文件 ----
Info "【2/4】删除开发期文件"
$devFiles = @('index.html', 'CHANGELOG.md', 'CHANGELOG', 'HISTORY.md', 'VERSION')
foreach ($f in $devFiles) {
  $hits = Get-ChildItem -LiteralPath $root -Recurse -Depth 1 -File -Force -Filter $f -ErrorAction SilentlyContinue
  foreach ($h in $hits) {
    if ($dryRun) { Info "  [dry-run] 将删除文件 $($h.FullName)" }
    else { Remove-Item -LiteralPath $h.FullName -Force; Ok "  已删除文件 $($h.FullName)" }
  }
}

$residue = Get-ChildItem -LiteralPath $root -Recurse -Depth 2 -File -Force -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -like '*.bak' -or $_.Name -like '*.bak-*' -or $_.Name.EndsWith('~') }
foreach ($r in $residue) {
  if ($dryRun) { Info "  [dry-run] 将删除残留 $($r.FullName)" }
  else { Remove-Item -LiteralPath $r.FullName -Force; Ok "  已删除残留 $($r.FullName)" }
}

# ---- 3. 归档 .dev-memory.md ----
Info "【3/4】处理 .dev-memory.md"
$mem = Get-ChildItem -LiteralPath $root -Recurse -Depth 1 -File -Force -Filter '.dev-memory.md' -ErrorAction SilentlyContinue |
  Select-Object -First 1
if ($mem) {
  if ($KeepMemory) {
    Info "  保留（原地）：$($mem.FullName)"
  } else {
    $skillName = Split-Path $root -Leaf
    $archiveDir = Join-Path (Split-Path $root -Parent) '.dev-memory'
    $archive = Join-Path $archiveDir "$skillName.md"
    if ($dryRun) { Info "  [dry-run] 将归档 $($mem.FullName) → $archive" }
    else {
      New-Item -ItemType Directory -Path $archiveDir -Force | Out-Null
      Move-Item -LiteralPath $mem.FullName -Destination $archive -Force
      Ok "  已归档到 $archive"
    }
  }
} else {
  Info "  无 .dev-memory.md"
}

# ---- 4. 剥离版本号 ----
Info "【4/4】剥离版本号与升级纪要"
# 教学/说明文档自身的版本字眼是示例，不剥离
$skipVersions = @('release-clean.md', 'dev-memory-guide.md', 'README.md')
$mds = Get-ChildItem -LiteralPath $root -Recurse -Depth 2 -File -Force -Filter '*.md' -ErrorAction SilentlyContinue |
  Where-Object { $skipVersions -notcontains $_.Name }
foreach ($md in $mds) {
  $text = Get-Content -LiteralPath $md.FullName -Raw -Encoding UTF8
  if ($null -eq $text) { continue }
  $orig = $text
  $changed = @()

  # frontmatter version 字段
  if ($text -match '(?m)^version:\s*') {
    $text = [regex]::Replace($text, '(?m)^version:\s*\r?\n', '')
    $changed += 'version 字段'
  }
  # 标题/行内版本后缀
  if ($text -match '（v\d+\.\d+(\.\d+)?\s*新增）') {
    $text = [regex]::Replace($text, '（v\d+\.\d+(\.\d+)?\s*新增）', '')
    $changed += '版本后缀'
  }
  # 文件头注
  if ($text -match '(?m)^>\s*v\d+\.\d+\s*新增') {
    $text = [regex]::Replace($text, '(?m)^(>\s*)v\d+\.\d+\s*新增\s*', '$1')
    $changed += '头注版本'
  }

  if ($text -ne $orig) {
    if ($dryRun) { Info "  [dry-run] 将剥离 $($changed -join '、')：$($md.FullName)" }
    else {
      Set-Content -LiteralPath $md.FullName -Value $text -Encoding UTF8 -NoNewline
      Ok "  已剥离 $($changed -join '、')：$($md.FullName)"
    }
  }
}

if ($Apply) { Ok ""; Ok "清洗完成。" }
else { Info ""; Info "以上为演练，未实际改动。确认无误后加 -Apply 执行。" }