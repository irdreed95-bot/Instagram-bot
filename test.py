import requests
import json

url = "https://web-api.app.fedshi.com/query"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

# الكلمة الصحيحة للرابط هي URL بحروف كبيرة
payload = {
    "query": 'query { ListProducts(Request: { Page: 1 }) { Products { ID Name RRPPrice Images { URL } } } }'
}

print("🚀 جاري سحب المنتجات وحفظها (مع تجاهل تحذيرات السيرفر)...")
try:
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    
    # إذا اكو بيانات، احفظها فوراً ولا تهتم لأي رسائل ثانية
    if data.get("data") and data["data"].get("ListProducts"):
        with open("final_products.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("✅ تم السحب بنجاح! ملف final_products.json صار جاهز ومكتمل.")
    else:
        print("❌ السيرفر ما رجع أي بيانات.")
except Exception as e:
    print(f"❌ خطأ: {e}")
    
