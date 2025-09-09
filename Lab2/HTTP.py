import requests

def http_requests():
    try:
        get_url = "https://postman-echo.com/get?message=hello"
        r1 = requests.get(get_url)
        print("GET:", r1.status_code, r1.text[:200])

        post_url = "https://postman-echo.com/post"
        r2 = requests.post(post_url, data={"msg": "hello"})
        print("POST:", r2.status_code, r2.text[:200])
    except Exception as e:
        print("Error:", e)

http_requests()
