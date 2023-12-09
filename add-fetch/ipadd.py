import requests
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode

API_ENDPOINT = "https://api.proxyscrape.com/v2/account/datacenter_shared/whitelist"

def send_request(api_key, action, ip_to_set, proxy):
    params = {
        'auth': api_key,
        'type': 'remove' if action.lower() == 'delete' else 'add',
        'ip[]': ip_to_set
    }

    # Use the 'proxies' parameter to specify the proxy for this request
    response = requests.get(API_ENDPOINT, params=urlencode(params), proxies={'http': proxy, 'https': proxy})
    print(f"Response for {api_key} ({action}) using proxy {proxy}: {response.text}")

def main():
    with open('api.txt', 'r') as api_file:
        api_keys = [line.strip() for line in api_file if line.strip()]

    with open('proxy.txt', 'r') as proxy_file:
        proxies = [line.strip() for line in proxy_file if line.strip()]

    action = input("Enter 'add' or 'delete': ").lower()
    if action not in ('add', 'delete'):
        print("Invalid action. Exiting.")
        return

    if action == 'delete':
        ip_to_set = input("Enter IP to delete: ")
    else:
        ip_to_set = input("Enter IP to add: ")

    with ThreadPoolExecutor(max_workers=len(api_keys)) as executor:
        # Pair each API key with a different proxy
        tasks = [(api_key, action, ip_to_set, proxy) for api_key, proxy in zip(api_keys, proxies)]
        futures = [executor.submit(send_request, *task) for task in tasks]

        # Wait for all the futures to complete
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
