import json
import os
import requests
import time
from instagrapi import Client

# ==========================================
# بيانات تسجيل الدخول الخاصة بك
USERNAME = "dr_e3.7"
PASSWORD = "DREED123456"
# ==========================================

FALLBACK_IMAGE = "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop"

print("🚀 جاري الاتصال بانستغرام...")

cl = Client()

# 1. نظام تسجيل الدخول الذكي (يعالج مشكلة طلب الموافقة من الهاتف)
try:
    cl.login(USERNAME, PASSWORD)
    print("✅ تم الاتصال بحساب الانستغرام بنجاح!")
except Exception as e:
    error_msg = str(e).lower()
    
    # إذا طلب انستغرام الموافقة من الهاتف (Challenge)
    if "challenge_required" in error_msg or "challenge" in error_msg or "suspicious" in error_msg:
        print("\n⚠️ انستغرام يطلب التحقق من هويتك!")
        print("📱 يرجى فتح تطبيق انستغرام في هاتفك الآن.")
        print("👆 ستجد رسالة 'هل تحاول تسجيل الدخول؟' (Was this you?). اضغط على 'نعم، هذا أنا'.")
        print("⏳ البوت سينتظر لمدة 60 ثانية لكي تقوم بالموافقة...")
        
        time.sleep(60) # الكود يتوقف هنا لمدة دقيقة بانتظار موافقتك
        
        print("\n🔄 جاري محاولة تسجيل الدخول مرة أخرى بعد الموافقة...")
        try:
            cl.login(USERNAME, PASSWORD)
            print("✅ تم الاتصال بنجاح بعد التحقق!")
        except Exception as e2:
            print(f"❌ فشل تسجيل الدخول مجدداً، يرجى إعادة تشغيل الكود: {e2}")
            exit()
            
    # إذا كان الحساب مربوطاً برقم هاتف أو تطبيق مصادقة ثنائية (2FA)
    elif "two_factor" in error_msg or "2fa" in error_msg or "two factor" in error_msg:
        print("\n🔐 حسابك محمي بالمصادقة الثنائية (Two-Factor Authentication).")
        code = input("👉 يرجى كتابة الكود المكون من 6 أرقام الذي وصلك الآن واضغط Enter: ")
        try:
            cl.login(USERNAME, PASSWORD, verification_code=code)
            print("✅ تم الاتصال بنجاح!")
        except Exception as e3:
            print(f"❌ الكود خاطئ أو فشل الاتصال: {e3}")
            exit()
            
    else:
        print(f"❌ فشل تسجيل الدخول لسبب آخر: {e}")
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

print(f"\n📦 تم العثور على {len(products)} منتجات، سيتم البدء بالنشر...\n")

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

    # تحديد الوسائط
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

    media_path = "temp_video.mp4" if is_video else "temp_post.jpg"

    print(f"🛍️ اسم المنتج: {name}")
    print(f"💵 السعر: {final_price} دينار")

    print("📥 جاري تحميل الوسائط...")
    try:
        media_bytes = requests.get(media_url).content
        with open(media_path, "wb") as f:
            f.write(media_bytes)
        print("✅ تم تحميل الوسائط بنجاح.")
    except Exception as e:
        print(f"❌ فشل التحميل للمنتج الحالي: {e}")
        continue 

    # النشر على انستغرام
    try:
        if is_video:
            print("🎥 جاري نشر الفيديو كـ Reel...")
            cl.clip_upload(media_path, caption)
            print("🎉 تم نشر الـ Reel بنجاح!")
            
            print("⏳ ننتظر 60 ثانية قبل نشر الستوري...")
            time.sleep(60) 
            
            print("🎥 جاري النشر كـ Story...")
            cl.video_upload_to_story(media_path)
            print("🎉 تم نشر الـ Story بنجاح!")
            
        else:
            print("📸 جاري نشر الصورة كمنشور عادي...")
            cl.photo_upload(media_path, caption)
            print("🎉 تم نشر المنشور بنجاح!")
            
            print("⏳ ننتظر 60 ثانية قبل نشر الستوري...")
            time.sleep(60) 
            
            print("📸 جاري النشر كـ Story...")
            cl.photo_upload_to_story(media_path)
            print("🎉 تم نشر الـ Story بنجاح!")
        
    except Exception as e:
        print(f"\n❌ حدث خطأ أثناء نشر المنتج رقم {index}: {e}")
    finally:
        if os.path.exists(media_path):
            os.remove(media_path)
            print("🧹 تم حذف ملف الوسائط المؤقت.")

    if index < len(products):
        print("\n⏳ تم الانتهاء من هذا المنتج. ننتظر 30 دقيقة قبل نشر المنتج التالي...")
        time.sleep(1800) 
        print("==========================================\n")

print("\n🎊 تمت العملية بنجاح! تم المرور على جميع المنتجات.")

