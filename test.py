import requests
import json

url = "https://web-api.app.fedshi.com/query"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

print("🕵️‍♂️ السيرفر قافل الخريطة، بس راح نجبره يفضح الأسماء بالخطأ...")

# حطينا Images بدون تفاصيلها حتى يعترض، وحطينا كل كلمات السعر حتى يصلحلنا
payload = {
    "query": "query { ListProducts(Request: { Page: 1 }) { Products { ID Name Images Price Cost Pricing Total PriceList } } }"
}

try:
    response = requests.post(url, headers=headers, json=payload)
    print("\n📦 رد السيرفر (ركز على قسم errors):")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"❌ خطأ: {e}")
    
