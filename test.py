import requests
import json

url = "https://web-api.app.fedshi.com/query"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

print("🚀 جاري استخراج الصور والأسعار تلقائياً بدون أي أخطاء مزعجة...")

# قائمة بالأسماء الشائعة اللي يستخدموها المبرمجين للسعر
price_guesses = ["Cost", "Price", "SellingPrice", "CustomerPrice", "RetailPrice", "SalePrice"]
# قائمة باحتمالات الصور (لأن مرات الصور تكون رابط مباشر، ومرات تكون بداخل ملف)
image_guesses = ["Images", "Images { Url }", "Images { Path }"]

success = False

for price in price_guesses:
    for img in image_guesses:
        if success: break
        
        payload = {
            "query": f"query {{ ListProducts(Request: {{ Page: 1 }}) {{ Products {{ ID Name {price} {img} }} }} }}"
        }
        
        try:
            res = requests.post(url, headers=headers, json=payload)
            data = res.json()
            
            # إذا السيرفر انطانا الداتا بدون أي خطأ
            if "errors" not in data and data.get("data"):
                # نجحنا! نحفظ الملف فوراً
                with open("final_products.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                    
                print("\n🎉🎉 بوم! كسرنا الحماية ولقينا الأسماء الصحيحة!")
                print(f"💰 السعر طلع اسمه بالموقع: {price}")
                print(f"🖼️ الصور طلع اسمها بالموقع: {img}")
                print("\n✅ تم سحب التفاصيل وحفظها في final_products.json جاهزة للانستغرام!")
                success = True
        except:
            pass # الكود راح يغلس على أي خطأ ويعبر للتخمين اللي بعده

if not success:
    # إذا كل التخمينات فشلت، هذا الأمر الإجباري راح يسحب "خريطة" الموقع غصباً عنه
    print("⚠️ السيرفر معاند جداً، جاري سحب خريطة المنتج لمعرفة الأسماء الحقيقية...")
    res = requests.post(url, headers=headers, json={"query": 'query { __type(name: "Product") { fields { name } } }'})
    print(json.dumps(res.json(), indent=2))
    
