import json
import os
import time
import requests
from instagrapi import Client

# ==========================================
# 🔑 الصق مفتاح الجلسة (sessionid) الخاص بك هنا فقط بين علامتي التنصيص
SESSION_ID = "58780692906%3AZUtwc85clhQdUu%3A21%3AAYjsW1fzKHYuHS2a1Lfa4BeoUdFpqYPerv4gUzRewg"


# ==========================================

print("🚀 تشغيل البوت الشامل لنشر جميع المنتجات...")

# 1. قراءة كل المنتجات من الملف
try:
    with open("final_products.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    products = data.get("data", {}).get("ListProducts", {}).get("Products", [])
except Exception as e:
    print(f"❌ خطأ في قراءة الملف: {e}")
    products = []

if not products:
    print("⚠️ لم يتم العثور على منتجات في الملف!")
    exit()

print(f"📦 تم العثور على {len(products)} منتج، جاري بدء النشر التلقائي...")

# 2. تسجيل الدخول
cl = Client()
try:
    print("⏳ جاري تسجيل الدخول بأمان...")
    cl.login_by_sessionid(SESSION_ID)
    print("✅ تم تسجيل الدخول بنجاح!")
except Exception as e:
    print(f"❌ فشل تسجيل الدخول: {e}")
    exit()

# 3. حلقة المرور على جميع المنتجات لنشرها تباعاً
for index, item in enumerate(products):
    name = item.get("Name", "منتج مميز")
    try:
        original_price = int(item.get("RRPPrice", 10000))
    except:
        original_price = 10000
    
    final_price = original_price + 5000  # إضافة الربح
    
    # البحث عن رابط فيديو أو صورة صالحة للمنتج
    media_url = ""
    is_video = False
    images_list = item.get("Images", [])
    
    # محاولة إيجاد فيديو (Reels) أولاً
    for img in images_list:
        url = img.get("URL", "")
        if ".mp4" in url.lower():
            media_url = url
            is_video = True
            break
            
    # إذا لم يوجد فيديو، نأخذ صورة (ونتجاهل الشعارات svg)
    if not media_url:
        for img in images_list:
            url = img.get("URL", "")
            if url and "http" in url and ".svg" not in url.lower():
                media_url = url
                break
                
    if not media_url:
        print(f"⚠️ تخطي المنتج ({name}) لعدم وجود صورة أو فيديو صالح.")
        continue

    print(f"\n🔄 جاري معالجة المنتج {index + 1} من {len(products)}: {name}")
    
    # تحميل الصورة/الفيديو من رابط المنتج
    file_ext = ".mp4" if is_video else ".jpg"
    media_path = f"temp_media_{index}{file_ext}"
    
    try:
        response = requests.get(media_url)
        with open(media_path, "wb") as f:
            f.write(response.content)
    except Exception as e:
        print(f"❌ فشل تحميل ملف المنتج: {e}")
        continue

    # تجهيز الوصف الاحترافي
    caption = f"🌟 {name} 🌟\n\nتميز بإطلالتك مع أحدث المنتجات لدينا!\n\n💰 السعر: {final_price} دينار فقط!\n🚚 يوجد توصيل لجميع محافظات العراق.\n📥 للحجز والاستفسار، راسلنا على الخاص.\n\n#شروة #تسوق_اونلاين #العراق #بغداد #اكسبلور #منتجات #توصيل_طلبات"
    story_caption = f"🔥 {name}\nبسعر {final_price} دينار فقط! 🔥"

    # النشر الفعلي
    try:
        if is_video:
            print("⏳ جاري النشر كـ فيديو ريلز (Reels)...")
            cl.clip_upload(media_path, caption)
            time.sleep(10)
            print("⏳ جاري النشر كـ ستوري (Story)...")
            cl.video_upload_to_story(media_path, story_caption)
        else:
            print("⏳ جاري النشر كـ منشور صورة (Post)...")
            cl.photo_upload(media_path, caption)
            time.sleep(10)
            print("⏳ جاري النشر كـ ستوري (Story)...")
            cl.photo_upload_to_story(media_path, story_caption)
            
        print(f"✅ تمت عملية النشر بنجاح للمنتج: {name}")
    except Exception as e:
        print(f"❌ خطأ أثناء نشر المنتج {name}: {e}")

    # مسح الملف من الذاكرة بعد النشر لتنظيف المساحة
    if os.path.exists(media_path):
        os.remove(media_path)

    # استراحة أمان (3 دقائق) لتجنب حظر الحساب (إلا إذا كان آخر منتج)
    if index < len(products) - 1:
        print("⏳ استراحة أمان: انتظار 3 دقائق قبل نشر المنتج التالي لحماية الحساب من الحظر...")
        time.sleep(180)
        
print("\n🎉🎉🎉 انتهى البوت من إدارة ونشر جميع المنتجات بنجاح!")

