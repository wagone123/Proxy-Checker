import requests
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode

API_ENDPOINT = "https://api.proxyscrape.com/v2/account/datacenter_shared/whitelist"

def send_request(api_key, action, ip_to_set):
    params = {
        'auth': api_key,
        'type': 'remove' if action.lower() == 'delete' else 'add',
        'ip[]': ip_to_set
    }

    response = requests.get(API_ENDPOINT, params=urlencode(params))
    print(f"Response for {api_key} ({action}): {response.text}")

def main():
    with open('api.txt', 'r') as file:
        api_keys = [line.strip() for line in file if line.strip()]

    action = input("Enter 'add' or 'delete': ").lower()
    if action not in ('add', 'delete'):
        print("Invalid action. Exiting.")
        return

    if action == 'delete':
        ip_to_set = input("Enter IP to delete: ")
    else:
        ip_to_set = input("Enter IP to add: ")

    with ThreadPoolExecutor(max_workers=len(api_keys)) as executor:
        futures = [executor.submit(send_request, api_key, action, ip_to_set) for api_key in api_keys]

        # Wait for all the futures to complete
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
