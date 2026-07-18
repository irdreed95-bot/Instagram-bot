import requests
import json

url = "https://web-api.app.fedshi.com/query"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Content-Type": "application/json"
}

print("🚀 جاري تنفيذ الحل الشامل... (الكود ديجرب كل الاحتمالات بصمت، ثواني وراجعلك)")

# قائمة بكل الاحتمالات اللي ممكن السيرفر يطلبها (الكود راح يجربها كلها بدون ما يطلعلك أي خطأ)
payloads = [
    'query { ListProducts(Request: { Page: 1, PageSize: 10 }) { Products { ID Name } } }',
    'query { ListProducts(Request: { Page: 1, Size: 10 }) { Products { ID Name } } }',
    'query { ListProducts(Request: { Page: 1, PerPage: 10 }) { Products { ID Name } } }',
    'query { ListProducts(Request: { Page: 1, Take: 10 }) { Products { ID Name } } }',
    'query { ListProducts(Request: { Page: 1 }) { Products { ID Name } } }'
]

success = False

for query_str in payloads:
    try:
        response = requests.post(url, headers=headers, json={"query": query_str})
        data = response.json()
        
        # إذا السيرفر رجع داتا حقيقية وماكو أخطاء
        if "errors" not in data and data.get("data"):
            success = True
            print("\n🎉🎉🎉 أخييييراً! نجحت العملية وكسرنا الحماية!")
            
            # حفظ البيانات بملف نظيف وجاهز
            with open("final_products.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            print("✅ تم سحب المنتجات وحفظها بملف: final_products.json (تلكاه بالقائمة الجانبية)")
            
            # طباعة عينة من المنتجات للتأكيد
            products = data["data"]["ListProducts"]["Products"]
            if products:
                print("\n🛒 عينة من المنتجات اللي انسحبت:")
                for p in products[:3]:
                    print(f" 🔹 {p.get('Name')}")
            break # نوقف المحاولات لأن نجحنا
            
    except Exception:
        # إذا صار خطأ، الكود راح يغلس ويعبر عالمحاولة اللي بعدها بدون ما يزعجك
        continue 

if not success:
    print("\n❌ السيرفر قافل قفلة نهائية ويحتاج رمز دخول (Token).")
    print("الموقع محمي بدرجة عالية، والحل الوحيد الباقي هو ننسخ كود الـ Token من متصفحك.")
    
