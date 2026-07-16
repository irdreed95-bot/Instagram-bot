import requests

url = "https://web-api.app.fedshi.com/query"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("🚀 جاري ضرب الـ API مباشرة...")

try:
    # راح نجرب نرسل طلب مباشر للرابط
    response = requests.get(url, headers=headers)
    
    print(f"✅ رمز الاستجابة: {response.status_code}")
    print("📦 الرد من السيرفر (أول 500 حرف):")
    print(response.text[:500])

except Exception as e:
    print(f"❌ حدث خطأ: {e}")
    
