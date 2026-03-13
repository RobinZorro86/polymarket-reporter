#!/usr/bin/env node
/**
 * Fix language switcher links in Chinese pages
 * Make lang switcher point to corresponding EN page instead of always /en/
 */

const fs = require('fs');
const path = require('path');

// Map ZH paths to their corresponding EN paths
const pathMap = {
  'zh/index.html': '/en/',
  'zh/about.html': '/en/about.html',
  'zh/search.html': '/en/search.html',
  'zh/kol/index.html': '/en/kol/',
  'zh/strategies/index.html': '/en/strategies/',
  'zh/knowledge-base/resources/index.html': '/en/resources/',
  'zh/learn/index.html': '/en/learn/',
  'zh/knowledge-base/index.html': '/en/knowledge-base/',
  'zh/reports/index.html': '/en/reports/'
};

const baseDir = process.cwd();
let fixedCount = 0;

Object.entries(pathMap).forEach(([zhPath, enPath]) => {
  const filePath = path.join(baseDir, zhPath);
  
  if (!fs.existsSync(filePath)) {
    console.log(`⚠️  File not found: ${zhPath}`);
    return;
  }
  
  let content = fs.readFileSync(filePath, 'utf8');
  
  // Look for lang switcher pattern: <a href="/en/" ...>EN</a> or similar
  const oldPattern = 'href="/en/"';
  const newPattern = `href="${enPath}"`;
  
  // Only fix if the current href is the generic /en/ and we want something more specific
  if (enPath !== '/en/' && content.includes(oldPattern)) {
    // Be careful to only replace in lang-switcher context
    const langSwitchPattern = /(<div class="lang-switch">.*?)(href="\/en\/")(.*?<\/div>)/s;
    
    if (langSwitchPattern.test(content)) {
      content = content.replace(langSwitchPattern, `$1href="${enPath}"$3`);
      fs.writeFileSync(filePath, content, 'utf8');
      console.log(`✅ Fixed lang switcher: ${zhPath} → ${enPath}`);
      fixedCount++;
    } else {
      console.log(`ℹ️  No lang-switch pattern in: ${zhPath}`);
    }
  } else if (enPath === '/en/') {
    console.log(`ℹ️  Already correct (homepage): ${zhPath}`);
  } else {
    console.log(`ℹ️  No generic /en/ link to fix in: ${zhPath}`);
  }
});

console.log(`\nTotal fixed: ${fixedCount}`);
