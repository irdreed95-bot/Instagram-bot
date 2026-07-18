import requests
import json

url = "https://web-api.app.fedshi.com/query"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

print("🕵️‍♂️ السيرفر غلس وما انطانا تلميح... جاري كسر الحقل بتجربة أشهر الكلمات تلقائياً...")

# قائمة بأشهر الأسماء اللي يستخدموها المبرمجين لروابط الصور
image_fields = ["URL", "url", "Url", "path", "Path", "src", "link", "file", "id", "ID"]

success = False

for field in image_fields:
    # الكود راح يعوض الكلمة بدل المتغير (field) ويجرب
    payload = {
        "query": f"query {{ ListProducts(Request: {{ Page: 1 }}) {{ Products {{ ID Name RRPPrice Images {{ {field} }} }} }} }}"
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload)
        data = res.json()
        
        # إذا السيرفر رجع البيانات بدون أخطاء، معناها لقفنا الكلمة الصح!
        if "errors" not in data and data.get("data"):
            print(f"\n🎉🎉 لقفناهااا! الكلمة الصحيحة لرابط الصورة هي: {field}")
            
            with open("final_products.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            print("✅ تم سحب المنتجات بالكامل (الاسم، السعر، الصور) بملف final_products.json!")
            success = True
            break # نوقف المحاولات فوراً
            
    except Exception:
        continue # نعبر عالكلمة اللي بعدها إذا فشلت

if not success:
    print("⚠️ ولا كلمة نجحت! المبرمج مستخدم اسم غريب جداً.")
    
