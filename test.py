import requests
from bs4 import BeautifulSoup
import json

# راح نستهدف الموقع الرئيسي مباشرة
url = "https://fedshi.com/" 

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("🚀 جاري سحب الصفحة واستخراج البيانات المخفية...")

try:
    response = requests.get(url, headers=headers)
    # استخدام المكتبة لتحليل الصفحة
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # البحث عن الكنز (البيانات المخفية)
    next_data = soup.find('script', id='__NEXT_DATA__')
    
    if next_data:
        # تحويل النص إلى بيانات مقروءة
        data = json.loads(next_data.text)
        print("✅ كفو! تم العثور على البيانات بنجاح.")
        
        # حفظ البيانات بملف حتى نقدر نفحصها براحتنا
        with open("fedshi_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print("🎉 تم حفظ المنتجات في ملف fedshi_data.json بالقائمة الجانبية.")
    else:
        print("❌ ما لقينا سكربت __NEXT_DATA__ بالصفحة.")

except Exception as e:
    print(f"❌ حدث خطأ: {e}")
    
