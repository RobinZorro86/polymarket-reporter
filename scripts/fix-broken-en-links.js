#!/usr/bin/env node
/**
 * Fix broken links in English pages that point to non-existent EN paths
 * Redirect them to corresponding ZH paths where deep content exists
 */

const fs = require('fs');
const path = require('path');

const fixes = [
  {
    file: 'en/kol/index.html',
    replacements: [
      { from: 'href="/en/knowledge-base/kol/rankings/"', to: 'href="/zh/knowledge-base/kol/rankings/"' },
      { from: 'href="/en/knowledge-base/kol/vladic_eth/"', to: 'href="/zh/knowledge-base/kol/vladic_eth/"' },
      { from: 'href="/en/knowledge-base/kol/noisyb0y1/"', to: 'href="/zh/knowledge-base/kol/noisyb0y1/"' }
    ]
  },
  {
    file: 'en/strategies/index.html',
    replacements: [
      { from: 'href="/en/knowledge-base/strategies/signal-sniper/"', to: 'href="/zh/knowledge-base/strategies/signal-sniper/"' },
      { from: 'href="/en/knowledge-base/strategies/weather-trader/"', to: 'href="/zh/knowledge-base/strategies/weather-trader/"' },
      { from: 'href="/en/knowledge-base/strategies/fast-loop/"', to: 'href="/zh/knowledge-base/strategies/fast-loop/"' },
      { from: 'href="/en/knowledge-base/strategies/divergence/"', to: 'href="/zh/knowledge-base/strategies/divergence/"' },
      { from: 'href="/en/knowledge-base/strategies/mert-sniper/"', to: 'href="/zh/knowledge-base/strategies/mert-sniper/"' },
      { from: 'href="/en/knowledge-base/strategies/copytrading/"', to: 'href="/zh/knowledge-base/strategies/copytrading/"' }
    ]
  }
];

const baseDir = process.cwd();
let fixedCount = 0;
let totalReplacements = 0;

fixes.forEach(({ file, replacements }) => {
  const filePath = path.join(baseDir, file);
  
  if (!fs.existsSync(filePath)) {
    console.log(`⚠️  File not found: ${file}`);
    return;
  }
  
  let content = fs.readFileSync(filePath, 'utf8');
  let fileChanged = false;
  
  replacements.forEach(({ from, to }) => {
    if (content.includes(from)) {
      content = content.replace(from, to);
      console.log(`  ✅ ${file}: ${from} → ${to}`);
      fileChanged = true;
      totalReplacements++;
    }
  });
  
  if (fileChanged) {
    fs.writeFileSync(filePath, content, 'utf8');
    fixedCount++;
  }
});

console.log(`\nTotal files modified: ${fixedCount}/${fixes.length}`);
console.log(`Total link replacements: ${totalReplacements}`);
