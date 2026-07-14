import requests
from bs4 import BeautifulSoup
import json

# رابط قائمة المنتجات الرئيسي
url = "https://web.fedshi.com/list" 
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    print("⏳ جاري سحب البيانات وتحليل الأقسام والترند...")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    next_data = soup.find('script', id='__NEXT_DATA__')
    if next_data:
        data = json.loads(next_data.string)
        
        # حفظ البيانات في ملف لقراءتها
        with open('debug_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print("✅ تم بنجاح!")
        print("تم حفظ البيانات البرمجية في ملف جديد اسمه: debug_data.json")
        print("\nالمفاتيح الأساسية المتاحة بالصفحة هي:")
        
        # استخراج المفاتيح لمعرفة مكان المنتجات
        page_props = data.get('props', {}).get('pageProps', {})
        for key in page_props.keys():
            print(f"- {key}")
            
    else:
        print("❌ لم يتم العثور على البيانات المخفية.")
            
except Exception as e:
    print(f"حدث خطأ: {e}")
    
