import requests
import json

url = "https://web-api.app.fedshi.com/query"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Content-Type": "application/json"
}

print("🚀 جاري سحب التفاصيل الكاملة (صور، أسعار، تفاصيل)...")

# الكود راح يجرب أشهر الأسماء البرمجية للصور والأسعار
payloads = [
    'query { ListProducts(Request: { Page: 1 }) { Products { ID Name Price Images } } }',
    'query { ListProducts(Request: { Page: 1 }) { Products { ID Name Price Image } } }',
    'query { ListProducts(Request: { Page: 1 }) { Products { ID Name Price { Value } Images { Url } } } }'
]

success = False
for query_str in payloads:
    try:
        response = requests.post(url, headers=headers, json={"query": query_str})
        data = response.json()
        
        # إذا السيرفر رجع البيانات بدون خطأ
        if "errors" not in data and data.get("data"):
            success = True
            
            with open("final_products.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            print("✅ تم سحب التفاصيل الكاملة بنجاح!")
            print("📦 افتح ملف final_products.json وشوف إذا الصور والأسعار موجودة.")
            break 
            
    except Exception:
        continue 

if not success:
    print("⚠️ السيرفر يحتاج تسمية معينة للصور أو الأسعار، افتح الملف وشوف شنو اللي نزل.")
    
