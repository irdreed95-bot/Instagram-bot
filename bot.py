import json
import os
import time
import requests
from instagrapi import Client

# ==========================================
# 🔑 الرمز السري الخاص بك (Session ID)
SESSION_ID = "الصق_المفتاح_السري_هنا"
# ==========================================

print("🚀 تشغيل البوت باستخدام مفتاح الجلسة الآمن...")

# 1. قراءة المنتجات
try:
    with open("final_products.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    products = data.get("data", {}).get("ListProducts", {}).get("Products", [])
except Exception as e:
    print(f"❌ خطأ في قراءة ملف المنتجات: {e}")
    products = []

if not products:
    print("⚠️ لم يتم العثور على منتجات!")
    exit()

print(f"📦 تم العثور على {len(products)} منتج.")

# 2. تسجيل الدخول بالـ Session ID (بدون طلب تحقق من الهند)
cl = Client()
try:
    print("⏳ جاري تسجيل الدخول بالمفتاح السري الآمن...")
    cl.login_by_sessionid(SESSION_ID)
    print("✅ تم تسجيل الدخول بنجاح تام!")
except Exception as e:
    print(f"❌ مفتاح الجلسة منتهي الصلاحية أو خطأ: {e}")
    exit()

# 3. نشر المنتجات
fallback_video = "1000101053.mp4"

for index, item in enumerate(products):
    name = item.get("Name", "منتج مميز")
    try:
        original_price = int(item.get("RRPPrice", 10000))
    except:
        original_price = 10000
    
    final_price = original_price + 5000  # إضافة الربح
    
    media_url = ""
    is_video = False
    images_list = item.get("Images", [])
    
    for img in images_list:
        url = img.get("URL", "")
        if ".mp4" in url.lower():
            media_url = url
            is_video = True
            break
            
    if not media_url:
        for img in images_list:
            url = img.get("URL", "")
            if url and "http" in url and ".svg" not in url.lower():
                media_url = url
                break

    media_path = f"temp_media_{index}.jpg"
    if media_url:
        try:
            response = requests.get(media_url)
            file_ext = ".mp4" if is_video else ".jpg"
            media_path = f"temp_media_{index}{file_ext}"
            with open(media_path, "wb") as f:
                f.write(response.content)
        except:
            media_path = fallback_video
            is_video = True
    else:
        media_path = fallback_video
        is_video = True

    print(f"\n🔄 جاري معالجة ونشر المنتج: {name}")
    
    caption = f"🌟 {name} 🌟\n\nتميز بإطلالتك مع أحدث المنتجات!\n\n💰 السعر: {final_price} دينار فقط!\n🚚 يوجد توصيل لجميع محافظات العراق.\n📥 للحجز والاستفسار، راسلنا على الخاص.\n\n#شروة #تسوق_اونلاين #العراق #بغداد #اكسبلور"
    story_caption = f"🔥 {name}\nبسعر {final_price} دينار فقط! 🔥"

    try:
        if is_video and os.path.exists(media_path):
            print("⏳ جاري نشر ريلز...")
            cl.clip_upload(media_path, caption)
            time.sleep(10)
            print("⏳ جاري نشر ستوري...")
            cl.video_upload_to_story(media_path, story_caption)
        elif os.path.exists(media_path):
            print("⏳ جاري نشر صورة...")
            cl.photo_upload(media_path, caption)
            time.sleep(10)
            print("⏳ جاري نشر ستوري...")
            cl.photo_upload_to_story(media_path, story_caption)
            
        print(f"✅ تم نشر المنتج ({name}) بنجاح!")
    except Exception as e:
        print(f"❌ خطأ أثناء النشر: {e}")

    if "temp_media_" in media_path and os.path.exists(media_path):
        os.remove(media_path)

    if index < len(products) - 1:
        print("⏳ استراحة 3 دقائق قبل المنتج التالي...")
        time.sleep(180)

print("\n🎉 انتهى البوت من نشر كل المنتجات بنجاح!")

