import requests
from bs4 import BeautifulSoup
import json

# الرابط الافتراضي لقائمة المنتجات
url = "https://web.fedshi.com/list" 
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    print("⏳ جاري فحص الصفحة لمعرفة هيكلية الموقع...")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # فحص إذا الموقع يستخدم تقنية Next.js (وهي الطريقة الأسهل والأضمن للسحب)
    next_data = soup.find('script', id='__NEXT_DATA__')
    if next_data:
        print("🎉 بشرى سارة! الموقع يستخدم Next.js.")
        print("هذا يعني نكدر نسحب كل المنتجات والأسعار والصور من ملف JSON الداخلي بدون أي تعقيد!")
    else:
        # فحص كلاسات المنتجات العادية
        text = response.text.lower()
        if "product" in text or "price" in text:
            print("👍 المنتجات تظهر في الـ HTML مباشرة ونكدر نقراها بالكود الحالي.")
        else:
            print("⚠️ تنبيه: المنتجات لا تظهر مباشرة بالـ HTML (غالباً الموقع يعتمد على طلبات API مخفية).")
            
except Exception as e:
    print(f"حدث خطأ أثناء الفحص: {e}")
  
