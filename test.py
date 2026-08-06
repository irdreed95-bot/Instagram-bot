import requests
import json

url = "https://web-api.app.fedshi.com/query"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

# راح نطلب الـ URL ونشوف السيرفر شنو راح يجاوبنا حرفياً
payload = {
    "query": 'query { ListProducts(Request: { Page: 1 }) { Products { ID Name RRPPrice Images { URL } } } }'
}

print("🔍 جاري قراءة عقل السيرفر وطباعة رده بالكامل...")

try:
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    
    # هذا الأمر راح يطبع كل شي يرجعه السيرفر (أخطاء، بيانات، تلميحات)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
except Exception as e:
    print(f"❌ خطأ: {e}")

