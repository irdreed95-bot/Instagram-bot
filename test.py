import requests
import json

url = "https://web-api.app.fedshi.com/query"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
}

# استعلام GraphQL القياسي لسحب خريطة قاعدة البيانات
payload = {
    "query": "{ __schema { types { name kind } } }"
}

print("🚀 جاري محاولة سحب خريطة قاعدة بيانات الموقع (Schema)...")

try:
    response = requests.post(url, headers=headers, json=payload)
    
    print(f"✅ رمز الاستجابة: {response.status_code}")
    
    # إذا نجحنا والسيرفر رجع داتا (رمز 200)
    if response.status_code == 200:
        with open("graphql_schema.json", "w", encoding="utf-8") as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=2)
        print("🎉 كفو! تم حفظ المخطط في ملف graphql_schema.json بالقائمة الجانبية.")
    else:
        print("⚠️ يبدو أن المخطط مقفول، الرد من السيرفر:")
        print(response.text[:500])

except Exception as e:
    print(f"❌ حدث خطأ: {e}")
    
