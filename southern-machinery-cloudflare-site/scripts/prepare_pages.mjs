#!/usr/bin/env node
import { copyFile, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { basename, resolve } from 'node:path';

const [bundlePath, outputPath, configPath] = process.argv.slice(2);

if (!bundlePath || !outputPath || !configPath) {
  console.error('Usage: prepare_pages.mjs <worker-bundle> <output-dir> <pages-wrangler-template>');
  process.exit(2);
}

const bundle = resolve(bundlePath);
const output = resolve(outputPath);
const config = resolve(configPath);

if (basename(bundle) === '_worker.js' && resolve(bundle, '..') === output) {
  console.error('Bundle must be outside the output directory because output is recreated.');
  process.exit(2);
}

await readFile(bundle);
await readFile(config);
await rm(output, { recursive: true, force: true });
await mkdir(output, { recursive: true });
await copyFile(bundle, resolve(output, '_worker.js'));
await copyFile(config, resolve(output, 'wrangler.toml'));
await writeFile(resolve(output, '_routes.json'), `${JSON.stringify({
  version: 1,
  include: ['/*'],
  exclude: [],
}, null, 2)}\n`);

console.log(`Prepared Pages Advanced Mode output: ${output}`);
