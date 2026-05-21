import os
import sys
import asyncio
import aiohttp
import random
from typing import List, Optional, Tuple
from eth_account import Account
from aiohttp_socks import ProxyConnector
from colorama import init, Fore, Style

init(autoreset=True)

BORDER_WIDTH = 80
BASE_URL     = "https://inception.dachain.io"

CONFIG = {
    "THREADS":        5,
    "RETRY_ATTEMPTS": 3,
    "RETRY_DELAY":    5,
    "TIMEOUT":        60,
    "DELAY_BETWEEN":  3,
    "TASK_DELAY":     2,
    "REFERRAL_CODE":  "DAC12841",
}

HEADERS_BASE = {
    "User-Agent":         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
    "Accept":             "*/*",
    "Accept-Language":    "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
    "Accept-Encoding":    "gzip, deflate, br, zstd",
    "Content-Type":       "application/json",
    "Origin":             "https://inception.dachain.io",
    "Sec-Ch-Ua":          '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
    "Sec-Ch-Ua-Mobile":   "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest":     "empty",
    "Sec-Fetch-Mode":     "cors",
    "Sec-Fetch-Site":     "same-origin",
}

LANG = {
    'vi': {
        'title':            'DACHAIN INCEPTION - 30 DAYS OF INCEPTION BADGE',
        'found_wallets':    'Tìm thấy {count} ví trong pvkey.txt',
        'found_proxies':    'Tìm thấy {count} proxy',
        'no_proxies':       'Không có proxy, chạy trực tiếp',
        'processing':       '⚙ ĐANG XỬ LÝ {count} VÍ',
        'pausing':          'Tạm dừng',
        'completed':        '✅ HOÀN THÀNH: {ok}/{total} VÍ | TỔNG NHÂN: x{mul}',
        'pvkey_not_found':  '❌ Không tìm thấy pvkey.txt',
        'pvkey_empty':      '❌ Không có private key hợp lệ',
        'invalid_key':      'Dòng {i}: không hợp lệ, bỏ qua',
        'no_proxy':         'Không có proxy',
        'unknown_ip':       'Không xác định',
        'proxy_line':       '🔄 Proxy: [{proxy}] | IP: [{ip}]',
        'wallet_label':     'Ví',
        'retry':            'Retry {cur}/{max}...',
        'max_retry':        'Hết số lần thử',
        'csrf_req':         'Đang lấy CSRF token...',
        'csrf_ok':          'CSRF token đã lấy thành công!',
        'csrf_fail':        'Lấy CSRF thất bại',
        'login_req':        'Đang đăng nhập vào Dachain...',
        'login_ok':         'Đăng nhập thành công! ID: {uid}',
        'login_wallet':     '- Wallet:      {addr}',
        'login_qe':         '- QE Balance:  {qe}',
        'login_fail':       'Đăng nhập thất bại',
        'profile_req':      'Đang lấy profile...',
        'profile_ok':       'Profile lấy thành công!',
        'profile_fail':     'Lấy profile thất bại',
        'profile_balance':  '- Balance QE: {qe} | Balance DACC: {dacc}',
        'profile_streak':   '- Streak: {v}',
        'profile_rank':     '- Rank: {v}',
        'profile_tx':       '- TX: {v}',
        'profile_wallet':   '- Wallet: {addr}',
        'flash_claiming':   'Đang claim Flash Badge (30 Days of Inception)...',
        'flash_ok':         'Claim thành công! Nhân: x{mul} QE | Hết hạn: {exp} | Trạng thái: {state}',
        'flash_already':    'Flash Badge đã được claim (state: {state})',
        'flash_fail':       'Claim Flash Badge thất bại',
        'summary_header':   '📊 Tóm tắt:',
        'summary_wallet':   '- Wallet:      {v}',
        'summary_username': '- Username:    {v}',
        'summary_qe':       '- QE Balance:  {qe}  |  DACC: {dacc}',
        'summary_flash':    '- Flash Badge: {v}',
        'success_line':     '✅ Thành công | Ví: {addr} | Nhân: x{mul} | Hết hạn: {exp}',
        'already_line':     'ℹ Đã claim | Ví: {addr} | State: {state}',
        'err_runtime':      'Lỗi: {e}',
    },
    'en': {
        'title':            'DACHAIN INCEPTION - 30 DAYS OF INCEPTION BADGE',
        'found_wallets':    'Found {count} wallets in pvkey.txt',
        'found_proxies':    'Found {count} proxies',
        'no_proxies':       'No proxies, running direct',
        'processing':       '⚙ PROCESSING {count} WALLETS',
        'pausing':          'Pausing',
        'completed':        '✅ COMPLETED: {ok}/{total} WALLETS | TOTAL MULTIPLIER: x{mul}',
        'pvkey_not_found':  '❌ pvkey.txt not found',
        'pvkey_empty':      '❌ No valid private keys',
        'invalid_key':      'Line {i}: invalid key, skipped',
        'no_proxy':         'No proxy',
        'unknown_ip':       'Unknown',
        'proxy_line':       '🔄 Proxy: [{proxy}] | IP: [{ip}]',
        'wallet_label':     'Wallet',
        'retry':            'Retry {cur}/{max}...',
        'max_retry':        'Max retries reached',
        'csrf_req':         'Fetching CSRF token...',
        'csrf_ok':          'CSRF token acquired!',
        'csrf_fail':        'Failed to get CSRF',
        'login_req':        'Logging into Dachain...',
        'login_ok':         'Login successful! ID: {uid}',
        'login_wallet':     '- Wallet:      {addr}',
        'login_qe':         '- QE Balance:  {qe}',
        'login_fail':       'Login failed',
        'profile_req':      'Fetching profile...',
        'profile_ok':       'Profile fetched successfully!',
        'profile_fail':     'Failed to fetch profile',
        'profile_balance':  '- Balance QE: {qe} | Balance DACC: {dacc}',
        'profile_streak':   '- Streak: {v}',
        'profile_rank':     '- Rank: {v}',
        'profile_tx':       '- TX: {v}',
        'profile_wallet':   '- Wallet: {addr}',
        'flash_claiming':   'Claiming Flash Badge (30 Days of Inception)...',
        'flash_ok':         'Claimed! Multiplier: x{mul} QE | Expires: {exp} | State: {state}',
        'flash_already':    'Flash Badge already claimed (state: {state})',
        'flash_fail':       'Flash Badge claim failed',
        'summary_header':   '📊 Summary:',
        'summary_wallet':   '- Wallet:      {v}',
        'summary_username': '- Username:    {v}',
        'summary_qe':       '- QE Balance:  {qe}  |  DACC: {dacc}',
        'summary_flash':    '- Flash Badge: {v}',
        'success_line':     '✅ Success | Wallet: {addr} | Multiplier: x{mul} | Expires: {exp}',
        'already_line':     'ℹ Already claimed | Wallet: {addr} | State: {state}',
        'err_runtime':      'Error: {e}',
    },
}

