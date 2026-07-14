import os
import re
import json
import requests
from bs4 import BeautifulSoup

print("⏳ جاري تشغيل الفحص المتقدم لاستخراج الـ API وسيرفر الموقع...")

# 1. التأكد من وجود ملف السورس وقراءته
if not os.path.exists("page_source.html"):
    print("❌ لم يتم العثور على ملف page_source.html. يرجى إعادة تشغيل الكود الأصلي لحفظ الصفحة.")
    exit()

with open("page_source.html", "r", encoding="utf-8") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

# 2. البحث عن بيانات Next.js المخفية في الـ HTML (__NEXT_DATA__)
print("\n🔍 1. البحث في بيانات Next.js الداخلية (قد تحتوي على روابط السيرفر)...")
next_data_tag = soup.find('script', id='__NEXT_DATA__')
if next_data_tag:
    try:
        next_data = json.loads(next_data_tag.string)
        print("✅ تم العثور على __NEXT_DATA__!")
        # طباعة معلومات الـ Build والـ Props
        print(f"   - Build ID: {next_data.get('buildId')}")
        # حفظ البيانات في ملف منفصل للتحليل
        with open("next_data.json", "w", encoding="utf-8") as nd_f:
            json.dump(next_data, nd_f, ensure_ascii=False, indent=4)
        print("💾 تم حفظ بيانات Next.js في ملف: next_data.json")
    except Exception as e:
        print(f"   ⚠️ خطأ أثناء تحليل __NEXT_DATA__: {e}")
else:
    print("   - لم يتم العثور على تاق __NEXT_DATA__.")

# 3. استخراج روابط ملفات الجافاسكريبت (.js)
print("\n🔍 2. استخراج ملفات الجافاسكريبت (.js) من الكود...")
scripts = soup.find_all('script', src=True)
js_urls = []
for s in scripts:
    src = s.get('src')
    if src and ('_next' in src or 'static' in src or 'chunks' in src):
        if src.startswith('/'):
            js_urls.append(f"https://web.fedshi.com{src}")
        else:
            js_urls.append(src)

print(f"   - تم العثور على {len(js_urls)} ملف جافاسكريبت.")

# 4. تحميل وتحليل ملفات الـ JS للبحث عن روابط الـ API وحقول تسجيل الدخول
print("\n🔍 3. جاري فحص محتوى ملفات الجافاسكريبت تلقائياً للبحث عن روابط الـ API...")
found_endpoints = set()

# الكلمات المفتاحية والأنماط للبحث عن روابط
url_pattern = re.compile(r'https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s\'"`]*)?', re.IGNORECASE)
api_route_pattern = re.compile(r'[\'"`]/api/[^\s\'"`]+[\'"`]', re.IGNORECASE)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

for idx, url in enumerate(js_urls):
    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            js_text = res.text
            
            # البحث عن جميع الروابط الكاملة
            urls = url_pattern.findall(js_text)
            for u in urls:
                if 'w3.org' not in u and 'reactjs' not in u and 'nextjs' not in u and 'vercel' not in u:
                    found_endpoints.add(u)
            
            # البحث عن مسارات الـ API الداخلية مثل /api/...
            api_routes = api_route_pattern.findall(js_text)
            for r in api_routes:
                found_endpoints.add(r.strip('\'"`'))
                
    except Exception as e:
        pass

print("\n🎯 النتائج والروابط المكتشفة:")
important_links = []
for ep in list(found_endpoints):
    ep_lower = ep.lower()
    # تصفية الروابط المهمة التي تحتوي على كلمات تخص فدشي أو تسجيل الدخول
    if 'fedshi' in ep_lower or any(kw in ep_lower for kw in ['login', 'signin', 'auth', 'user', 'token', 'signup', 'register', 'session']):
        important_links.append(ep)

if important_links:
    print("📌 تم العثور على هذه الروابط الهامة جداً:")
    for link in sorted(important_links):
        print(f"   ⭐ {link}")
else:
    print("❌ لم يتم العثور على روابط خاصة في الملفات السطحية.")
    print("📌 الروابط العامة المكتشفة الأخرى (أول 10 روابط):")
    for link in list(found_endpoints)[:10]:
        print(f"   - {link}")

print("\n💡 جاري البحث والتحليل... انتهى الفحص!")
