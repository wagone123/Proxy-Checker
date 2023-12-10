import requests
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode
import time

API_ENDPOINT = "https://api.proxyscrape.com/v2/account/datacenter_shared/whitelist"
MAX_RETRIES = 3

def send_request(api_key, action, ip_to_set, proxy=None, retries=0):
    try:
        params = {
            'auth': api_key,
            'type': 'remove' if action.lower() == 'delete' else 'add',
            'ip[]': ip_to_set
        }

        proxies = {'http': proxy, 'https': proxy} if proxy else None
        response = requests.get(API_ENDPOINT, params=urlencode(params), proxies=proxies)
        response.raise_for_status()

        print(f"Response for {api_key} ({action}) using proxy {proxy}: {response.text}")

    except requests.RequestException as e:
        print(f"Error for {api_key} ({action}) using proxy {proxy}: {e}")

        if retries < MAX_RETRIES:
            print(f"Retrying {retries + 1}...")
            time.sleep(1)
            send_request(api_key, action, ip_to_set, proxy, retries + 1)
        else:
            print("Max retries reached. Skipping.")

def delete_ip(api_keys, ip_to_delete, proxies):
    for api_key, proxy in zip(api_keys, proxies):
        send_request(api_key, 'delete', ip_to_delete, proxy)

def add_ip(api_keys, ip_to_add, proxies=None):
    with ThreadPoolExecutor(max_workers=15) as executor:  # Set max_workers to 15
        tasks = [(api_key, 'add', ip_to_add, proxy) for api_key, proxy in zip(api_keys, proxies)]
        futures = [executor.submit(send_request, *task) for task in tasks]

        # Wait for all the futures to complete
        for future in futures:
            future.result()

def main():
    with open('api.txt', 'r') as api_file:
        api_keys = [line.strip() for line in api_file if line.strip()]

    action = input("Enter 'add' or 'delete': ").lower()
    if action not in ('add', 'delete'):
        print("Invalid action. Exiting.")
        return

    ip_to_set = input("Enter IP: ")

    with open('proxy.txt', 'r') as proxy_file:
        proxies = [line.strip() for line in proxy_file if line.strip()]

    if action == 'delete':
        delete_ip(api_keys, ip_to_set, proxies)
    else:
        add_ip(api_keys, ip_to_set, proxies)

if __name__ == "__main__":
    main()
