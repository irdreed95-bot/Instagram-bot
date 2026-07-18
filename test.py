import requests
import json

url = "https://web-api.app.fedshi.com/query"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

print("🚀 جاري إرسال الطلب بالصيغة الرسمية اللي طلبها السيرفر...")

# ضفنا (Request: {}) مثل ما طلب، وسوينا الحروف كبيرة ID و Name
payload = {
    "query": "query { ListProducts(Request: {}) { Products { ID Name } } }"
}

try:
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    
    # إذا ماكو أخطاء، معناها فتحنا المخزن أخيراً!
    if "errors" not in data:
        print("🎉🎉🎉 أخيييييراً! نجحنا والمخزن انفتح!")
        
        # نحفظ المنتجات بملف حتى نستخدمها للبوت
        with open("final_products.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print("✅ تم سحب المنتجات وحفظها في ملف 'final_products.json' بالقائمة الجانبية.")
        
        # نطبع أول منتجين بس حتى تشوفهم بعينك
        products = data.get("data", {}).get("ListProducts", {}).get("Products", [])
        print("\n🛒 عينة من المنتجات اللي سحبناها:")
        for p in products[:2]:
            print(f"- رقم المنتج: {p.get('ID')} | الاسم: {p.get('Name')}")
            
    else:
        print("⚠️ السيرفر طلب تعديل جديد، هذا رده:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
except Exception as e:
    print(f"❌ حدث خطأ بالاتصال: {e}")
    
