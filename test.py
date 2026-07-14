import requests
import json

print("🔄 جاري الاتصال بالسيرفر وفحص الـ API تلقائياً...")

# الرابط الذي سحبه البوت مالتنا بنجاح
api_url = "https://web-api.app.fedshi.com/query"

# ترويسة بسيطة وعامة جداً لتجنب أي تعقيد
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# محاولة 1: طلب المنتجات بأسهل وأقصر صيغة ممكنة لمعرفة استجابة السيرفر
payload_try_1 = {
    "query": "{ products { id name price } }"
}

# محاولة 2: استعلام الفحص الذاتي (Introspection) لمعرفة أسماء الجداول بالسيرفر
introspection_payload = {
    "query": """
    {
      __schema {
        queryType {
          fields {
            name
          }
        }
      }
    }
    """
}

try:
    print("⚡ 1. محاولة جلب قائمة المنتجات مباشرة...")
    response = requests.post(api_url, json=payload_try_1, headers=headers, timeout=10)
    
    if response.status_code == 200:
        res_json = response.json()
        print("✅ استجاب السيرفر بنجاح!")
        print("📊 البيانات المستلمة:")
        print(json.dumps(res_json, indent=2, ensure_ascii=False)[:1000]) # طباعة أول 1000 حرف
    else:
        print(f"⚠️ المحاولة الأولى لم تنجح (رمز الحالة {response.status_code}).")
        print("⚡ 2. جاري محاولة فحص هيكل البيانات الداخلي (Introspection)...")
        
        # إذا فشلت المحاولة الأولى، نطلب من السيرفر أن يعطينا الأسماء المتاحة لديه
        response_intro = requests.post(api_url, json=introspection_payload, headers=headers, timeout=10)
        if response_intro.status_code == 200:
            intro_json = response_intro.json()
            print("✅ تم استخراج هيكل البيانات بنجاح!")
            print("📝 الجداول والطلبات المتاحة في السيرفر:")
            # استخراج أسماء الحقول المتاحة بالسيرفر
            fields = intro_json.get("data", {}).get("__schema", {}).get("queryType", {}).get("fields", [])
            for field in fields:
                print(f"   - {field.get('name')}")
        else:
            print("❌ السيرفر يتطلب توثيق (Token/Login) أو ترويسات خاصة لعرض البيانات.")
            print(f"رد السيرفر: {response_intro.text[:300]}")

except Exception as e:
    print(f"❌ حدث خطأ أثناء الاتصال: {e}")
    
