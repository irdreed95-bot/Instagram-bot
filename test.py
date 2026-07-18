import requests
import json

url = "https://web-api.app.fedshi.com/query"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

print("🚀 جاري سحب المنتجات (الحل النهائي)...")

# السيرفر اعترف أن الكلمة هي Products (بحرف P كبير)
# هذا الكود راح يجرب يسحب البيانات بأكثر من صيغة لحد ما ينجح فوراً
fields_to_try = [
    "id name price",
    "id title price",
    "id name",
    "id title",
    "id"
]

success = False
for fields in fields_to_try:
    payload = {"query": f"query {{ ListProducts {{ Products {{ {fields} }} }} }}"}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        # إذا ماكو خطأ، معناها سحبنا المنتجات بنجاح!
        if "errors" not in data:
            # حفظ المنتجات بملف نهائي نظيف
            with open("final_products.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print("🎉🎉🎉 مبروووووك! انتهى التعب وكسرنا حماية الموقع!")
            print("✅ تم سحب المنتجات وحفظها في ملف 'final_products.json' بالقائمة الجانبية.")
            
            # طباعة أول منتج حتى تشوفه بعينك
            products_list = data.get("data", {}).get("ListProducts", {}).get("Products", [])
            if products_list:
                print("\n🛒 عينة من أول منتج تم سحبه:")
                print(json.dumps(products_list[0], indent=2, ensure_ascii=False))
            
            success = True
            break # نوقف البحث لأن تمت العملية
            
    except Exception as e:
        pass

if not success:
    print("❌ واجهنا مشكلة، تأكد من الاتصال بالإنترنت.")
    
