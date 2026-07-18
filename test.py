import requests
import json

url = "https://web-api.app.fedshi.com/query"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

print("📦 السيرفر انطانا صندوق (ProductListResponse)، جاري البحث عن المنتجات بداخله...")

# طرق فتح الصندوق المشهورة برمجياً
queries = [
    "query { ListProducts { items { id name } } }",
    "query { ListProducts { data { id name } } }",
    "query { ListProducts { products { id name } } }",
    "query { ListProducts { edges { node { id name } } } }",
    "query { ListProducts { nodes { id name } } }"
]

for q in queries:
    print(f"\n🔄 نجرب نفتح الصندوق بـ: {q}")
    payload = {"query": q}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        # إذا السيرفر ما رجع خطأ، معناها فتحنا الصندوق!
        if "errors" not in data:
            print("🎉🎉🎉 بوم! كسرنا الصندوق وطلعت المنتجات!")
            # نطبع أول 800 حرف حتى ما تنترس شاشتك بالتليفون
            print(json.dumps(data, indent=2, ensure_ascii=False)[:800])
            break 
        else:
            error_msg = data['errors'][0].get('message', 'خطأ')
            # السيرفر مرات يفضح الاسم الصحيح برسالة الخطأ
            print(f"❌ مو هذا المفتاح، الرد: {error_msg[:100]}")
            
    except Exception as e:
        print(f"❌ حدث خطأ بالاتصال.")
        
print("\n🏁 انتهى الفحص.")
