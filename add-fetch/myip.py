import requests
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode

API_ENDPOINT = "https://api.proxyscrape.com/v2/account/datacenter_shared/whitelist"

def send_request(api_key, action, ip_to_set, proxy=None):
    try:
        params = {
            'auth': api_key,
            'type': 'remove' if action.lower() == 'delete' else 'add',
            'ip[]': ip_to_set
        }

        # Use the 'proxies' parameter to specify the proxy for this request if provided
        proxies = {'http': proxy, 'https': proxy} if proxy else None
        response = requests.get(API_ENDPOINT, params=urlencode(params), proxies=proxies)
        response.raise_for_status()  # Raise HTTPError for bad responses

        print(f"Response for {api_key} ({action}) using proxy {proxy}: {response.text}")

    except requests.RequestException as e:
        print(f"Error for {api_key} ({action}) using proxy {proxy}: {e}")

def delete_ip(api_key, ip_to_delete):
    send_request(api_key, 'delete', ip_to_delete)

def add_ip(api_key, ip_to_add, proxies=None):
    with ThreadPoolExecutor() as executor:
        # Use concurrent connections for IP addition
        tasks = [(api_key, 'add', ip_to_add, proxy) for proxy in proxies]
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

    if action == 'delete':
        # Perform IP deletion one by one
        for api_key in api_keys:
            delete_ip(api_key, ip_to_set)
    else:
        # Read proxies from proxy.txt for concurrent IP addition
        with open('proxy.txt', 'r') as proxy_file:
            proxies = [line.strip() for line in proxy_file if line.strip()]

        add_ip(api_keys[0], ip_to_set, proxies)

if __name__ == "__main__":
    main()
