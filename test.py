import requests
import json

url = "https://web-api.app.fedshi.com/query"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

print("🚀 جاري الالتفاف على خطأ السيرفر وسحب البيانات...")

# راح نجرب الكلمات الآمنة اللي ما تسوي كراش للسيرفر
safe_fields = ["url", "path", "src", "link", "fileUrl", "id"]
success = False

for field in safe_fields:
    print(f"🔄 نجرب حقل الصور: {field}")
    payload = {
        "query": f"query {{ ListProducts(Request: {{ Page: 1 }}) {{ Products {{ ID Name RRPPrice Images {{ {field} }} }} }} }}"
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload)
        data = res.json()
        
        # إذا السيرفر رجع بيانات (حتى لو اكو تحذيرات بسيطة)، نحفظها فوراً!
        if data.get("data") and data["data"].get("ListProducts"):
            print(f"\n🎉 بطل! الكلمة الصحيحة والآمنة هي: {field}")
            with open("final_products.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("✅ تم تجهيز ملف final_products.json بنجاح!")
            success = True
            break # نوقف البحث لأن لقينا المطلوب
    except Exception as e:
        pass
        
if not success:
    print("\n❌ السيرفر ديواجه مشكلة عامة. جاري فحص استجابة السيرفر بدون صور:")
    payload = {"query": "query { ListProducts(Request: { Page: 1 }) { Products { ID Name RRPPrice } } }"}
    res = requests.post(url, headers=headers, json=payload)
    print(json.dumps(res.json(), indent=2, ensure_ascii=False))