def print_border(text: str, color=Fore.CYAN, width=BORDER_WIDTH):
    text = text.strip()
    if len(text) > width - 4:
        text = text[:width - 7] + "..."
    padded = f" {text} ".center(width - 2)
    print(f"{color}┌{'─' * (width - 2)}┐{Style.RESET_ALL}")
    print(f"{color}│{padded}│{Style.RESET_ALL}")
    print(f"{color}└{'─' * (width - 2)}┘{Style.RESET_ALL}")

def print_separator(color=Fore.MAGENTA):
    print(f"{color}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")

def p(icon: str, text: str, color=Fore.CYAN):
    print(f"{color}  {icon} {text}{Style.RESET_ALL}")

def load_private_keys() -> List[Tuple[int, str]]:
    fp = "pvkey.txt"
    if not os.path.exists(fp):
        p("✖", LANG['pvkey_not_found'], Fore.RED)
        with open(fp, 'w') as f:
            f.write("# Mỗi dòng một private key\n")
        sys.exit(1)
    keys = []
    with open(fp) as f:
        for i, line in enumerate(f, 1):
            k = line.strip()
            if not k or k.startswith('#'):
                continue
            if not k.startswith('0x'):
                k = '0x' + k
            try:
                Account.from_key(k)
                keys.append((i, k))
            except Exception:
                p("⚠", LANG['invalid_key'].format(i=i), Fore.YELLOW)
    if not keys:
        p("✖", LANG['pvkey_empty'], Fore.RED)
        sys.exit(1)
    return keys

