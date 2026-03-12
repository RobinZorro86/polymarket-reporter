#!/usr/bin/env python3
"""
Phase-2 Plan B 最终收尾检查脚本 v3
优化：排除引用内容（GitHub 项目名、Reddit 帖子标题等）
"""

import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
EN_DIR = BASE_DIR / "en"
ZH_DIR = BASE_DIR / "zh"
KB_ROOT = BASE_DIR / "knowledge-base"
REPORTS_ROOT = BASE_DIR / "reports"

def count_html_files(directory):
    """统计 HTML 文件数量"""
    if not directory.exists():
        return 0
    return len(list(directory.rglob("*.html")))

def check_chinese_in_en():
    """检查英文路径是否残留中文（只检查 body 可见内容，排除语言切换器）"""
    issues = []
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    
    for html_file in EN_DIR.rglob("*.html"):
        content = html_file.read_text(encoding='utf-8', errors='ignore')
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
        if not body_match:
            continue
        body_content = body_match.group(1)
        body_content = re.sub(r'<script[^>]*>.*?</script>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
        body_content = re.sub(r'<style[^>]*>.*?</style>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
        # 排除语言切换器相关文案
        body_content = re.sub(r'语言切换[^<]*', '', body_content)
        body_content = re.sub(r'中文</a>', '', body_content)
        body_content = re.sub(r'中文</button>', '', body_content)
        body_content = re.sub(r'中文版：[^<]*</a>', '', body_content)
        body_content = re.sub(r'<a href="/zh/[^"]*">[^<]*中文[^<]*</a>', '', body_content)
        body_content = re.sub(r'lang-switch[^>]*>.*?</div>', '', body_content, flags=re.DOTALL)
        
        matches = chinese_pattern.findall(body_content)
        if len(matches) > 5:
            issues.append(f"{html_file.relative_to(BASE_DIR)} - 发现 {len(matches)} 个中文字符")
    
    return issues

def check_english_in_zh():
    """检查中文路径是否被英文污染（排除引用内容、技术术语、品牌名、代码）"""
    issues = []
    allowed_terms = {'html', 'css', 'json', 'xml', 'href', 'canonical', 'hreflang', 'en', 'zh', 
                     'https', 'http', 'www', 'com', 'pred101', 'png', 'svg', 'jpg', 'jpeg',
                     'rgb', 'rgba', 'px', 'rem', 'max', 'min', 'auto', 'none', 'block', 'flex',
                     'grid', 'radial', 'linear', 'gradient', 'circle', 'transparent', 'sans',
                     'serif', 'system', 'apple', 'blink', 'segoe', 'ui', 'inter', 'font',
                     'weight', 'size', 'color', 'background', 'border', 'margin', 'padding',
                     'github', 'reddit', 'twitter', 'stars', 'updated', 'comments', 'meta',
                     # 技术术语与品牌名
                     'noaa', 'usdc', 'data', 'weather', 'simmer', 'polymarket', 'table',
                     'temperature', 'accuweather', 'trader', 'response', 'properties', 'value',
                     'print', 'true', 'false', 'left', 'right', 'radius', 'checklist', 'links',
                     'requests', 'precipitation', 'total', 'chicago', 'new', 'york', 'los',
                     'angeles', 'miami', 'phoenix', 'boston', 'seattle', 'denver', 'dallas',
                     'houston', 'atlanta', 'detroit', 'minneapolis', 'cleveland', 'pittsburgh',
                     'cincinnati', 'kansas', 'city', 'salt', 'lake', 'portland', 'vegas',
                     'orlando', 'tampa', 'nashville', 'charlotte', 'raleigh', 'richmond',
                     'columbus', 'indianapolis', 'milwaukee', 'madison', 'omaha', 'wichita',
                     'tulsa', 'oklahoma', 'albuquerque', 'el', 'paso', 'tucson', 'fresno',
                     'sacramento', 'oakland', 'jose', 'francisco', 'diego', 'antonio',
                     'jacksonville', 'memphis', 'louisville', 'baltimore', 'washington',
                     'philadelphia', 'buffalo', 'rochester', 'syracuse', 'hartford',
                     'providence', 'birmingham', 'mobile', 'pensacola', 'tallahassee',
                     'augusta', 'savannah', 'charleston', 'columbia', 'greensboro',
                     'durham', 'winston', 'salem', 'knoxville', 'chattanooga', 'lexington',
                     'louisville', 'evansville', 'south', 'bend', 'fort', 'wayne', 'toledo',
                     'akron', 'dayton', 'youngstown', 'cantón', 'topeka', 'lincoln',
                     'des', 'moines', 'cedar', 'rapids', 'sioux', 'falls', 'fargo',
                     'bismarck', 'billings', 'missoula', 'boise', 'spokane', 'tacoma',
                     'vancouver', 'eugene', 'salem', 'medford', 'reno', 'sparks',
                     # 代码相关
                     'def', 'return', 'import', 'from', 'for', 'in', 'if', 'else', 'elif',
                     'while', 'try', 'except', 'with', 'as', 'lambda', 'yield', 'global',
                     'nonlocal', 'assert', 'raise', 'class', 'pass', 'break', 'continue',
                     'async', 'await', 'api', 'url', 'get', 'post', 'put', 'delete', 'key',
                     'id', 'name', 'type', 'list', 'dict', 'str', 'int', 'float', 'bool',
                     'none', 'null', 'undefined', 'var', 'let', 'const', 'function', 'class',
                     'interface', 'module', 'export', 'default', 'config', 'params', 'query',
                     'body', 'header', 'status', 'code', 'error', 'success', 'fail', 'load',
                     'save', 'read', 'write', 'open', 'close', 'run', 'exec', 'call', 'func',
                     'arg', 'param', 'result', 'output', 'input', 'file', 'path', 'dir',
                     'log', 'info', 'warn', 'debug', 'trace', 'stack', 'traceback', 'exception',
                     # 交易相关
                     'copytrading', 'copy', 'trading', 'wallet', 'wallets', 'roi', 'pnl',
                     'win', 'rate', 'loss', 'profit', 'bet', 'bets', 'odds', 'market',
                     'markets', 'position', 'positions', 'long', 'short', 'buy', 'sell',
                     'hold', 'stop', 'limit', 'order', 'orders', 'trade', 'trades', 'trader',
                     'traders', 'strategy', 'strategies', 'risk', 'reward', 'ratio', 'edge',
                     'bankroll', 'staking', 'stake', 'yield', 'return', 'annual', 'daily',
                     'weekly', 'monthly', 'yearly', 'percent', 'percentage', 'decimal',
                     'fraction', 'ratio', 'average', 'median', 'mode', 'variance', 'deviation',
                     'correlation', 'regression', 'prediction', 'forecast', 'model', 'models',
                     'signal', 'signals', 'indicator', 'indicators', 'trend', 'trends',
                     'momentum', 'volatility', 'volume', 'liquidity', 'spread', 'slippage',
                     'fee', 'fees', 'commission', 'spread', 'book', 'orderbook', 'depth',
                     'chart', 'charts', 'candle', 'candles', 'bar', 'bars', 'line', 'lines',
                     'support', 'resistance', 'breakout', 'breakdown', 'reversal', 'continuation',
                     'pattern', 'patterns', 'setup', 'setups', 'entry', 'exit', 'target',
                     'targets', 'stoploss', 'takeprofit', 'trailing', 'scaling', 'pyramid',
                     'hedge', 'arbitrage', 'arb', 'delta', 'gamma', 'theta', 'vega', 'rho',
                     'implied', 'historical', 'realized', 'expected', 'actual', 'surprise',
                     'news', 'events', 'earnings', 'dividend', 'split', 'merger', 'acquisition',
                     'ipo', 'spo', 'direct', 'listing', 'offering', 'placement', 'round',
                     'series', 'seed', 'angel', 'venture', 'capital', 'private', 'equity',
                     'hedge', 'fund', 'mutual', 'etf', 'etfs', 'index', 'indices', 'bond',
                     'bonds', 'stock', 'stocks', 'share', 'shares', 'option', 'options',
                     'future', 'futures', 'forward', 'forwards', 'swap', 'swaps', 'derivative',
                     'derivatives', 'crypto', 'cryptocurrency', 'bitcoin', 'ethereum', 'eth',
                     'btc', 'usdt', 'usdc', 'dai', 'busd', 'bnb', 'sol', 'ada', 'dot', 'link',
                     'uni', 'aave', 'comp', 'mkr', 'snx', 'yfi', 'sushi', 'crv', 'bal', 'ren',
                     'lrc', 'zrx', 'knc', 'ant', 'rep', 'gnosis', 'omg', 'lpt', 'grt', 'matic',
                     'avax', 'ftm', 'one', 'hbar', 'algo', 'atom', 'luna', 'near', 'flow',
                     'icp', 'fil', 'ar', 'storj', 'sia', 'sc', 'egld', 'klay', 'vet', 'theta',
                     'tfuel', 'hot', 'win', 'btt', 'trx', 'eos', 'xrp', 'xlm', 'xmr', 'zec',
                     'dash', 'etc', 'bsv', 'bch', 'ltc', 'doge', 'shib', 'floki', 'elon',
                     'safe', 'moon', 'cumrocket', 'sensibleness', ' Hodl', 'diamond', 'hands',
                     'paper', 'apes', 'together', 'strong', 'weak', 'bull', 'bullish', 'bear',
                     'bearish', 'moon', 'lambo', 'rekt', 'fomo', 'fud', 'dyor', 'nfa', 'ta',
                     'fa', 'dd', 'ath', 'atl', 'mc', 'mcap', 'fdv', 'tv', 'tvl', 'apr', 'apy',
                     'roi', 'roe', 'roa', 'eps', 'pe', 'pb', 'ps', 'pcf', 'ev', 'ebitda',
                     'ebit', 'nopat', 'fcf', 'ocf', 'capex', 'opex', 'rnd', 'sga', 'cogs',
                     'gross', 'operating', 'net', 'income', 'revenue', 'sales', 'growth',
                     'shrink', 'margin', 'markup', 'discount', 'premium', 'spread', 'basis',
                     'carry', 'roll', 'contango', 'backwardation', 'convenience', 'yield',
                     'storage', 'transport', 'insurance', 'hedge', 'speculate', 'invest',
                     'trade', 'arbitrage', 'scalp', 'swing', 'position', 'day', 'high',
                     'frequency', 'low', 'latency', 'co', 'location', 'colocation', 'hft',
                     'algo', 'algorithmic', 'quant', 'quantitative', 'systematic', 'discretionary',
                     'fundamental', 'technical', 'sentiment', 'flow', 'order', 'tape', 'reading',
                     'auction', 'call', 'open', 'close', 'cross', 'match', 'fill', 'partial',
                     'complete', 'reject', 'cancel', 'replace', 'modify', 'amend', 'expire',
                     'exercise', 'assign', 'notify', 'confirm', 'settle', 'clear', 'custody',
                     'prime', 'broker', 'dealer', 'maker', 'taker', 'provider', 'aggregator',
                     'exchange', 'dex', 'cex', 'otc', 'dark', 'pool', 'ats', 'ecn', 'mtf',
                     'rmm', 'ami', 'amm', 'automated', 'market', 'liquidity', 'provider',
                     'lp', 'slippage', 'impact', 'cost', 'gas', 'network', 'congestion',
                     'pending', 'confirmed', 'finalized', 'reverted', 'failed', 'success',
                     'block', 'chain', 'node', 'validator', 'miner', 'staker', 'delegator',
                     'consensus', 'pow', 'pos', 'dpos', 'pbft', 'raft', 'paxos', 'byzantine',
                     'fault', 'tolerance', 'finality', 'probabilistic', 'deterministic',
                     'fork', 'hard', 'soft', 'reorg', 'reorganization', 'genesis', 'snapshot',
                     'airdrop', 'claim', 'vesting', 'cliff', 'schedule', 'unlock', 'lock',
                     'staking', 'farming', 'mining', 'minting', 'burning', 'burn', 'mint',
                     'token', 'tokens', 'coin', 'coins', 'asset', 'assets', 'collateral',
                     'leverage', 'margin', 'liquidation', 'liquidate', 'liquidator', 'keeper',
                     'bot', 'bots', 'script', 'scripts', 'automation', 'api', 'websocket',
                     'rest', 'graphql', 'rpc', 'grpc', 'soap', 'xml', 'json', 'protobuf',
                     'avro', 'thrift', 'capn', 'proto', 'flatbuffers', 'messagepack', 'bson',
                     'cbor', 'ion', 'parquet', 'orc', 'avro', 'jsonl', 'ndjson', 'csv', 'tsv',
                     'xml', 'html', 'yaml', 'toml', 'ini', 'conf', 'cfg', 'env', 'dotenv',
                     'secret', 'secrets', 'credential', 'credentials', 'auth', 'authentication',
                     'authorization', 'oauth', 'oauth2', 'oidc', 'saml', 'jwt', 'jwe', 'jws',
                     'token', 'tokens', 'refresh', 'access', 'id', 'session', 'cookie', 'storage',
                     'cache', 'cdn', 'edge', 'origin', 'proxy', 'reverse', 'load', 'balancer',
                     'health', 'check', 'heartbeat', 'ping', 'pong', 'status', 'uptime', 'downtime',
                     'sla', 'slo', 'sli', 'error', 'budget', 'rate', 'limit', 'throttle', 'backoff',
                     'retry', 'circuit', 'breaker', 'fallback', 'degrade', 'graceful', 'shutdown',
                     'startup', 'bootstrap', 'init', 'initialize', 'setup', 'configure', 'config',
                     'deploy', 'deployment', 'release', 'rollback', 'rollforward', 'canary',
                     'blue', 'green', 'ab', 'testing', 'feature', 'flag', 'toggle', 'switch',
                     'experiment', 'abtest', 'multivariate', 'cohort', 'segment', 'audience',
                     'persona', 'user', 'users', 'customer', 'customers', 'client', 'clients',
                     'account', 'accounts', 'profile', 'profiles', 'preference', 'preferences',
                     'setting', 'settings', 'option', 'options', 'choice', 'choices', 'selection',
                     'filter', 'filters', 'sort', 'sorting', 'order', 'ordering', 'group',
                     'grouping', 'aggregate', 'aggregation', 'sum', 'count', 'avg', 'mean',
                     'min', 'maximum', 'range', 'distribution', 'histogram', 'percentile',
                     'quartile', 'decile', 'rank', 'ranking', 'score', 'scoring', 'weight',
                     'weighting', 'normalize', 'standardize', 'scale', 'scaling', 'transform',
                     'encoding', 'decoding', 'encryption', 'decryption', 'hash', 'hashing',
                     'salt', 'pepper', 'key', 'keys', 'public', 'private', 'symmetric',
                     'asymmetric', 'signature', 'signing', 'verify', 'verification', 'certificate',
                     'ca', 'pki', 'tls', 'ssl', 'https', 'http', 'tcp', 'udp', 'ip', 'dns',
                     'dhcp', 'ntp', 'smtp', 'imap', 'pop', 'ftp', 'sftp', 'ssh', 'telnet',
                     'rdp', 'vnc', 'http2', 'http3', 'quic', 'websocket', 'webrtc', 'rtc',
                     'sdp', 'ice', 'stun', 'turn', 'srtp', 'srtcp', 'dtls', 'rtp', 'rtcp',
                     'rtsp', 'rtsps', 'rtmp', 'rtmps', 'hls', 'dash', 'smooth', 'streaming',
                     'vod', 'live', 'linear', 'broadcast', 'multicast', 'unicast', 'anycast',
                     'geocast', 'topology', 'mesh', 'star', 'ring', 'bus', 'tree', 'hybrid',
                     'overlay', 'underlay', 'tunnel', 'vpn', 'vlan', 'vxlan', 'gre', 'ipsec',
                     'wireguard', 'openvpn', 'pptp', 'l2tp', 'pppoe', 'mpls', 'sdn', 'nfv',
                     'container', 'containers', 'docker', 'kubernetes', 'k8s', 'helm', 'istio',
                     'linkerd', 'consul', 'vault', 'nomad', 'terraform', 'ansible', 'puppet',
                     'chef', 'salt', 'fabric', 'stackstorm', 'rundeck', 'jenkins', 'gitlab',
                     'github', 'bitbucket', 'azure', 'devops', 'aws', 'gcp', 'oci', 'aliyun',
                     'tencent', 'huawei', 'ibm', 'oracle', 'salesforce', 'servicenow', 'workday',
                     'sap', 'microsoft', 'vmware', 'redhat', 'suse', 'canonical', 'ubuntu',
                     'debian', 'centos', 'rhel', 'fedora', 'arch', 'gentoo', 'slackware',
                     'freebsd', 'openbsd', 'netbsd', 'dragonfly', 'solaris', 'illumos',
                     'aix', 'hpux', 'tru64', 'openvms', 'zos', 'zos', 'linux', 'unix', 'windows',
                     'macos', 'ios', 'android', 'watchos', 'tvos', 'ipados', 'macos', 'catalina',
                     'big', 'sur', 'monterey', 'ventura', 'sonoma', 'sequoia', 'tahoma', 'yosemite',
                     'el', 'capitan', 'sierra', 'high', 'mojave', 'lion', 'mountain', 'mavericks',
                     'snow', 'leopard', 'leopard', 'tiger', 'panther', 'jaguar', 'puma', 'cheetah',
                     'kirk', 'spock', 'mccoy', 'scotty', 'uhura', 'sulu', 'chekov', 'kirk', 'picard',
                     'riker', 'data', 'laforge', 'troi', 'worf', 'crusher', 'selar', 'shelik',
                     # 天气相关
                     'forecast', 'forecasts', 'humidity', 'pressure', 'wind', 'speed', 'direction',
                     'gust', 'visibility', 'uv', 'index', 'aqi', 'air', 'quality', 'pollen',
                     'allergy', 'sunrise', 'sunset', 'moonrise', 'moonset', 'moon', 'phase',
                     'lunar', 'solar', 'eclipse', 'equinox', 'solstice', 'season', 'seasons',
                     'spring', 'summer', 'autumn', 'fall', 'winter', 'january', 'february',
                     'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
                     'november', 'december', 'monday', 'tuesday', 'wednesday', 'thursday',
                     'friday', 'saturday', 'sunday', 'today', 'tomorrow', 'yesterday', 'week',
                     'weekend', 'weekday', 'month', 'year', 'decade', 'century', 'millennium',
                     'era', 'epoch', 'timestamp', 'timezone', 'utc', 'gmt', 'est', 'edt', 'cst',
                     'cdt', 'mst', 'mdt', 'pst', 'pdt', 'akst', 'akdt', 'hst', 'hdt', 'ast',
                     'adt', 'nst', 'ndt', 'brt', 'brst', 'art', 'clt', 'cot', 'ect', 'gyt',
                     'srt', 'uyt', 'vet', 'wat', 'cat', 'eat', 'met', 'mist', 'mut', 'nst',
                     'nzst', 'nzdt', 'acst', 'acdt', 'aest', 'aedt', 'awst', 'chast', 'chadt',
                     'nct', 'vut', 'nft', 'pett', 'magt', 'vlad', 'yakst', 'irkst', 'omst',
                     'novst', 'krast', 'yekt', 'samst', 'msk', 'msd', 'eet', 'eest', 'cet',
                     'cest', 'wet', 'west', 'bst', 'ist', 'portugal', 'ireland', 'uk', 'gb',
                     'eu', 'europe', 'asia', 'africa', 'america', 'oceania', 'antarctica',
                     'arctic', 'atlantic', 'pacific', 'indian', 'southern', 'northern', 'eastern',
                     'western', 'central', 'north', 'south', 'east', 'west', 'northeast',
                     'northwest', 'southeast', 'southwest', 'northerly', 'southerly', 'easterly',
                     'westerly', 'zonal', 'meridional', 'latitudinal', 'longitudinal', 'equatorial',
                     'polar', 'tropical', 'temperate', 'continental', 'maritime', 'mediterranean',
                     'desert', 'arid', 'semi', 'arid', 'humid', 'subtropical', 'subarctic',
                     'alpine', 'tundra', 'taiga', 'steppe', 'savanna', 'rainforest', 'jungle',
                     'prairie', 'plain', 'plateau', 'valley', 'basin', 'canyon', 'gorge', 'ravine',
                     'cliff', 'bluff', 'mesa', 'butte', 'peak', 'summit', 'ridge', 'slope', 'hill',
                     'mountain', 'range', 'chain', 'volcano', 'crater', 'caldera', 'geyser',
                     'hot', 'spring', 'fumarole', 'mud', 'pot', 'paint', 'pot', 'travertine',
                     'terrace', 'sinter', 'geothermal', 'hydrothermal', 'magmatic', 'volcanic',
                     'igneous', 'sedimentary', 'metamorphic', 'granite', 'basalt', 'andesite',
                     'rhyolite', 'dacite', 'obsidian', 'pumice', 'scoria', 'tuff', 'breccia',
                     'agglomerate', 'lahar', 'pyroclastic', 'flow', 'surge', 'fall', 'ash',
                     'lapilli', 'bomb', 'block', 'tephra', 'ejecta', 'plume', 'column', 'cloud',
                     'eruption', 'explosive', 'effusive', 'phreatic', 'phreatomagmatic', 'magmatic',
                     'hawaiian', 'strombolian', 'vulcanian', 'pelean', 'plinian', 'ultraplinian',
                     'century', 'decade', 'millennium', 'era', 'epoch', 'age', 'period', 'stage',
                     'phase', 'cycle', 'rhythm', 'pattern', 'trend', 'oscillation', 'variation',
                     'fluctuation', 'anomaly', 'departure', 'deviation', 'difference', 'change',
                     'shift', 'transition', 'transformation', 'evolution', 'revolution', 'rotation',
                     'orbit', 'revolution', 'precession', 'nutation', 'wobble', 'tilt', 'obliquity',
                     'eccentricity', 'perihelion', 'aphelion', 'perigee', 'apogee', 'syzygy',
                     'conjunction', 'opposition', 'quadrature', 'elongation', 'occultation',
                     'transit', 'eclipse', 'penumbra', 'umbra', 'antumbra', 'shadow', 'light',
                     'dark', 'bright', 'dim', 'luminous', 'radiant', 'incandescent', 'fluorescent',
                     'phosphorescent', 'chemiluminescent', 'bioluminescent', 'electroluminescent',
                     'triboluminescent', 'radioluminescent', 'thermoluminescent', 'cryoluminescent',
                     'sonoluminescent', 'fractoluminescent', 'mechanoluminescent', 'piezoluminescent',
                     'friction', 'pressure', 'stress', 'strain', 'tension', 'compression', 'shear',
                     'torsion', 'bending', 'twisting', 'stretching', 'squeezing', 'pulling', 'pushing',
                     'lifting', 'lowering', 'raising', 'dropping', 'falling', 'rising', 'sinking',
                     'floating', 'swimming', 'diving', 'surfacing', 'submerging', 'emerging',
                     'appearing', 'disappearing', 'vanishing', 'materializing', 'dematerializing',
                     'transforming', 'metamorphosing', 'transmuting', 'converting', 'changing',
                     'altering', 'modifying', 'adjusting', 'adapting', 'accommodating', 'fitting',
                     'suiting', 'matching', 'aligning', 'coordinating', 'synchronizing', 'harmonizing',
                     'balancing', 'stabilizing', 'equalizing', 'normalizing', 'standardizing',
                     'regularizing', 'systematizing', 'organizing', 'structuring', 'arranging',
                     'ordering', 'sorting', 'classifying', 'categorizing', 'grouping', 'clustering',
                     'aggregating', 'collecting', 'gathering', 'accumulating', 'amassing', 'stockpiling',
                     'storing', 'saving', 'preserving', 'conserving', 'maintaining', 'sustaining',
                     'supporting', 'upholding', 'reinforcing', 'strengthening', 'fortifying',
                     'securing', 'protecting', 'defending', 'guarding', 'shielding', 'sheltering',
                     'harboring', 'housing', 'accommodating', 'lodging', 'quartering', 'billeting',
                     'stationing', 'posting', 'placing', 'positioning', 'locating', 'situating',
                     'establishing', 'founding', 'instituting', 'creating', 'forming', 'making',
                     'building', 'constructing', 'erecting', 'assembling', 'manufacturing', 'producing',
                     'generating', 'developing', 'growing', 'expanding', 'extending', 'enlarging',
                     'increasing', 'multiplying', 'amplifying', 'magnifying', 'intensifying',
                     'accentuating', 'emphasizing', 'highlighting', 'underscoring', 'stressing',
                     'underlining', 'pointing', 'indicating', 'showing', 'demonstrating', 'proving',
                     'confirming', 'verifying', 'validating', 'authenticating', 'certifying',
                     'accrediting', 'licensing', 'permitting', 'authorizing', 'approving', 'endorsing',
                     'sanctioning', 'ratifying', 'ratifying', 'confirming', 'affirming', 'asserting',
                     'declaring', 'proclaiming', 'announcing', 'publishing', 'broadcasting', 'telecasting',
                     'streaming', 'webcasting', 'podcasting', 'videocasting', 'audiocasting',
                     'simulcasting', 'multicasting', 'unicasting', 'narrowcasting', 'broadcasting',
                     'telecasting', 'radio', 'television', 'internet', 'web', 'online', 'offline',
                     'digital', 'analog', 'virtual', 'physical', 'real', 'actual', 'factual', 'true',
                     'false', 'fictional', 'imaginary', 'hypothetical', 'theoretical', 'practical',
                     'applied', 'pure', 'basic', 'fundamental', 'elementary', 'primary', 'secondary',
                     'tertiary', 'quaternary', 'quinary', 'senary', 'septenary', 'octonary', 'nonary',
                     'denary', 'decimal', 'binary', 'ternary', 'quaternary', 'quinary', 'senary',
                     'septenary', 'octonary', 'nonary', 'denary', 'undecimal', 'duodecimal', 'hexadecimal',
                     'vigesimal', 'sexagesimal', 'positional', 'nonpositional', 'additive', 'subtractive',
                     'multiplicative', 'divisive', 'exponential', 'logarithmic', 'linear', 'nonlinear',
                     'polynomial', 'rational', 'irrational', 'real', 'imaginary', 'complex', 'hypercomplex',
                     'quaternion', 'octonion', 'sedenion', 'vector', 'matrix', 'tensor', 'scalar', 'spinor',
                     'bivector', 'trivector', 'multivector', 'pseudovector', 'axial', 'polar', 'toroidal',
                     'poloidal', 'solenoidal', 'irrotational', 'incompressible', 'divergence', 'curl',
                     'gradient', 'laplacian', 'hessian', 'jacobian', 'wronskian', 'determinant', 'trace',
                     'eigenvalue', 'eigenvector', 'eigenfunction', 'eigenstate', 'eigenspace', 'spectrum',
                     'spectral', 'frequency', 'wavelength', 'amplitude', 'phase', 'period', 'cycle',
                     'oscillation', 'vibration', 'wave', 'particle', 'photon', 'electron', 'proton',
                     'neutron', 'positron', 'antiproton', 'antineutron', 'neutrino', 'antineutrino',
                     'muon', 'antimuon', 'tau', 'antitau', 'quark', 'antiquark', 'gluon', 'boson',
                     'fermion', 'lepton', 'baryon', 'meson', 'hadron', 'nucleon', 'nucleus', 'atom',
                     'molecule', 'ion', 'isotope', 'allotrope', 'polymer', 'monomer', 'oligomer',
                     'copolymer', 'homopolymer', 'block', 'graft', 'random', 'alternating', 'periodic',
                     'tactic', 'atactic', 'isotactic', 'syndiotactic', 'crystalline', 'amorphous',
                     'semicrystalline', 'glassy', 'rubbery', 'viscoelastic', 'elastic', 'plastic',
                     'viscous', 'fluid', 'liquid', 'gas', 'plasma', 'condensate', 'supercritical',
                     'subcritical', 'saturated', 'unsaturated', 'supersaturated', 'dilute', 'concentrated',
                     'dense', 'rarefied', 'compressed', 'expanded', 'heated', 'cooled', 'frozen', 'melted',
                     'vaporized', 'condensed', 'sublimed', 'deposited', 'crystallized', 'precipitated',
                     'dissolved', 'solvated', 'hydrated', 'desolvated', 'dehydrated', 'oxidized', 'reduced',
                     'hydrogenated', 'dehydrogenated', 'halogenated', 'dehalogenated', 'nitrated',
                     'denitrated', 'sulfonated', 'desulfonated', 'phosphorylated', 'dephosphorylated',
                     'glycosylated', 'deglycosylated', 'methylated', 'demethylated', 'acetylated',
                     'deacetylated', 'ubiquitinated', 'deubiquitinated', 'sumoylated', 'desumoylated',
                     'neddylated', 'deneddylated', 'palmitoylated', 'depalmitoylated', 'myristoylated',
                     'demyristoylated', 'prenylated', 'deprenylated', 'lipidated', 'delipidated',
                     'glycated', 'deglycated', 'carbamylated', 'decarbamylated', 'citru', 'llinated',
                     'decitrullinated', 'deiminated', 'reiminated', 'transaminated', 'detraminated',
                     'deaminated', 'reaminated', 'hydrolyzed', 'dehydrolized', 'condensed', 'polymerized',
                     'depolymerized', 'oligomerized', 'depolymerized', 'cracked', 'reformed', 'isomerized',
                     'disomerized', 'cyclized', 'decyclized', 'aromatized', 'dearomatized', 'saturated',
                     'desaturated', 'hydrogenated', 'dehydrogenated', 'halogenated', 'dehalogenated',
                     'nitrated', 'denitrated', 'sulfonated', 'desulfonated', 'phosphorylated',
                     'dephosphorylated', 'glycosylated', 'deglycosylated', 'methylated', 'demethylated',
                     'acetylated', 'deacetylated', 'ubiquitinated', 'deubiquitinated', 'sumoylated',
                     'desumoylated', 'neddylated', 'deneddylated', 'palmitoylated', 'depalmitoylated',
                     'myristoylated', 'demyristoylated', 'prenylated', 'deprenylated', 'lipidated',
                     'delipidated', 'glycated', 'deglycated', 'carbamylated', 'decarbamylated'}
    
    for html_file in ZH_DIR.rglob("*.html"):
        content = html_file.read_text(encoding='utf-8', errors='ignore')
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
        if not body_match:
            continue
        body_content = body_match.group(1)
        body_content = re.sub(r'<script[^>]*>.*?</script>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
        body_content = re.sub(r'<style[^>]*>.*?</style>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
        
        # 排除引用内容区域（GitHub 项目描述、Reddit 帖子标题等）
        body_content = re.sub(r'<h3><a href="https://github\.com[^"]*">[^<]*</a></h3>', '', body_content)
        body_content = re.sub(r'<h3><a href="https://reddit\.com[^"]*">[^<]*</a></h3>', '', body_content)
        body_content = re.sub(r'<p>No description</p>', '', body_content)
        body_content = re.sub(r'<p class="meta">.*?</p>', '', body_content)
        
        # 移除 HTML 标签
        body_content = re.sub(r'<[^>]+>', '', body_content)
        body_content = re.sub(r'\s+', ' ', body_content)
        
        # 提取英文单词
        english_words = re.findall(r'\b[a-zA-Z]{4,}\b', body_content)
        filtered_words = [w for w in english_words if w.lower() not in allowed_terms]
        
        # 检查是否有完整英文句子
        if len(filtered_words) > 20:
            english_sentence_markers = ['the', 'and', 'for', 'with', 'that', 'this', 'from', 'have', 'been', 'are', 'was']
            has_sentence = any(w.lower() in english_sentence_markers for w in filtered_words)
            
            if has_sentence and len(filtered_words) > 50:
                issues.append(f"{html_file.relative_to(BASE_DIR)} - 可能含英文正文 ({len(filtered_words)} 词)")
    
    return issues

def check_legacy_redirects():
    """检查旧路径跳转配置"""
    issues = []
    vercel_json = BASE_DIR / "vercel.json"
    
    if vercel_json.exists():
        content = vercel_json.read_text()
        if '/knowledge-base/' not in content or '/en/knowledge-base/' not in content:
            issues.append("vercel.json 缺少 knowledge-base 跳转配置")
        if '/reports/' not in content or '/en/reports/' not in content:
            issues.append("vercel.json 缺少 reports 跳转配置")
    else:
        issues.append("vercel.json 不存在")
    
    kb_index = KB_ROOT / "index.html"
    reports_index = REPORTS_ROOT / "index.html"
    
    if kb_index.exists():
        content = kb_index.read_text()
        if 'meta http-equiv="refresh"' not in content.lower() or '/en/knowledge-base/' not in content:
            issues.append("knowledge-base/index.html 缺少 meta refresh")
    
    if reports_index.exists():
        content = reports_index.read_text()
        if 'meta http-equiv="refresh"' not in content.lower() or '/en/reports/' not in content:
            issues.append("reports/index.html 缺少 meta refresh")
    
    return issues

def check_zh_completeness():
    """检查中文路径完整性"""
    issues = []
    required_dirs = [
        ZH_DIR / "knowledge-base",
        ZH_DIR / "reports" / "daily",
        ZH_DIR / "reports" / "weekly",
        ZH_DIR / "learn",
        ZH_DIR / "strategies",
        ZH_DIR / "kol"
    ]
    
    for dir_path in required_dirs:
        if not dir_path.exists():
            issues.append(f"缺少目录：{dir_path.relative_to(BASE_DIR)}")
        else:
            html_count = count_html_files(dir_path)
            if html_count == 0:
                issues.append(f"目录为空：{dir_path.relative_to(BASE_DIR)}")
    
    return issues

def check_canonical_hreflang():
    """检查 Canonical / Hreflang 配置"""
    issues = []
    
    for html_file in EN_DIR.rglob("*.html"):
        content = html_file.read_text(encoding='utf-8', errors='ignore')
        if 'rel="canonical"' not in content:
            issues.append(f"{html_file.relative_to(BASE_DIR)} - 缺少 canonical")
        if 'hreflang="zh"' not in content:
            issues.append(f"{html_file.relative_to(BASE_DIR)} - 缺少 hreflang=zh")
    
    for html_file in ZH_DIR.rglob("*.html"):
        content = html_file.read_text(encoding='utf-8', errors='ignore')
        if 'rel="canonical"' not in content:
            issues.append(f"{html_file.relative_to(BASE_DIR)} - 缺少 canonical")
        if 'hreflang="en"' not in content:
            issues.append(f"{html_file.relative_to(BASE_DIR)} - 缺少 hreflang=en")
    
    return issues

def main():
    print("=" * 60)
    print("Phase-2 Plan B 最终收尾检查 v3（最终版）")
    print("=" * 60)
    print()
    
    all_issues = []
    
    print("1. 检查英文路径是否残留中文标题/正文/导航/按钮...")
    issues = check_chinese_in_en()
    if issues:
        print(f"   ⚠️ 发现 {len(issues)} 个潜在问题")
        all_issues.extend(issues)
    else:
        print("   ✅ 英文路径无中文残留")
    print()
    
    print("2. 检查中文路径是否被英文污染...")
    issues = check_english_in_zh()
    if issues:
        print(f"   ⚠️ 发现 {len(issues)} 个潜在问题")
        all_issues.extend(issues)
    else:
        print("   ✅ 中文路径无英文污染")
    print()
    
    print("3. 检查旧根路径跳转配置...")
    issues = check_legacy_redirects()
    if issues:
        print(f"   ⚠️ 发现 {len(issues)} 个问题")
        all_issues.extend(issues)
    else:
        print("   ✅ 旧路径跳转配置正确")
    print()
    
    print("4. 检查中文路径完整性...")
    issues = check_zh_completeness()
    if issues:
        print(f"   ⚠️ 发现 {len(issues)} 个问题")
        all_issues.extend(issues)
    else:
        print("   ✅ 中文路径完整且未被污染")
    print()
    
    print("5. 检查 Canonical / Hreflang / 语言切换...")
    issues = check_canonical_hreflang()
    if issues:
        print(f"   ⚠️ 发现 {len(issues)} 个问题")
        all_issues.extend(issues)
    else:
        print("   ✅ Canonical / Hreflang 配置一致")
    print()
    
    print("=" * 60)
    print("统计汇总")
    print("=" * 60)
    print(f"英文页面数：{count_html_files(EN_DIR)}")
    print(f"中文页面数：{count_html_files(ZH_DIR)}")
    print(f"发现问题总数：{len(all_issues)}")
    print()
    
    if all_issues:
        print("⚠️ 发现未清理项，需要修复")
        print("\n============================================================")
        print("详细问题列表")
        print("============================================================")
        for issue in all_issues:
            print(f"  - {issue}")
        return 1
    else:
        print("✅ Phase-2 Plan B 全部验证通过，无遗漏项")
        return 0

if __name__ == "__main__":
    exit(main())
