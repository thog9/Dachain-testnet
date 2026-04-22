import os
import sys
import asyncio
from colorama import init, Fore, Style
import inquirer

init(autoreset=True)

BORDER_WIDTH = 80

def print_border(text: str, color=Fore.CYAN, width=BORDER_WIDTH):
    text = text.strip()
    if len(text) > width - 4:
        text = text[:width - 7] + "..."
    padded_text = f" {text} ".center(width - 2)
    print(f"{color}┌{'─' * (width - 2)}┐{Style.RESET_ALL}")
    print(f"{color}│{padded_text}│{Style.RESET_ALL}")
    print(f"{color}└{'─' * (width - 2)}┘{Style.RESET_ALL}")

def _banner():
    banner = r"""


██████╗░░█████╗░░█████╗░██╗░░██╗░█████╗░██╗███╗░░██╗
██╔══██╗██╔══██╗██╔══██╗██║░░██║██╔══██╗██║████╗░██║
██║░░██║███████║██║░░╚═╝███████║███████║██║██╔██╗██║
██║░░██║██╔══██║██║░░██╗██╔══██║██╔══██║██║██║╚████║
██████╔╝██║░░██║╚█████╔╝██║░░██║██║░░██║██║██║░╚███║
╚═════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝╚═╝░░╚══╝


    """
    print(f"{Fore.GREEN}{banner:^80}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
    print_border("DACHAIN WAITLIST", Fore.GREEN)
    print(f"{Fore.YELLOW}│ {'Website'}: {Fore.CYAN}https://thogtoolhub.com/{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}│ {'Discord'}: {Fore.CYAN}https://discord.gg/MnmYBKfHQf{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}│ {'Channel Telegram'}: {Fore.CYAN}https://t.me/thogairdrops{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")

def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')

async def run_socialX(language: str):
    from scripts.socialX import run_socialX as socialX_run
    await socialX_run(language)

async def run_submit(language: str):
    from scripts.submit import run_submit as submit_run
    await submit_run(language)

async def run_badge6days(language: str):
    from scripts.badge6days import run_badge6days as badge6days_run
    await badge6days_run(language)

async def run_faucet(language: str):
    from scripts.faucet import run_faucet as faucet_run
    await faucet_run(language)

async def run_social(language: str):
    from scripts.social import run_social as social_run
    await social_run(language)

async def run_creates(language: str):
    from scripts.creates import run_creates as creates_run
    await creates_run(language)

async def run_sendtx(language: str):
    from scripts.sendtx import run_sendtx as sendtx_run
    await sendtx_run(language)

async def run_transactions(language: str):
    from scripts.transactions import run_transactions as transactions_run
    await transactions_run(language)

async def run_holding(language: str):
    from scripts.holding import run_holding as holding_run
    await holding_run(language)
   
async def cmd_exit(language: str):
    messages = {"vi": "Đang thoát...", "en": "Exiting..."}
    print_border(messages[language], Fore.GREEN)
    sys.exit(0)

SCRIPT_MAP = {
    "badge6days" run_badge6days,
    "faucet": run_faucet,
    "social": run_social,
    "creates": run_creates,
    "sendtx": run_sendtx,
    "transactions": run_transactions,
    "holding": run_holding,
    
    "socialX": run_socialX,
    "submit": run_submit,
    "exit": cmd_exit
}


def get_available_scripts(language):
    scripts = {
        'vi': [
            {"name": "$. Nhân Badge → EARLY.BADGE [ Kết thúc 6 ngày ]", "value": "badge6days"},
            
            {"name": "1. Faucet DACC → DAC Inception", "value": "faucet"},
            {"name": "2. Tự động hoàn thành nhiệm vụ Exploration", "value": "social"},
            {"name": "3. Tự động hoàn thành mở Quantum Crates", "value": "creates"},
            {"name": "4. Gửi TX ngẫu nhiên hoặc File (address.txt)", "value": "sendtx"},
            {"name": "5. Tự động xác nhận nhiệm vụ Transactions", "value": "transactions"},
            {"name": "6. Tự động xác nhận nhiệm vụ Holding", "value": "holding"},
            

            
            {"name": "#. Tự động hoàn thành nhiệm vụ DIRECTIVES ( Login X )", "value": "socialX"},
            {"name": "#. Tự động submit nhiệm vụ Email | Share ( Login X )", "value": "submit"},
            
            {"name": "X. Thoát", "value": "exit"},
        ],
        'en': [
            {"name": "$. Claim Badge → EARLY.BADGE [ End 6 days ]", "value": "badge6days"},
            
            {"name": "1. Faucet DACC → DAC Inception", "value": "faucet"},
            {"name": "2. Automatic tasks Exploration", "value": "social"},
            {"name": "3. Automatic open Quantum Crates", "value": "creates"},
            {"name": "4. Send TX random or File (address.txt)", "value": "sendtx"},
            {"name": "5. Automatically define tasks Transactions", "value": "transactions"},
            {"name": "6. Automatically define tasks Holding", "value": "holding"},

            
            {"name": "#. Automatic task DIRECTIVES ( Login X )", "value": "socialX"},
            {"name": "#. Automatic submit tasks Email | Share ( Login X )", "value": "submit"},

            {"name": "X. Thoát", "value": "exit"},
        ]
    }
    return scripts[language]

def run_script(script_func, language):
    """Chạy script bất kể nó là async hay không."""
    if asyncio.iscoroutinefunction(script_func):
        asyncio.run(script_func(language))
    else:
        script_func(language)

def select_language():
    while True:
        _clear()
        _banner()
        print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
        print_border("CHỌN NGÔN NGỮ / SELECT LANGUAGE", Fore.YELLOW)
        questions = [
            inquirer.List('language',
                          message=f"{Fore.CYAN}Vui lòng chọn / Please select:{Style.RESET_ALL}",
                          choices=[("1. Tiếng Việt", 'vi'), ("2. English", 'en')],
                          carousel=True)
        ]
        answer = inquirer.prompt(questions)
        if answer and answer['language'] in ['vi', 'en']:
            return answer['language']
        print(f"{Fore.RED}❌ {'Lựa chọn không hợp lệ / Invalid choice':^76}{Style.RESET_ALL}")

def main():
    _clear()
    _banner()
    language = select_language()

    messages = {
        "vi": {
            "running": "Đang thực thi: {}",
            "completed": "Đã hoàn thành: {}",
            "error": "Lỗi: {}",
            "press_enter": "Nhấn Enter để tiếp tục...",
            "menu_title": "MENU CHÍNH",
            "select_script": "Chọn script để chạy",
            "locked": "🔒 Script này bị khóa! Vui lòng vào group hoặc donate để mở khóa."
        },
        "en": {
            "running": "Running: {}",
            "completed": "Completed: {}",
            "error": "Error: {}",
            "press_enter": "Press Enter to continue...",
            "menu_title": "MAIN MENU",
            "select_script": "Select script to run",
            "locked": "🔒 This script is locked! Please join our group or donate to unlock."
        }
    }

    while True:
        _clear()
        _banner()
        print(f"{Fore.YELLOW}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
        print_border(messages[language]["menu_title"], Fore.YELLOW)
        print(f"{Fore.CYAN}│ {messages[language]['select_script'].center(BORDER_WIDTH - 4)} │{Style.RESET_ALL}")

        available_scripts = get_available_scripts(language)
        questions = [
            inquirer.List('script',
                          message=f"{Fore.CYAN}{messages[language]['select_script']}{Style.RESET_ALL}",
                          choices=[script["name"] for script in available_scripts],
                          carousel=True)
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            continue

        selected_script_name = answers['script']
        selected_script = next(script for script in available_scripts if script["name"] == selected_script_name)
        selected_script_value = selected_script["value"]

        if selected_script.get("locked"):
            _clear()
            _banner()
            print_border("SCRIPT BỊ KHÓA / LOCKED", Fore.RED)
            print(f"{Fore.YELLOW}{messages[language]['locked']}")
            print('')
            print(f"{Fore.CYAN}→ Telegram: https://t.me/thogairdrops")
            print(f"{Fore.CYAN}→ Website: https://thogtoolhub.com{Style.RESET_ALL}")
            print('')
            input(f"{Fore.YELLOW}⏎ {messages[language]['press_enter']}{Style.RESET_ALL:^76}")
            continue

        script_func = SCRIPT_MAP.get(selected_script_value)
        if script_func is None:
            print(f"{Fore.RED}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(f"{'Chưa triển khai / Not implemented'}: {selected_script_name}", Fore.RED)
            input(f"{Fore.YELLOW}⏎ {messages[language]['press_enter']}{Style.RESET_ALL:^76}")
            continue

        try:
            print(f"{Fore.CYAN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(messages[language]["running"].format(selected_script_name), Fore.CYAN)
            run_script(script_func, language)
            print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(messages[language]["completed"].format(selected_script_name), Fore.GREEN)
            input(f"{Fore.YELLOW}⏎ {messages[language]['press_enter']}{Style.RESET_ALL:^76}")
        except Exception as e:
            print(f"{Fore.RED}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(messages[language]["error"].format(str(e)), Fore.RED)
            print('')
            input(f"{Fore.YELLOW}⏎ {messages[language]['press_enter']}{Style.RESET_ALL:^76}")

if __name__ == "__main__":
    main()