def load_proxies() -> List[str]:
    if not os.path.exists("proxies.txt"):
        return []
    return [l.strip() for l in open("proxies.txt") if l.strip() and not l.startswith('#')]

def parse_proxy(proxy: Optional[str]) -> Optional[str]:
    if not proxy:
        return None
    proxy = proxy.strip()
    if proxy.startswith(("http://", "https://", "socks4://", "socks5://")):
        return proxy
    parts = proxy.split(":")
    if len(parts) == 4:
        host, port, user, pwd = parts
        return f"http://{user}:{pwd}@{host}:{port}"
    if len(parts) == 2:
        return f"http://{parts[0]}:{parts[1]}"
    return f"http://{proxy}"

def make_connector(proxy_url: Optional[str]):
    if not proxy_url:
        return aiohttp.TCPConnector(ssl=False)
    if proxy_url.startswith("socks"):
        return ProxyConnector.from_url(proxy_url, ssl=False)
    return aiohttp.TCPConnector(ssl=False)

def proxy_kwargs(proxy_url: Optional[str]) -> dict:
    if not proxy_url or proxy_url.startswith("socks"):
        return {}
    return {"proxy": proxy_url}

async def get_proxy_ip(proxy_url: Optional[str]) -> str:
    try:
        connector = make_connector(proxy_url)
        kw        = proxy_kwargs(proxy_url)
        timeout   = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as s:
            async with s.get("https://api.ipify.org?format=json", **kw) as r:
                data = await r.json()
                return data.get("ip", LANG['unknown_ip'])
    except Exception:
        return LANG['unknown_ip']

class DaChainClient:
    def __init__(self, session: aiohttp.ClientSession, proxy_url: Optional[str], wallet_address: str):
        self.session        = session
        self.kw             = proxy_kwargs(proxy_url)
        self.wallet         = wallet_address
        self.csrf           = None
        self.session_cookie = None

    def _h(self, referer: str = "/") -> dict:
        h = {**HEADERS_BASE, "Referer": f"{BASE_URL}{referer}"}
        if self.csrf:
            h["x-csrftoken"] = self.csrf
        cookies = f"ref_code={CONFIG['REFERRAL_CODE']}"
        if self.csrf:
            cookies += f"; csrftoken={self.csrf}"
        if self.session_cookie:
            cookies += f"; sessionid={self.session_cookie}"
        h["Cookie"] = cookies
        return h

    async def get_csrf(self) -> bool:
        try:
            async with self.session.get(
                f"{BASE_URL}/csrf/",
                headers={**HEADERS_BASE, "Cookie": f"ref_code={CONFIG['REFERRAL_CODE']}"},
                **self.kw
            ) as r:
                if r.status == 200:
                    for c in r.cookies.values():
                        if c.key == "csrftoken":
                            self.csrf = c.value
                            return True
                    for c in self.session.cookie_jar:
                        if c.key == "csrftoken":
                            self.csrf = c.value
                            return True
                return False
        except Exception:
            return False

    async def wallet_login(self) -> Optional[dict]:
        try:
            async with self.session.post(
                f"{BASE_URL}/api/auth/wallet/",
                json={"wallet_address": self.wallet},
                headers=self._h("/"),
                **self.kw
            ) as r:
                if r.status == 200:
                    data = await r.json()
                    for c in r.cookies.values():
                        if c.key == "sessionid":
                            self.session_cookie = c.value
                    if not self.session_cookie:
                        for c in self.session.cookie_jar:
                            if c.key == "sessionid":
                                self.session_cookie = c.value
                    return data
                return None
        except Exception:
            return None

    async def get_profile(self) -> Optional[dict]:
        try:
            async with self.session.get(
                f"{BASE_URL}/api/inception/profile/",
                headers=self._h("/"),
                **self.kw
            ) as r:
                return await r.json() if r.status == 200 else None
        except Exception:
            return None

    async def claim_flash_badge(self) -> Tuple[Optional[dict], int]:
        """Claim the 30 Days of Inception flash badge."""
        try:
            async with self.session.post(
                f"{BASE_URL}/api/inception/flash-badge/claim/",
                data=b"",
                headers={**self._h("/dashboard"), "Content-Length": "0"},
                **self.kw
            ) as r:
                body = await r.json() if r.status in (200, 400, 429) else None
                return body, r.status
        except Exception:
            return None, 0

