import requests
import json

url = "https://web-api.app.fedshi.com/query"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Content-Type": "application/json"
}

print("🚀 لقينا المفتاح السري (ListProducts)! جاري فتح المخزن...")

# استخدمنا الأمر اللي السيرفر فضح نفسه بيه
payload = {
    "query": "query { ListProducts { id } }"
}

try:
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    
    # إذا السيرفر انطانا الداتا بدون أخطاء
    if "errors" not in data:
        print("🎉🎉 بوم! المخزن انفتح والمنتجات كدامنا:")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:800])
    else:
        # إذا السيرفر طلب متغيرات إضافية (مثل رقم الصفحة أو غيره)
        error_msg = data['errors'][0].get('message', 'خطأ غير معروف')
        print("⚠️ السيرفر تعرف على الأمر، بس طلب تفاصيل أكثر:")
        print(f"الرد: {error_msg}")
        
except Exception as e:
    print(f"❌ حدث خطأ بالاتصال: {e}")
    
