import requests
import json

url = "https://web-api.app.fedshi.com/query"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

print("🔍 جاري فحص سبب الرفض من السيرفر...")

payload = {
    "query": "query { ListProducts { Products { id name } } }"
}

try:
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    
    print("\n📦 الرد الحقيقي من السيرفر:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
        
except Exception as e:
    print(f"❌ حدث خطأ بالاتصال: {e}")
    
