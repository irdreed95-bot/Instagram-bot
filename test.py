import json
import os
import re

print("🔍 جاري تصحيح الخطأ وفحص ملف page_source.html...")

# 1. التأكد من وجود الملف الذي نمتلكه فعلاً في القائمة الجانبية
if not os.path.exists("page_source.html"):
    print("❌ لم يتم العثور على ملف page_source.html.")
    exit()

try:
    # 2. قراءة محتوى صفحة الويب اللي سحبها البوت
    with open("page_source.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    # 3. استخراج البيانات السرية الخاصة بـ Next.js
    print("🕵️ جاري البحث عن كنز البيانات المخفي (__NEXT_DATA__)...")
    match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html_content, re.DOTALL)

    if match:
        print("✅ ممتاز! تم العثور على البيانات المخفية داخل الصفحة.")
        json_data = json.loads(match.group(1))
        
        # 4. هنا نقوم بصناعة الملف الذي كان مفقوداً!
        with open("next_data.json", "w", encoding="utf-8") as out:
            json.dump(json_data, out, ensure_ascii=False, indent=2)
        
        print("💾 تم إنشاء وحفظ ملف 'next_data.json' بنجاح! (ستلاحظ ظهوره في القائمة الجانبية)")
        
        # 5. استخراج وعرض نظرة سريعة على البيانات
        props = json_data.get("props", {}).get("pageProps", {})
        print("\n📊 الأقسام التي تم استخراجها من الصفحة:")
        for key in props.keys():
            print(f" 🔹 {key}")
            
        print("\n🚀 عاشت إيدك! الآن صار عندنا الداتا الحقيقية، جاهزين نسحب منها المنتجات بالتفصيل.")
    else:
        print("⚠️ لم نجد وسم __NEXT_DATA__. يبدو أن الصفحة التي تم سحبها فارغة أو تحتاج توجيه مختلف.")
        
except Exception as e:
    print(f"❌ حدث خطأ: {e}")
    
