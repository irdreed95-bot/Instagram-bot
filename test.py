import requests
import json

url = "https://web-api.app.fedshi.com/query"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Content-Type": "application/json"
}

# هذا الاستعلام هو أبسط نوع ممكن، يطلب فقط اسم النوع (Type)
payload = {
    "query": "{ __type(name: \"Query\") { fields { name } } }"
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    print("✅ نجح الاتصال! البيانات المستلمة:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
else:
    print(f"⚠️ فشل الاتصال، الرمز: {response.status_code}")
    print(response.text)
    
