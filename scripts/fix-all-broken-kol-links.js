#!/usr/bin/env node
/**
 * Fix all broken links to non-existent EN KOL pages
 * Redirect them to corresponding ZH paths
 */

const fs = require('fs');
const path = require('path');

const kolPages = [
  'rankings',
  'vladic_eth',
  'noisyb0y1',
  'rohonchain',
  'edwordkaru',
  'dmitriyungarov',
  '0xchainmind',
  'aleiahlock',
  'ayi_ainotes',
  'cutnpaste4',
  'molt-cornelius',
  'runes-leo'
];

const baseDir = process.cwd();
const enDir = path.join(baseDir, 'en');
let totalReplacements = 0;
let filesModified = 0;

function processDirectory(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  
  entries.forEach(entry => {
    const fullPath = path.join(dir, entry.name);
    
    if (entry.isDirectory()) {
      processDirectory(fullPath);
    } else if (entry.isFile() && entry.name.endsWith('.html')) {
      let content = fs.readFileSync(fullPath, 'utf8');
      let changed = false;
      
      kolPages.forEach(kol => {
        const from = `href="/en/knowledge-base/kol/${kol}/"`;
        const to = `href="/zh/knowledge-base/kol/${kol}/"`;
        
        if (content.includes(from)) {
          content = content.split(from).join(to);
          console.log(`  ✅ ${path.relative(baseDir, fullPath)}: KOL ${kol} → ZH`);
          changed = true;
          totalReplacements++;
        }
      });
      
      if (changed) {
        fs.writeFileSync(fullPath, content, 'utf8');
        filesModified++;
      }
    }
  });
}

console.log('Scanning English files for broken KOL links...\n');
processDirectory(enDir);

console.log(`\nTotal files modified: ${filesModified}`);
console.log(`Total link replacements: ${totalReplacements}`);
