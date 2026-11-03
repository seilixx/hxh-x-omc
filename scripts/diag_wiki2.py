import urllib.request
import json

url = "https://upload.wikimedia.org/wikipedia/en/4/47/Iron_Man_%28circa_2018%29.png"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://en.wikipedia.org/"
}
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=5) as res:
        data = res.read()
        print("Success! Downloaded bytes:", len(data))
except Exception as e:
    print("Failed:", e)
