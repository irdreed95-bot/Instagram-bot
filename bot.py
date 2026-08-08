import json
import os
import requests
import time
from instagrapi import Client

# ==========================================
# 🔑 مفتاح الجلسة الخاص بك (SESSION_ID)
SESSION_ID = "58780692906%3AZUtwc85clhQdUu%3A21%3AAYjsW1fzKHYuHS2a1Lfa4BeoUdFpqYPerv4gUzRewg"
# ==========================================

FALLBACK_IMAGE = "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop"

print("🚀 جاري الاتصال بانستغرام...")

# 1. تسجيل الدخول مرة واحدة فقط لتجنب الحظر
cl = Client()
try:
    cl.login_by_sessionid(SESSION_ID)
    print("✅ تم الاتصال بحساب الانستغرام بنجاح!")
except Exception as e:
    print(f"❌ فشل تسجيل الدخول: {e}")
    exit()

# 2. قراءة بيانات المنتجات
try:
    with open("final_products.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    products = data.get("data", {}).get("ListProducts", {}).get("Products", [])
except Exception:
    products = []

if not products:
    print("❌ لم يتم العثور على منتجات في الملف.")
    exit()

print(f"📦 تم العثور على {len(products)} منتجات، سيتم البدء بالنشر...\n")

# 3. حلقة تكرارية للمرور على جميع المنتجات
for index, item in enumerate(products, start=1):
    print(f"--- 🔄 البدء بالمنتج رقم {index} من {len(products)} ---")
    
    name = item.get("Name", "منتج مميز")
    
    # تسعير المنتج (إضافة 5000 دينار ربح)
    try:
        original_price = int(item.get("RRPPrice", 10000))
    except ValueError:
        original_price = 10000
    final_price = original_price + 5000

    # استخراج الميزات
    features = item.get("Description", "") or item.get("Features", "") 
    if not features:
        features = "منتج عالي الجودة ومميز جداً، اطلبه الآن ولا تفوت الفرصة."
    else:
        features = features[:300] + "..." if len(features) > 300 else features

    # تحديد الوسائط (هل هي صورة أم فيديو؟)
    media_list = item.get("Images", [])
    video_list = item.get("Videos", []) 

    media_url = FALLBACK_IMAGE
    is_video = False

    if video_list and isinstance(video_list, list) and video_list[0].get("URL"):
        media_url = video_list[0].get("URL")
        is_video = True
    elif media_list and isinstance(media_list, list) and media_list[0].get("URL"):
        media_url = media_list[0].get("URL")
        if any(ext in media_url.lower() for ext in ['.mp4', '.mov']):
            is_video = True

    if not media_url or ".svg" in media_url.lower() or media_url.startswith("/"):
        media_url = FALLBACK_IMAGE
        is_video = False

    # تجهيز الكابشن والهاشتاقات
    hashtags = "#فد_شي #عراق #بغداد #تسوق_اونلاين #عروض #اكسبلور #تسوق #العراق #بنات_العراق #تخفيضات"
    caption = f"✨ {name} ✨\n\n📌 الميزات:\n{features}\n\n💰 السعر: {final_price} دينار فقط!\n\nللحجز والاستفسار راسلنا على الخاص 📩\n\n{hashtags}"

    # مسار الحفظ المؤقت
    media_path = "temp_video.mp4" if is_video else "temp_post.jpg"

    print(f"🛍️ اسم المنتج: {name}")
    print(f"💵 السعر: {final_price} دينار")

    # تحميل الوسائط
    print("📥 جاري تحميل الوسائط...")
    try:
        media_bytes = requests.get(media_url).content
        with open(media_path, "wb") as f:
            f.write(media_bytes)
        print("✅ تم تحميل الوسائط بنجاح.")
    except Exception as e:
        print(f"❌ فشل التحميل للمنتج الحالي: {e}")
        print("⏭️ جاري التخطي للمنتج التالي...")
        continue # تخطي هذا المنتج إذا فشل التحميل والانتقال للمنتج التالي

    # النشر على انستغرام
    try:
        if is_video:
            print("🎥 جاري نشر الفيديو كـ Reel...")
            cl.clip_upload(media_path, caption)
            print("🎉 تم نشر الـ Reel بنجاح!")
            
            print("⏳ ننتظر دقيقة واحدة (60 ثانية) قبل نشر الستوري...")
            time.sleep(60) # انتظار دقيقة
            
            print("🎥 جاري النشر كـ Story...")
            cl.video_upload_to_story(media_path)
            print("🎉 تم نشر الـ Story بنجاح!")
            
        else:
            print("📸 جاري نشر الصورة كمنشور عادي...")
            cl.photo_upload(media_path, caption)
            print("🎉 تم نشر المنشور بنجاح!")
            
            print("⏳ ننتظر دقيقة واحدة (60 ثانية) قبل نشر الستوري...")
            time.sleep(60) # انتظار دقيقة
            
            print("📸 جاري النشر كـ Story...")
            cl.photo_upload_to_story(media_path)
            print("🎉 تم نشر الـ Story بنجاح!")
        
    except Exception as e:
        print(f"\n❌ حدث خطأ أثناء نشر المنتج رقم {index}: {e}")
    finally:
        # تنظيف الملفات المؤقتة
        if os.path.exists(media_path):
            os.remove(media_path)
            print("🧹 تم حذف ملف الوسائط المؤقت.")

    # انتظار 30 دقيقة قبل المنتج التالي (باستثناء المنتج الأخير)
    if index < len(products):
        print("\n⏳ تم الانتهاء من هذا المنتج. ننتظر 30 دقيقة قبل نشر المنتج التالي...")
        time.sleep(1800) # 1800 ثانية = 30 دقيقة
        print("==========================================\n")

print("\n🎊 تمت العملية بنجاح! تم المرور على جميع المنتجات.")

