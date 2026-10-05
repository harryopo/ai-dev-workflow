#!/usr/bin/env node
/* 结构层门禁：把 slop_scan 的纯正则做不到的两件事变成退出码 —— CSS 真解析（stylelint）
   与标记真校验（html-validate）。需要 .sfd-tools 里的 npm 包（项目本地安装，不入版本库）。
   两份规则表都是数据：rules/stylelint.config.json 只管"颜色/字体必须走 var()"、拼错属性、
   无效 hex、未知函数、重复声明；间距与裸 hex 的 token 纪律仍由 slop_scan 负责，不重复判。
   strict-value 要求整个值都是变量，所以 border/outline 这类"宽度+样式+颜色"混写的简写不纳入
   （1px solid var(--x) 会被误判），它们的裸 hex 由 slop_scan 的 bare-hex-outside-root 兜住。
   rules/html-validate.config.json 用 recommended 组加 WCAG 项，关掉排版风格类规则，
   避免把 skill 变成格式警察。豁免用两家原生注释：stylelint-disable-* / html-validate-disable-*,
   写理由由人工保证，本脚本不另设豁免语法。

   node scripts/structure_lint.mjs <文件|目录> [...] [--json] [--strict] [--tools <目录>]
                                    [--only css|html]
   退出码：0 干净 / 1 有硬判定 / 2 调用错误、没扫到东西、或结构层没装。
   "结构层没装"必须报错退出，不允许静默跳过变成绿灯。
*/

import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SKILL = path.dirname(HERE);
const KNOWN_FLAGS = ['--json', '--strict', '--tools', '--only', '-h', '--help'];
/* html-validate 的 recommended 把 style="" 一律判 error，但动态宽高/进度条这类写法
   在真实项目里是常规手段（实测 15 个页面里 197 条），降级为 warn，否则门禁会被淹没。
   需要它变硬判时用 --strict。 */
const DOWNGRADE = { 'no-inline-style': 'warn' };

class LintError extends Error {}

function fail(msg) {
  process.stderr.write(`ERROR  ${msg}\n`);
  return 2;
}

function findToolsDir(explicit) {
  /* 显式给了 --tools 就以它为准：那里没有依赖就报错，不能回头去猜别的目录，
     否则"指错路径"会被静默当成"用另一份安装"，检查结果与调用者的意图不符。 */
  if (explicit) {
    const nm = path.join(explicit, 'node_modules');
    if (fs.existsSync(path.join(nm, 'stylelint')) && fs.existsSync(path.join(nm, 'html-validate'))) {
      return explicit;
    }
    throw new LintError(`--tools 指向的目录里没有 stylelint + html-validate：${explicit}`);
  }
  const candidates = [];
  if (process.env.SFD_TOOLS) candidates.push(process.env.SFD_TOOLS);
  let dir = SKILL;
  for (let i = 0; i < 6 && dir !== path.dirname(dir); i += 1) {
    candidates.push(path.join(dir, '.sfd-tools'));
    dir = path.dirname(dir);
  }
  candidates.push(path.join(process.cwd(), '.sfd-tools'));
  for (const c of candidates) {
    const nm = path.join(c, 'node_modules');
    if (c && fs.existsSync(path.join(nm, 'stylelint')) && fs.existsSync(path.join(nm, 'html-validate'))) {
      return c;
    }
  }
  throw new LintError(
    '找不到结构层依赖（stylelint + html-validate）。安装：在仓库根建 .sfd-tools 并执行 ' +
    'cd .sfd-tools && npm install。未安装时本门禁不参与判定，其他四个门禁仍要跑。');
}

function expandInputs(args) {
  const files = [];
  for (const a of args) {
    const p = path.resolve(a);
    const st = fs.existsSync(p) ? fs.statSync(p) : null;
    if (st && st.isDirectory()) {
      for (const f of walk(p)) files.push(f);
    } else if (st && st.isFile()) {
      files.push(p);
    } else {
      throw new LintError(`路径不存在：${a}`);
    }
  }
  return files.filter((f) => ['.html', '.htm', '.css'].includes(path.extname(f).toLowerCase()));
}

