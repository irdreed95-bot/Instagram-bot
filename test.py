import requests

url = "https://web-api.app.fedshi.com/query"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
}

print("🚀 جاري إرسال طلب POST للـ API...")

try:
    # غيرنا الطريقة إلى post ودزينا داتا فارغة
    response = requests.post(url, headers=headers, json={})
    
    print(f"✅ رمز الاستجابة: {response.status_code}")
    print("📦 الرد من السيرفر:")
    print(response.text[:500])

except Exception as e:
    print(f"❌ حدث خطأ: {e}")
    
