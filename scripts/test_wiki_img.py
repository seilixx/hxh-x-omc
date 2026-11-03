import urllib.request
import json
import urllib.parse

def test_wiki(title):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Antigravity/1.0 (test@example.com)"})
    try:
        with urllib.request.urlopen(req, timeout=5) as res:
            data = json.loads(res.read())
            img = data.get("thumbnail", {}).get("source") or data.get("originalimage", {}).get("source")
            print(f"{title} -> {img}")
            return img
    except Exception as e:
        print(f"Error {title}: {e}")
        return None

test_wiki("Iron Man")
test_wiki("Spider-Man")
test_wiki("Lionel Messi")
test_wiki("Cristiano Ronaldo")
