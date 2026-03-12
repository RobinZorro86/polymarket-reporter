#!/usr/bin/env python3
"""
Phase-2 Plan B 自动验证脚本
验证内容：
1. 英文路径内容纯净度（无中文残留）
2. 中文路径完整性（无英文污染）
3. 旧路径跳转配置
4. Canonical / Hreflang 一致性
5. 语言切换器覆盖
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

class Phase2Verifier:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.issues = []
        self.stats = {
            'en_pages': 0,
            'zh_pages': 0,
            'en_with_chinese': 0,
            'zh_with_english': 0,
            'missing_lang_switch': 0,
            'broken_canonical': 0,
            'broken_hreflang': 0
        }
    
    def check_chinese_in_english(self) -> List[Tuple[str, List[str]]]:
        """检查英文页面中的中文残留"""
        issues = []
        en_dir = self.base_dir / "en"
        
        # 中文正则（排除技术术语和预期文案）
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
        # 预期的中文（语言切换器中的"中文"链接）
        expected_chinese = {'中文', '简体中文'}
        
        for html_file in en_dir.rglob("*.html"):
            if html_file.name.endswith(".backup"):
                continue
            
            content = html_file.read_text(encoding='utf-8')
            chinese_matches = chinese_pattern.findall(content)
            
            # 过滤预期的中文
            unexpected_chinese = [m for m in chinese_matches if m not in expected_chinese]
            
            if unexpected_chinese:
                issues.append((str(html_file.relative_to(self.base_dir)), unexpected_chinese[:5]))
                self.stats['en_with_chinese'] += 1
            
            self.stats['en_pages'] += 1
        
        return issues
    
    def check_english_in_chinese(self) -> List[Tuple[str, List[str]]]:
        """检查中文页面中的英文污染（排除技术术语）"""
        issues = []
        zh_dir = self.base_dir / "zh"
        
        # 英文标题/正文正则（排除 HTML 标签、URL、技术术语）
        english_title_pattern = re.compile(r'<title>([A-Za-z\s,\.]+)</title>')
        english_heading_pattern = re.compile(r'<h[1-3][^>]*>([A-Za-z\s,\.]+)</h[1-3]>')
        
        # 预期的英文（技术术语、产品名）
        expected_english = {'HTML', 'CSS', 'API', 'GitHub', 'OpenClaw', 'Polymarket', 'Simmer', 'USD', 'BTC', 'ETH'}
        
        for html_file in zh_dir.rglob("*.html"):
            if html_file.name.endswith(".backup"):
                continue
            
            content = html_file.read_text(encoding='utf-8')
            
            # 检查标题
            title_matches = english_title_pattern.findall(content)
            heading_matches = english_heading_pattern.findall(content)
            
            suspicious = []
            for match in title_matches + heading_matches:
                words = match.split()
                if len(words) > 3:  # 长英文标题可疑
                    suspicious.append(match.strip()[:50])
            
            if suspicious:
                issues.append((str(html_file.relative_to(self.base_dir)), suspicious[:3]))
                self.stats['zh_with_english'] += 1
            
            self.stats['zh_pages'] += 1
        
        return issues
    
    def check_old_path_redirects(self) -> Dict[str, bool]:
        """检查旧路径跳转配置"""
        results = {}
        
        # 检查 vercel.json
        vercel_json = self.base_dir / "vercel.json"
        if vercel_json.exists():
            content = vercel_json.read_text(encoding='utf-8')
            results['vercel_json_redirects'] = '/knowledge-base/' in content and '/en/knowledge-base/' in content
            results['vercel_json_reports'] = '/reports/' in content and '/en/reports/' in content
        else:
            results['vercel_json_redirects'] = False
            results['vercel_json_reports'] = False
        
        # 检查根路径 index.html
        kb_index = self.base_dir / "knowledge-base" / "index.html"
        reports_index = self.base_dir / "reports" / "index.html"
        
        if kb_index.exists():
            content = kb_index.read_text(encoding='utf-8')
            results['kb_meta_refresh'] = 'http-equiv="refresh"' in content and '/en/knowledge-base/' in content
        else:
            results['kb_meta_refresh'] = False
        
        if reports_index.exists():
            content = reports_index.read_text(encoding='utf-8')
            results['reports_meta_refresh'] = 'http-equiv="refresh"' in content and '/en/reports/' in content
        else:
            results['reports_meta_refresh'] = False
        
        return results
    
    def check_canonical_hreflang(self) -> Dict[str, List[str]]:
        """检查 canonical 和 hreflang 配置"""
        issues = {'en': [], 'zh': []}
        
        # 检查 EN 页面
        en_dir = self.base_dir / "en"
        for html_file in en_dir.rglob("*.html"):
            if html_file.name.endswith(".backup"):
                continue
            
            content = html_file.read_text(encoding='utf-8')
            
            # 检查 canonical
            has_canonical = 'rel="canonical"' in content
            has_hreflang_en = 'hreflang="en"' in content
            has_hreflang_zh = 'hreflang="zh"' in content
            
            if not has_canonical or not has_hreflang_en or not has_hreflang_zh:
                issues['en'].append(str(html_file.relative_to(self.base_dir)))
                self.stats['broken_hreflang'] += 1
        
        # 检查 ZH 页面
        zh_dir = self.base_dir / "zh"
        for html_file in zh_dir.rglob("*.html"):
            if html_file.name.endswith(".backup"):
                continue
            
            content = html_file.read_text(encoding='utf-8')
            
            has_canonical = 'rel="canonical"' in content
            has_hreflang_en = 'hreflang="en"' in content
            has_hreflang_zh = 'hreflang="zh"' in content
            
            if not has_canonical or not has_hreflang_en or not has_hreflang_zh:
                issues['zh'].append(str(html_file.relative_to(self.base_dir)))
                self.stats['broken_hreflang'] += 1
        
        return issues
    
    def check_lang_switcher(self) -> List[str]:
        """检查语言切换器覆盖"""
        missing = []
        
        # 检查 EN 页面
        en_dir = self.base_dir / "en"
        for html_file in en_dir.rglob("*.html"):
            if html_file.name.endswith(".backup"):
                continue
            
            content = html_file.read_text(encoding='utf-8')
            
            # 检查是否有语言切换器（包括内联样式和 class 方式）
            has_switcher = (
                'lang-switch' in content or 
                '中文' in content or 
                'Chinese' in content
            )
            
            if not has_switcher:
                missing.append(str(html_file.relative_to(self.base_dir)))
                self.stats['missing_lang_switch'] += 1
        
        # 检查 ZH 页面
        zh_dir = self.base_dir / "zh"
        for html_file in zh_dir.rglob("*.html"):
            if html_file.name.endswith(".backup"):
                continue
            
            content = html_file.read_text(encoding='utf-8')
            
            # 检查是否有语言切换器（包括内联样式和 class 方式）
            has_switcher = (
                'lang-switch' in content or 
                'English' in content or 
                'EN' in content
            )
            
            if not has_switcher:
                missing.append(str(html_file.relative_to(self.base_dir)))
                self.stats['missing_lang_switch'] += 1
        
        return missing
    
    def run_full_check(self) -> Dict:
        """运行完整验证"""
        print("=" * 60)
        print("Phase-2 Plan B 自动验证")
        print("=" * 60)
        
        # 1. 英文路径纯净度
        print("\n1. 检查英文路径中文残留...")
        en_issues = self.check_chinese_in_english()
        if en_issues:
            print(f"   ⚠️ 发现 {len(en_issues)} 个页面含中文残留")
            for path, chars in en_issues[:3]:
                print(f"      - {path}: {', '.join(chars)}")
        else:
            print("   ✅ 英文路径无中文残留")
        
        # 2. 中文路径完整性
        print("\n2. 检查中文路径英文污染...")
        zh_issues = self.check_english_in_chinese()
        if zh_issues:
            print(f"   ⚠️ 发现 {len(zh_issues)} 个页面含英文污染")
            for path, titles in zh_issues[:3]:
                print(f"      - {path}: {', '.join(titles)}")
        else:
            print("   ✅ 中文路径无英文污染")
        
        # 3. 旧路径跳转
        print("\n3. 检查旧路径跳转配置...")
        redirects = self.check_old_path_redirects()
        all_redirects_ok = all(redirects.values())
        if all_redirects_ok:
            print("   ✅ 旧路径跳转配置正确")
        else:
            print("   ⚠️ 跳转配置问题:")
            for key, val in redirects.items():
                if not val:
                    print(f"      - {key}: ❌")
        
        # 4. Canonical / Hreflang
        print("\n4. 检查 Canonical / Hreflang...")
        hreflang_issues = self.check_canonical_hreflang()
        total_broken = len(hreflang_issues['en']) + len(hreflang_issues['zh'])
        if total_broken > 0:
            print(f"   ⚠️ 发现 {total_broken} 个页面缺少配置")
            for path in hreflang_issues['en'][:3]:
                print(f"      - en/{path}")
            for path in hreflang_issues['zh'][:3]:
                print(f"      - zh/{path}")
        else:
            print("   ✅ Canonical / Hreflang 配置完整")
        
        # 5. 语言切换器
        print("\n5. 检查语言切换器覆盖...")
        missing_switcher = self.check_lang_switcher()
        if missing_switcher:
            print(f"   ⚠️ 发现 {len(missing_switcher)} 个页面缺少语言切换器")
            for path in missing_switcher[:10]:
                print(f"      - {path}")
        else:
            print("   ✅ 语言切换器全覆盖")
        
        # 统计汇总
        print("\n" + "=" * 60)
        print("统计汇总")
        print("=" * 60)
        print(f"英文页面数：{self.stats['en_pages']}")
        print(f"中文页面数：{self.stats['zh_pages']}")
        print(f"英文路径中文残留：{self.stats['en_with_chinese']} 页")
        print(f"中文路径英文污染：{self.stats['zh_with_english']} 页")
        print(f"缺少语言切换器：{self.stats['missing_lang_switch']} 页")
        print(f"Canonical/Hreflang 问题：{self.stats['broken_hreflang']} 页")
        
        # 总体结论
        print("\n" + "=" * 60)
        all_passed = (
            len(en_issues) == 0 and
            len(zh_issues) == 0 and
            all_redirects_ok and
            total_broken == 0 and
            len(missing_switcher) == 0
        )
        
        if all_passed:
            print("✅ Phase-2 Plan B 全部验证通过")
        else:
            print("⚠️ 发现需要修复的问题")
        
        print("=" * 60)
        
        return {
            'passed': all_passed,
            'en_issues': en_issues,
            'zh_issues': zh_issues,
            'redirects': redirects,
            'hreflang_issues': hreflang_issues,
            'missing_switcher': missing_switcher,
            'stats': self.stats
        }

if __name__ == "__main__":
    os.chdir("/home/zqd/.openclaw/workspace/polymarket-reporter")
    verifier = Phase2Verifier(".")
    result = verifier.run_full_check()
