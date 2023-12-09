import requests

def get_ip_info():
    api_url = "https://api.myip.com"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        ip_info = response.json()
        print("IP Information:")
        print(f"IP Address: {ip_info['ip']}")
        print(f"Location: {ip_info.get('location', {}).get('city', 'N/A')}, {ip_info.get('location', {}).get('region', 'N/A')}, {ip_info.get('location', {}).get('country', 'N/A')}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_ip_info()