def fmt_expiry(iso: Optional[str]) -> str:
    """Shorten ISO timestamp to readable form."""
    if not iso:
        return "-"
    try:
        return iso[:16].replace("T", " ") + " UTC"
    except Exception:
        return iso

async def process_wallet(index: int, private_key: str, proxy: Optional[str]) -> Tuple[int, float]:
    account   = Account.from_key(private_key)
    address   = account.address
    short     = f"{address[:6]}...{address[-4:]}"
    proxy_url = parse_proxy(proxy)
    proxy_str = proxy or LANG['no_proxy']

    print_border(f"{LANG['wallet_label']} {index}: {short}", Fore.YELLOW)

    ip = await get_proxy_ip(proxy_url)
    print(f"{Fore.CYAN}  {LANG['proxy_line'].format(proxy=proxy_str, ip=ip)}{Style.RESET_ALL}")
    print()

    timeout = aiohttp.ClientTimeout(total=CONFIG['TIMEOUT'])

    try:
        connector = make_connector(proxy_url)
        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            cookie_jar=aiohttp.CookieJar(unsafe=True)
        ) as session:

            for attempt in range(CONFIG['RETRY_ATTEMPTS']):
                if attempt > 0:
                    p("ℹ", LANG['retry'].format(cur=attempt, max=CONFIG['RETRY_ATTEMPTS'] - 1), Fore.YELLOW)
                    await asyncio.sleep(CONFIG['RETRY_DELAY'])

                dac = DaChainClient(session, proxy_url, address)

                p(">", LANG['csrf_req'], Fore.CYAN)
                if not await dac.get_csrf():
                    p("✖", LANG['csrf_fail'], Fore.RED)
                    continue
                p("✓", LANG['csrf_ok'], Fore.GREEN)
                await asyncio.sleep(random.uniform(0.5, 1.0))

                p(">", LANG['login_req'], Fore.CYAN)
                login_res = await dac.wallet_login()
                if not login_res or not login_res.get('success'):
                    p("✖", LANG['login_fail'], Fore.RED)
                    continue
                user_data    = login_res.get('user', {})
                user_id      = user_data.get('id', '-')
                login_qe_val = user_data.get('qe_balance', 0)
                p("✓", LANG['login_ok'].format(uid=user_id), Fore.GREEN)
                print(f"{Fore.WHITE}     {LANG['login_wallet'].format(addr=f'{Fore.YELLOW}{address}{Style.RESET_ALL}')}")
                print(f"{Fore.WHITE}     {LANG['login_qe'].format(qe=f'{Fore.CYAN}{login_qe_val}{Style.RESET_ALL}')}")
                print()
                await asyncio.sleep(random.uniform(0.8, 1.5))

                p(">", LANG['profile_req'], Fore.CYAN)
                profile = await dac.get_profile()
                if not profile:
                    p("✖", LANG['profile_fail'], Fore.RED)
                    continue
                username   = profile.get('username', '-')
                qe_balance = profile.get('qe_balance', 0)
                dacc_bal   = profile.get('dacc_balance', '0.000000')
                streak     = profile.get('streak_days', 0)
                user_rank  = profile.get('user_rank', '-')
                tx_count   = profile.get('tx_count', 0)

                p("✓", LANG['profile_ok'], Fore.GREEN)
                print(f"{Fore.WHITE}  {LANG['profile_balance'].format(qe=f'{Fore.CYAN}{qe_balance}{Fore.WHITE}', dacc=f'{Fore.CYAN}{dacc_bal}{Style.RESET_ALL}')}")
                print(f"{Fore.WHITE}  {LANG['profile_streak'].format(v=f'{Fore.CYAN}{streak}{Style.RESET_ALL}')}")
                print(f"{Fore.WHITE}  {LANG['profile_rank'].format(v=f'{Fore.CYAN}{user_rank}{Style.RESET_ALL}')}")
                print(f"{Fore.WHITE}  {LANG['profile_tx'].format(v=f'{Fore.CYAN}{tx_count}{Style.RESET_ALL}')}")
                print(f"{Fore.WHITE}  {LANG['profile_wallet'].format(addr=f'{Fore.YELLOW}{address}{Style.RESET_ALL}')}")
                print()
                await asyncio.sleep(random.uniform(0.5, 1.0))

                label = "── 30 DAYS OF INCEPTION BADGE ──"
                print(f"{Fore.YELLOW}┌─ {label} {'─' * (BORDER_WIDTH - len(label) - 4)}{Style.RESET_ALL}")

                print(f"{Fore.YELLOW}│{Style.RESET_ALL}  {Fore.CYAN}> {LANG['flash_claiming']}{Style.RESET_ALL}")
                await asyncio.sleep(random.uniform(CONFIG['TASK_DELAY'], CONFIG['TASK_DELAY'] + 1))
                res, status_code = await dac.claim_flash_badge()

                flash_done  = 0
                multiplier  = 0.0
                expiry_str  = "-"
                state_str   = "-"

                if res is None and status_code == 0:
                    print(f"{Fore.YELLOW}│{Style.RESET_ALL}  {Fore.RED}✖ {LANG['flash_fail']}{Style.RESET_ALL}")

                elif res and res.get('success'):
                    fb         = res.get('flash_badge', {})
                    state_str  = fb.get('state', 'claimed_active')
                    multiplier = fb.get('multiplier', 0.0)
                    expiry_str = fmt_expiry(fb.get('multiplier_expires_at'))
                    msg = LANG['flash_ok'].format(
                        mul=multiplier,
                        exp=expiry_str,
                        state=state_str
                    )
                    print(f"{Fore.YELLOW}│{Style.RESET_ALL}  {Fore.GREEN}✓ {msg}{Style.RESET_ALL}")
                    flash_done = 1

                elif status_code in (400, 429):
                    fb         = (res or {}).get('flash_badge', {})
                    state_str  = fb.get('state', 'already_claimed') if fb else 'already_claimed'
                    multiplier = fb.get('multiplier', 0.0) if fb else 0.0
                    expiry_str = fmt_expiry(fb.get('multiplier_expires_at')) if fb else "-"
                    msg = LANG['flash_already'].format(state=state_str)
                    print(f"{Fore.YELLOW}│{Style.RESET_ALL}  {Fore.YELLOW}ℹ {msg}{Style.RESET_ALL}")

                else:
                    print(f"{Fore.YELLOW}│{Style.RESET_ALL}  {Fore.RED}✖ {LANG['flash_fail']}{Style.RESET_ALL}")

                print(f"{Fore.YELLOW}└{'─' * (BORDER_WIDTH - 2)}{Style.RESET_ALL}")
                print()

                final      = await dac.get_profile()
                final_qe   = final.get('qe_balance', qe_balance) if final else qe_balance
                final_dacc = final.get('dacc_balance', dacc_bal)  if final else dacc_bal

                print(f"{Fore.WHITE}  {'─' * 50}{Style.RESET_ALL}")
                print(f"{Fore.WHITE}  {LANG['summary_header']}{Style.RESET_ALL}")
                print(f"{Fore.WHITE}     {LANG['summary_wallet'].format(v=f'{Fore.YELLOW}{short}{Style.RESET_ALL}')}")
                print(f"{Fore.WHITE}     {LANG['summary_username'].format(v=f'{Fore.YELLOW}{username}{Style.RESET_ALL}')}")
                print(f"{Fore.WHITE}     {LANG['summary_qe'].format(qe=f'{Fore.CYAN}{final_qe}{Fore.WHITE}', dacc=f'{Fore.CYAN}{final_dacc}{Style.RESET_ALL}')}")
                if flash_done:
                    badge_info = f"x{multiplier} QE Multiplier | Expires: {expiry_str}"
                    print(f"{Fore.WHITE}     {LANG['summary_flash'].format(v=f'{Fore.GREEN}{badge_info}{Style.RESET_ALL}')}")
                print(f"{Fore.WHITE}  {'─' * 50}{Style.RESET_ALL}")
                print()

                if flash_done:
                    print(f"{Fore.GREEN}  {LANG['success_line'].format(addr=short, mul=multiplier, exp=expiry_str)}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}  {LANG['already_line'].format(addr=short, state=state_str)}{Style.RESET_ALL}")
                print()

                return flash_done, multiplier

            p("✖", LANG['max_retry'], Fore.RED)
            return 0, 0.0

    except Exception as e:
        import traceback
        p("✖", LANG['err_runtime'].format(e=e), Fore.RED)
        print(f"{Fore.RED}{traceback.format_exc()}{Style.RESET_ALL}")
        return 0, 0.0

