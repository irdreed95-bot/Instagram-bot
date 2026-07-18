import requests
import json

url = "https://web-api.app.fedshi.com/query"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Content-Type": "application/json"
}

print("🚀 جاري اختراق حماية الـ GraphQL عبر تخمين الأوامر السرية...")

# قائمة بأشهر الأوامر اللي يستخدمها المبرمجين لجلب المنتجات
queries = [
    "query { products { id } }",
    "query { products(first: 5) { edges { node { id } } } }",
    "query { getProducts { id } }",
    "query { items { id } }",
    "query { productList { id } }"
]

for q in queries:
    print(f"\n🔄 نجرب الأمر: {q}")
    payload = {"query": q}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        # إذا ماكو كلمة errors بالرد، يعني الكود صح وقبلة السيرفر!
        if "errors" not in data:
            print("🎉🎉🎉 بوم! لقينا الأمر الصحيح!")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
            break # نوقف البحث لأن لقيناه
        else:
            error_msg = data['errors'][0].get('message', 'خطأ غير معروف')
            print(f"❌ السيرفر رفضه وگال: {error_msg[:100]}")
            
    except Exception as e:
        print(f"❌ حدث خطأ بالاتصال.")
        
print("\n🏁 انتهى الفحص.")
