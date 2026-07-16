from bs4 import BeautifulSoup
import json

print("🔍 جاري الفحص الدقيق لملف live_page.html...")

try:
    # فتح الملف وقراءته
    with open("live_page.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, 'html.parser')
        
        # الطريقة الصحيحة 100% للبحث في مواقع Next.js
        next_data_script = soup.find('script', id='__NEXT_DATA__')
        
        if next_data_script:
            print("🎉 ممتاز! لقينا السكريبت الخاص بـ Next.js!")
            
            # النص بداخل السكريبت هو أصلاً JSON جاهز، بس نحوله
            json_data = json.loads(next_data_script.string)
            
            # نحفظ الداتا بملف جديد ومرتب
            with open("extracted_data.json", "w", encoding="utf-8") as out:
                json.dump(json_data, out, ensure_ascii=False, indent=2)
                
            print("✅ تم استخراج الداتا وحفظها بنجاح في ملف 'extracted_data.json'.")
            print("🚀 كملنا! روح شوف القائمة الجانبية راح تلكى الملف الجديد.")
            
        else:
            print("⚠️ لم نجد السكريبت بالمعرف __NEXT_DATA__.")
            print("💡 جاري طباعة كل السكريبتات الموجودة بالصفحة حتى نعرف وين ضامين الداتا:")
            
            # إذا الموقع مغير اسم الـ ID، هذا الكود راح يكشفه إلنا
            scripts = soup.find_all('script')
            for i, s in enumerate(scripts):
                script_id = s.get('id', 'بدون ID')
                # نطبع بس السكريبتات اللي بيها ID حتى ما تصير هوسة
                if script_id != 'بدون ID':
                    print(f" 🔹 سكريبت {i+1}: ID = {script_id}")

except Exception as e:
    print(f"❌ حدث خطأ: {e}")
    
