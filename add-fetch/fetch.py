import requests
import time
from datetime import datetime

def fetch_proxies(api_key, proxy):
    url = f"https://api.proxyscrape.com/v2/account/datacenter_shared/proxy-list?auth={api_key}&type=getproxies&country[]=all&protocol=http&format=normal&status=all"

    try:
        response = requests.get(url, proxies={'http': proxy, 'https': proxy}, timeout=10)
        if response.status_code == 200:
            return True, response.text.splitlines()
    except requests.RequestException as e:
        print(f"Error fetching proxies for API key {api_key} with proxy {proxy}: {e}")

    return False, []

def save_proxies(proxies, filename):
    with open(filename, "a") as file:
        file.write("\n".join(proxies) + "\n")

if __name__ == "__main__":
    # Read API keys from api.txt
    with open("api.txt", "r") as api_file:
        api_keys = api_file.read().splitlines()

    # Read proxies from proxy.txt
    with open("proxy.txt", "r") as proxy_file:
        proxies = proxy_file.read().splitlines()

    # Fetch proxies for each API key using a different proxy from proxy.txt
    all_proxies = []
    for api_key, proxy in zip(api_keys, proxies):
        success, fetched_proxies = fetch_proxies(api_key, proxy)
        if success:
            all_proxies.extend(fetched_proxies)
            print(f"Proxies fetched successfully for API key {api_key} with proxy {proxy}")
        else:
            print(f"Failed to fetch proxies for API key {api_key} with proxy {proxy}")

        # Introduce a 3-second delay
        

    # Save all proxies in a single file (append mode)
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"fetched_{current_datetime}.txt"
    save_proxies(all_proxies, filename)

    print(f"Proxies fetched successfully and saved in {filename}")
