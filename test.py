import requests
import json

url = "https://web-api.app.fedshi.com/query"

# ضفنا User-Agent مال تليفون حقيقي حتى السيرفر يطمن أكثر
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Content-Type": "application/json"
}

print("🚀 جاري إضافة Limit للطلب حتى لا ينهار سيرفر فدشي...")

# ضفنا Limit: 10 بداخل الـ Request
payload = {
    "query": "query { ListProducts(Request: { Page: 1, Limit: 10 }) { Products { ID Name } } }"
}

try:
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    
    # إذا السيرفر رجع خطأ، خلي نشوف شنو هو
    if "errors" in data:
        print("⚠️ السيرفر رجع رسالة:")
        print(json.dumps(data['errors'], indent=2, ensure_ascii=False))
    else:
        print("🎉🎉🎉 كفوووو! السيرفر استقر وفتحنا المخزن!")
        print("\n📦 الرد من السيرفر:")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
        
except Exception as e:
    print(f"❌ حدث خطأ بالاتصال: {e}")
    
