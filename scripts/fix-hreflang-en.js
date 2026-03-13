#!/usr/bin/env node
/**
 * Fix hreflang zh links in English pages
 * Issue: Some EN pages point to /zh/knowledge-base/* but should point to /zh/*
 */

const fs = require('fs');
const path = require('path');

const fixes = [
  {
    file: 'en/kol/index.html',
    from: 'hreflang="zh" href="https://www.pred101.com/zh/knowledge-base/kol/"',
    to: 'hreflang="zh" href="https://www.pred101.com/zh/kol/"'
  },
  {
    file: 'en/strategies/index.html',
    from: 'hreflang="zh" href="https://www.pred101.com/zh/knowledge-base/strategies/"',
    to: 'hreflang="zh" href="https://www.pred101.com/zh/strategies/"'
  }
];

const baseDir = process.cwd();
let fixedCount = 0;

fixes.forEach(({ file, from, to }) => {
  const filePath = path.join(baseDir, file);
  
  if (!fs.existsSync(filePath)) {
    console.log(`⚠️  File not found: ${file}`);
    return;
  }
  
  let content = fs.readFileSync(filePath, 'utf8');
  
  if (content.includes(from)) {
    content = content.replace(from, to);
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`✅ Fixed: ${file}`);
    fixedCount++;
  } else {
    console.log(`ℹ️  No match in: ${file}`);
  }
});

console.log(`\nTotal fixed: ${fixedCount}/${fixes.length}`);
