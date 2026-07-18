import requests
import json

url = "https://web-api.app.fedshi.com/query"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

print("🕵️‍♂️ جاري إجبار السيرفر على كشف اسم رابط الصورة...")

# حطينا TestLink بداخل أقواس الصور حتى يعترض ويصلحلنا الغلط
payload = {
    "query": "query { ListProducts(Request: { Page: 1 }) { Products { ID Name RRPPrice Images { TestLink } } } }"
}

try:
    response = requests.post(url, headers=headers, json=payload)
    print("\n📦 رد السيرفر (ركز هنا راح يگولنا شنو الاسم الصحيح بدل TestLink):")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"❌ خطأ: {e}")
    
