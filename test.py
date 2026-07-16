import requests

url = "https://web-api.app.fedshi.com/query"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Content-Type": "application/json"
}

# استعلام ذكي يجيب بس الأوامر (الـ Queries) المتاحة بالسيرفر
payload = {
    "query": """
    {
      __schema {
        queryType {
          fields {
            name
          }
        }
      }
    }
    """
}

print("🚀 جاري البحث عن أمر سحب المنتجات من السيرفر...")

try:
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        fields = data.get("data", {}).get("__schema", {}).get("queryType", {}).get("fields", [])
        
        print("✅ لقينا هاي الأوامر اللي تخص المنتجات والأقسام:")
        found = False
        for f in fields:
            name = f.get("name", "")
            # نبحث بس عن الكلمات اللي تفيدنا حتى ما تنترس الشاشة
            if "product" in name.lower() or "categor" in name.lower() or "item" in name.lower():
                print(f" 🎯 {name}")
                found = True
                
        if not found:
            print("⚠️ ما لقينا كلمة Product.. خلي نطبع أول 15 أمر موجود:")
            for f in fields[:15]: 
                print(f" - {f.get('name')}")
    else:
        print(f"❌ السيرفر رفض الطلب: {response.status_code}")

except Exception as e:
    print(f"❌ حدث خطأ: {e}")
    