async def run_flash_badge(language: str = 'vi'):
    global LANG
    LANG = LANG[language]
    print()
    print_border(LANG['title'], Fore.YELLOW)
    print()

    private_keys = load_private_keys()
    p("ℹ", LANG['found_wallets'].format(count=len(private_keys)), Fore.YELLOW)

    proxies = load_proxies()
    if proxies:
        p("ℹ", LANG['found_proxies'].format(count=len(proxies)), Fore.YELLOW)
    else:
        p("ℹ", LANG['no_proxies'], Fore.YELLOW)

    print()
    print_separator()
    print_border(LANG['processing'].format(count=len(private_keys)), Fore.MAGENTA)
    print()

    total       = len(private_keys)
    accs_ok     = 0
    total_mul   = 0.0
    sema        = asyncio.Semaphore(CONFIG['THREADS'])

    async def run_one(i: int, pnum: int, key: str):
        nonlocal accs_ok, total_mul
        proxy = proxies[i % len(proxies)] if proxies else None
        async with sema:
            done, mul = await process_wallet(pnum, key, proxy)
            if done > 0:
                accs_ok   += 1
                total_mul += mul
            if i < total - 1:
                delay = CONFIG['DELAY_BETWEEN']
                p("ℹ", f"{LANG['pausing']} {delay}s...", Fore.YELLOW)
                await asyncio.sleep(delay)

    await asyncio.gather(
        *[run_one(i, pnum, key) for i, (pnum, key) in enumerate(private_keys)],
        return_exceptions=True
    )

    print()
    print_separator()
    print_border(LANG['completed'].format(ok=accs_ok, total=total, mul=total_mul), Fore.GREEN)
    print()

if __name__ == "__main__":
    asyncio.run(run_flash_badge('vi'))