function* walk(dir) {
  for (const e of fs.readdirSync(dir, {withFileTypes: true})) {
    if (e.name === 'node_modules' || e.name.startsWith('.')) continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) yield* walk(p);
    else if (['.html', '.htm', '.css'].includes(path.extname(e.name).toLowerCase())) yield p;
  }
}

function readJson(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

async function runStylelint(toolsDir, files, configPath) {
  if (!files.length) return [];
  const require = createRequire(path.join(toolsDir, 'noop.js'));
  const stylelint = require('stylelint');
  const from = {paths: [path.join(toolsDir, 'node_modules')]};
  const config = readJson(configPath);
  config.plugins = (config.plugins || []).map((p) => require.resolve(p, from));
  config.overrides = [
    {files: ['**/*.html', '**/*.htm'], customSyntax: require.resolve('postcss-html', from)},
  ];
  const res = await stylelint.lint({files, config, configBasedir: toolsDir});
  const out = [];
  for (const r of res.results) {
    // stylelint 会把配错的规则名/选项塞进 invalidOptionWarnings 然后一条不报；
    // 那等于给我的门禁发绿灯，必须当成调用失败响
    for (const w of r.invalidOptionWarnings || []) {
      throw new LintError(`stylelint 配置无效：${w.text}`);
    }
    for (const w of r.warnings) {
      // 未知规则名会作为普通 warning 返回；同样是我配错，必须响而不是当成页面缺陷
      if (/^Unknown rule /i.test(String(w.text || ''))) {
        throw new LintError(`stylelint 配置里有不存在的规则：${w.text}`);
      }
      out.push({
        file: path.relative(process.cwd(), r.source).replace(/\\/g, '/'),
        line: w.line || 1,
        rule: w.rule || 'css-parse',
        severity: w.severity === 'warning' ? 'warn' : 'hard',
        measured: String(w.text || '').slice(0, 160),
        threshold: '-',
        message: 'CSS 解析层（stylelint）：' + String(w.text || '').replace(/\s*\([^)]*\)\s*$/, ''),
        source: 'structure-lint',
      });
    }
  }
  return out;
}

async function runHtmlValidate(toolsDir, files, configPath) {
  const html = files.filter((f) => ['.html', '.htm'].includes(path.extname(f).toLowerCase()));
  if (!html.length) return [];
  const require = createRequire(path.join(toolsDir, 'noop.js'));
  const {HtmlValidate} = require('html-validate');
  const hv = new HtmlValidate(readJson(configPath));
  const out = [];
  for (const f of html) {
    const res = await hv.validateFile(f);
    for (const r of res.results) {
      for (const m of r.messages) {
        // 配置里写错规则名会被 html-validate 当消息返回；那是我配错，不是页面有病，必须响
        if (/Definition for rule .* was not found/.test(m.message || '')) {
          throw new LintError(`html-validate 配置里有不存在的规则：${m.message}`);
        }
        out.push({
          file: path.relative(process.cwd(), f).replace(/\\/g, '/'),
          line: m.line || 1,
          rule: m.ruleId || 'html-parse',
          severity: DOWNGRADE[m.ruleId] || (m.severity === 1 ? 'warn' : 'hard'),
          measured: String(m.message || '').slice(0, 160),
          threshold: '-',
          message: '标记校验层（html-validate）：' + String(m.message || ''),
          source: 'structure-lint',
        });
      }
    }
  }
  return out;
}

function dedupe(findings) {
  const seen = new Set();
  const out = [];
  for (const x of findings) {
    const key = `${x.file}:${x.line}:${x.rule}:${x.measured}`;
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(x);
  }
  return out;
}

