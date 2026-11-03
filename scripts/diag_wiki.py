import urllib.request
import json
import urllib.parse

url = "https://en.wikipedia.org/api/rest_v1/page/summary/Iron_Man"
headers = {
    "User-Agent": "HunterXOmcApp/1.0 (contact: info@example.com) python-requests"
}
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=5) as res:
        data = json.loads(res.read())
        img_url = data.get("thumbnail", {}).get("source")
        print("Summary OK, thumbnail:", img_url)
        if img_url:
            img_req = urllib.request.Request(img_url, headers=headers)
            with urllib.request.urlopen(img_req, timeout=5) as img_res:
                content = img_res.read()
                print("Image download OK! Bytes:", len(content))
except Exception as e:
    print("Failed:", e)
