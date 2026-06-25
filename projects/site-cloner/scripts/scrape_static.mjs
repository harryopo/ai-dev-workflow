import scrape from 'website-scraper';
import { existsSync, mkdirSync } from 'fs';
import { resolve } from 'path';

const args = process.argv.slice(2);
const url = args[0];
const outputDir = args[1] || './output';
const maxDepth = parseInt(args[2]) || 3;

if (!url) {
    console.log('用法: node scrape_static.mjs <URL> [输出目录] [最大深度]');
    console.log('示例: node scrape_static.mjs https://example.com ./output 3');
    process.exit(1);
}

const dir = resolve(outputDir);
if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
}

console.log(`开始下载: ${url}`);
console.log(`输出目录: ${dir}`);
console.log(`最大深度: ${maxDepth}`);
console.log('-'.repeat(50));

try {
    const result = await scrape({
        urls: [url],
        directory: dir,
        recursive: true,
        maxRecursiveDepth: maxDepth,
        defaultFilename: 'index.html',
        prettifyUrls: true,
        ignoreErrors: true,
        requestConcurrency: 5,
        request: {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
            },
            retry: { limit: 3 }
        },
        subdirectories: [
            { directory: 'css', extensions: ['.css'] },
            { directory: 'js', extensions: ['.js'] },
            { directory: 'images', extensions: ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', '.webp'] },
            { directory: 'fonts', extensions: ['.woff', '.woff2', '.ttf', '.eot', '.otf'] },
            { directory: 'media', extensions: ['.mp4', '.webm', '.mp3', '.wav'] }
        ],
        plugins: [{
            apply(registerAction) {
                registerAction('onResourceSaved', ({ resource }) => {
                    console.log(`  ✓ ${resource.getUrl()}`);
                });
                registerAction('onResourceError', ({ resource, error }) => {
                    console.log(`  ✗ ${resource.getUrl()} — ${error.message}`);
                });
            }
        }]
    });

    console.log('-'.repeat(50));
    console.log(`完成！下载了 ${result.length} 个资源到 ${dir}`);
} catch (err) {
    console.error(`下载失败: ${err.message}`);
    process.exit(1);
}