async function main(rawArgv) {
  // 支持 --tools=<目录> 写法，和 python 侧门禁保持一致
  const argv = [];
  for (const a of rawArgv) {
    if (a.startsWith('--') && a.includes('=') && KNOWN_FLAGS.includes(a.split('=')[0])) {
      argv.push(a.split('=')[0], a.slice(a.indexOf('=') + 1));
    } else {
      argv.push(a);
    }
  }
  for (const a of argv) {
    if (a.startsWith('-') && !KNOWN_FLAGS.includes(a.split('=')[0])) {
      process.stderr.write(`ERROR  未知参数 ${JSON.stringify(a)}（可用：${KNOWN_FLAGS.join(', ')}）\n`);
      return 2;
    }
  }
  const flags = new Set(argv.filter((a) => a.startsWith('-') && !a.includes('=')));
  const getOpt = (name) => {
    const i = argv.indexOf(name);
    return i >= 0 ? argv[i + 1] : undefined;
  };
  if (flags.has('-h') || flags.has('--help')) {
    process.stdout.write('用法：node scripts/structure_lint.mjs <文件|目录> [...] [--json] [--strict] [--tools 目录] [--only css|html]\n');
    return 0;
  }
  const only = getOpt('--only');
  if (only !== undefined && !['css', 'html'].includes(only)) {
    process.stderr.write(`ERROR  --only 只接受 css 或 html，收到 ${JSON.stringify(only)}\n`);
    return 2;
  }
  const inputs = argv.filter((a, i) => !a.startsWith('-') && argv[i - 1] !== '--tools' && argv[i - 1] !== '--only');
  if (!inputs.length) {
    process.stderr.write('ERROR  需要至少一个 html/css 文件或目录\n');
    return 2;
  }

  let files;
  try {
    files = expandInputs(inputs);
    if (!files.length) throw new LintError('没有可检查的 css/html —— 空扫描不等于通过');
  } catch (e) {
    return fail(e.message);
  }

  let toolsDir;
  try {
    toolsDir = findToolsDir(getOpt('--tools'));
  } catch (e) {
    return fail(e.message);
  }

  let findings = [];
  try {
    if (only !== 'html') {
      findings = findings.concat(await runStylelint(toolsDir, files, path.join(SKILL, 'rules', 'stylelint.config.json')));
    }
    if (only !== 'css') {
      findings = findings.concat(await runHtmlValidate(toolsDir, files, path.join(SKILL, 'rules', 'html-validate.config.json')));
    }
  } catch (e) {
    return fail(`结构层执行失败：${e.message}`);
  }

  findings = dedupe(findings).sort((a, b) => (a.file + a.line + a.rule).localeCompare(b.file + b.line + b.rule));
  const hard = findings.filter((x) => x.severity === 'hard');
  const warn = findings.filter((x) => x.severity === 'warn');
  const strict = flags.has('--strict');

  if (flags.has('--json')) {
    process.stdout.write(JSON.stringify({scanned: files.length, tools: toolsDir.replace(/\\/g, '/'), hard, warn}, null, 2) + '\n');
  } else {
    for (const x of hard) {
      process.stdout.write(`FAIL  ${x.rule.padEnd(40)} ${x.file}:${x.line}  ${x.message} (measured ${x.measured})\n`);
    }
    for (const x of warn) {
      process.stdout.write(`WARN  ${x.rule.padEnd(40)} ${x.file}:${x.line}  ${x.message}\n`);
    }
    process.stdout.write('-'.repeat(72) + '\n');
    process.stdout.write(`scanned=${files.length} hard=${hard.length} warn=${warn.length}（结构层：stylelint + html-validate）\n`);
    process.stdout.write(hard.length || (strict && warn.length) ? 'RESULT: FAIL\n' : 'RESULT: PASS\n');
  }
  return hard.length || (strict && warn.length) ? 1 : 0;
}

main(process.argv.slice(2)).then((code) => process.exit(code), (e) => {
  process.stderr.write(`ERROR  未预期失败：${e && e.message ? e.message : e}\n`);
  process.exit(2);
});
