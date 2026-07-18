import requests
import json

url = "https://web-api.app.fedshi.com/query"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

print("🔍 جاري استفزاز السيرفر حتى يفضح أسماء حقول السعر والصور الحقيقية...")

# تعمدنا نكتب PriceTest و ImageTest حتى السيرفر يصلحلنا الغلط
payload = {
    "query": "query { ListProducts(Request: { Page: 1 }) { Products { ID Name PriceTest ImageTest } } }"
}

try:
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    
    print("\n📦 رد السيرفر الفضاح:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
        
except Exception as e:
    print(f"❌ خطأ: {e}")
    
