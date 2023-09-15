import requests
from python-dotenv import load_dotenv # ?

load_dotenv()
wt = os.getenv("WT")
heades = {'User-Agent': 'Firefox blabal', 'Authorization': 'Bearer blblaba'}

rt = requests.get("https://link.zde", headers=heades)

title = rt.json()["sections"][0]["items"][0]["title"]
desc = rt.json()["sections"][0]["items"][0]["short_description"]
il = rt.json()["sections"][0]["items"][0]["image"]["url"]

print(rt.statuscode)
print(title, " - ", desc)
print(il)