#!/usr/bin/env node
/**
 * Fix language switcher links in English pages
 * Make lang switcher point to corresponding ZH page instead of always /zh/
 */

const fs = require('fs');
const path = require('path');

// Map EN paths to their corresponding ZH paths
const pathMap = {
  'en/index.html': '/zh/',
  'en/about.html': '/zh/about.html',
  'en/search.html': '/zh/search.html',
  'en/kol/index.html': '/zh/kol/',
  'en/strategies/index.html': '/zh/strategies/',
  'en/resources/index.html': '/zh/knowledge-base/resources/',
  'en/learn/index.html': '/zh/learn/',
  'en/knowledge-base/index.html': '/zh/knowledge-base/',
  'en/reports/index.html': '/zh/reports/'
};

const baseDir = process.cwd();
let fixedCount = 0;

Object.entries(pathMap).forEach(([enPath, zhPath]) => {
  const filePath = path.join(baseDir, enPath);
  
  if (!fs.existsSync(filePath)) {
    console.log(`⚠️  File not found: ${enPath}`);
    return;
  }
  
  let content = fs.readFileSync(filePath, 'utf8');
  
  // Look for lang switcher pattern: <a href="/zh/" ...>中文</a> or similar
  const oldPattern = 'href="/zh/"';
  const newPattern = `href="${zhPath}"`;
  
  // Only fix if the current href is the generic /zh/ and we want something more specific
  if (zhPath !== '/zh/' && content.includes(oldPattern)) {
    // Be careful to only replace in lang-switcher context
    const langSwitchPattern = /(<div class="lang-switch">.*?)(href="\/zh\/")(.*?<\/div>)/s;
    
    if (langSwitchPattern.test(content)) {
      content = content.replace(langSwitchPattern, `$1href="${zhPath}"$3`);
      fs.writeFileSync(filePath, content, 'utf8');
      console.log(`✅ Fixed lang switcher: ${enPath} → ${zhPath}`);
      fixedCount++;
    } else {
      console.log(`ℹ️  No lang-switch pattern in: ${enPath}`);
    }
  } else if (zhPath === '/zh/') {
    console.log(`ℹ️  Already correct (homepage): ${enPath}`);
  } else {
    console.log(`ℹ️  No generic /zh/ link to fix in: ${enPath}`);
  }
});

console.log(`\nTotal fixed: ${fixedCount}`);
