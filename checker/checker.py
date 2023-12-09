import requests
import concurrent.futures

def check_proxy(proxy):
    url = "http://www.google.com"
    proxies = {"http": proxy, "https": proxy}

    try:
        start_time = time.time()
        response = requests.get(url, proxies=proxies, timeout=5)
        end_time = time.time()

        if response.status_code == 200:
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            return True, response_time
    except requests.RequestException:
        pass

    return False, None

def check_proxy_wrapper(proxy):
    result, response_time = check_proxy(proxy)
    status = "Alive" if result else "Dead"
    response_time_str = f"{response_time:.4f} ms" if response_time else "N/A"
    print(f"Proxy: {proxy} - Status: {status} - Response Time: {response_time_str}")

if __name__ == "__main__":
    import time

    # Read proxies from proxy.txt
    with open("proxy.txt", "r") as file:
        proxies = file.read().splitlines()

    # Use 10 threads for faster checking
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(check_proxy_wrapper, proxies)
