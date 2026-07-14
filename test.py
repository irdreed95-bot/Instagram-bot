import requests
from bs4 import BeautifulSoup
import json

# معلومات الحساب الخاص بك لتسجيل الدخول
phone = "07828638203"
password = "Dreed1234"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
}

session = requests.Session()

print("⏳ جاري تحليل نظام الحماية والتحقق من طريقة تسجيل الدخول...")

# 1. محاولة تسجيل الدخول عبر نظام NextAuth (النظام القياسي لـ Next.js)
try:
    csrf_url = "https://web.fedshi.com/api/auth/csrf"
    res = session.get(csrf_url, headers=headers, timeout=10)
    if res.status_code == 200:
        csrf_data = res.json()
        csrf_token = csrf_data.get("csrfToken")
        print(f"🔑 تم العثور على نظام NextAuth! توكن الـ CSRF هو: {csrf_token[:15]}...")
        
        # إرسال طلب تسجيل الدخول
        login_url = "https://web.fedshi.com/api/auth/callback/credentials"
        payload = {
            "phone": phone,
            "username": phone, # نجرب المعرفين احتياطاً
            "password": password,
            "csrfToken": csrf_token,
            "callbackUrl": "https://web.fedshi.com/list",
            "json": "true"
        }
        
        login_res = session.post(login_url, data=payload, headers=headers)
        print(f"📊 نتيجة محاولة تسجيل الدخول (NextAuth): {login_res.status_code}")
        print(f"🔗 الرابط الفعلي بعد المحاولة: {login_res.url}")
        
        cookies = session.cookies.get_dict()
        print(f"🍪 الكوكيز المستلمة: {list(cookies.keys())}")
        
        # محاولة دخول صفحة المنتجات بعد الدخول
        list_res = session.get("https://web.fedshi.com/list", headers=headers)
        soup = BeautifulSoup(list_res.content, 'html.parser')
        next_data = soup.find('script', id='__NEXT_DATA__')
        if next_data:
            print("\n🎉🎉🎉 بشرى سارة! تم تسجيل الدخول بنجاح وسحب المنتجات!")
            with open('products_debug.json', 'w', encoding='utf-8') as f:
                json.dump(json.loads(next_data.string), f, ensure_ascii=False, indent=4)
            print("💾 تم حفظ المنتجات في ملف: products_debug.json")
            exit()
except Exception as e:
    print(f"⚠️ فشلت محاولة NextAuth أو غير مستخدمة: {e}")

# 2. في حال لم ينجح NextAuth، نقوم بتحليل كود الصفحة لمعرفة فورم تسجيل الدخول الفعلي
try:
    print("\n🔍 جاري قراءة الصفحة الرئيسية لتحليل حقول تسجيل الدخول...")
    main_res = session.get("https://web.fedshi.com/", headers=headers)
    print(f"🔗 الرابط الفعلي للصفحة الرئيسية: {main_res.url}")
    
    # حفظ سورس الصفحة للتحليل
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(main_res.text)
    print("💾 تم حفظ سورس الصفحة في ملف: page_source.html")
    
    soup = BeautifulSoup(main_res.content, 'html.parser')
    
    # البحث عن حقول الإدخال (Inputs)
    inputs = soup.find_all('input')
    print(f"📝 الحقول المتاحة في الصفحة ({len(inputs)} حقول):")
    for inp in inputs:
        print(f"   - Name: {inp.get('name')}, Type: {inp.get('type')}, ID: {inp.get('id')}, Placeholder: {inp.get('placeholder')}")
        
    # البحث عن الفورم (Form)
    forms = soup.find_all('form')
    print(f"📦 الفورم المتاحة ({len(forms)} فورم):")
    for i, form in enumerate(forms):
        print(f"   - فورم {i+1}: Action={form.get('action')}, Method={form.get('method')}")

except Exception as e:
    print(f"❌ حدث خطأ أثناء تحليل الصفحة: {e}")
    
