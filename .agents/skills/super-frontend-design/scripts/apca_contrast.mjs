#!/usr/bin/env node
/* APCA Lc 计算器：stdin 收 [{fg:[r,g,b], bg:[r,g,b]}, ...]（0-255 sRGB），
   stdout 出 [Lc, ...]，算不出来的位置给 null（不猜）。

   算法交给 colorjs.io（0.7.1，MIT），本脚本不自己实现 APCA —— 手写一版近似值
   会给出"看起来对"的数字，那比没数字更糟。

   符号约定：APCA 不对称，深字浅底返回负数（实测黑字白底 -107.88，白字黑底 +106.04）。
   条文里的「Lc≥60」讲的是绝对值，所以这里取 |Lc|，render_probe 再与阈值比。

   退出码：0 正常 / 2 依赖缺失或输入不合法。
*/

import process from 'node:process';
import {createRequire} from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SKILL = path.dirname(HERE);

function die(msg) {
  process.stderr.write(`ERROR  ${msg}\n`);
  process.exit(2);
}

function toolsDir() {
  const cands = [];
  if (process.env.SFD_TOOLS) cands.push(process.env.SFD_TOOLS);
  let dir = SKILL;
  for (let i = 0; i < 6 && dir !== path.dirname(dir); i += 1) {
    cands.push(path.join(dir, '.sfd-tools'));
    dir = path.dirname(dir);
  }
  cands.push(path.join(process.cwd(), '.sfd-tools'));
  for (const c of cands) {
    if (c && fs.existsSync(path.join(c, 'node_modules', 'colorjs.io'))) return c;
  }
  die('找不到 colorjs.io。安装：在仓库根建 .sfd-tools 并执行 cd .sfd-tools && npm install');
}

function readStdin() {
  try {
    return fs.readFileSync(0, 'utf8');
  } catch (e) {
    die(`读不到 stdin：${e.message}`);
  }
}

const raw = readStdin();
if (!raw.trim()) die('stdin 为空：需要 [{fg:[r,g,b], bg:[r,g,b]}, ...]');

let pairs;
try {
  pairs = JSON.parse(raw);
} catch (e) {
  die(`stdin 不是合法 JSON：${e.message}`);
}
if (!Array.isArray(pairs)) die('stdin 必须是数组');

const require = createRequire(path.join(toolsDir(), 'noop.js'));
const mod = require('colorjs.io');
const Color = mod.default ?? mod.Color ?? mod;
if (typeof Color !== 'function') die('colorjs.io 的 Color 导入形态变了，需要检查版本');

const rgb = (arr) => {
  if (!Array.isArray(arr) || arr.length < 3) return null;
  const nums = arr.slice(0, 3).map(Number);
  if (!nums.every((n) => Number.isFinite(n))) return null;
  return nums.map((n) => Math.min(255, Math.max(0, n)) / 255);
};

const out = pairs.map((p) => {
  const fg = rgb(p && p.fg);
  const bg = rgb(p && p.bg);
  if (!fg || !bg) return null;
  try {
    return Math.abs(new Color('srgb', fg).contrast(new Color('srgb', bg), 'APCA'));
  } catch (e) {
    return null;
  }
});

process.stdout.write(JSON.stringify(out) + '\n');
