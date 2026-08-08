import json
import os
import requests
import time
from instagrapi import Client

# ==========================================
# 🔑 الإعدادات الأساسية
SESSION_ID = "48878484782%3AB0HBPJKQa0M5m2%3A16%3AAYhhbnzsaAMH0uihHHL6-MWUcXVPpCNU3Xol9-v43Q"

# 📩 اكتب يوزر حسابك (اللي تريد البوت يدزله رسالة من ينشر منتج)
ADMIN_USERNAME = "d_d3.d" 
# ==========================================

print("🚀 جاري الاتصال بانستغرام...")
cl = Client()

try:
    print("⏳ جاري تسجيل الدخول...")
    cl.login_by_sessionid(SESSION_ID)
    print("✅ تم الاتصال بحساب الانستغرام بنجاح تام!")
except Exception as e:
    print(f"❌ فشل تسجيل الدخول: {e}")
    exit()

# محاولة جلب الآي دي الخاص بحسابك لإرسال الرسائل له
try:
    admin_user_id = cl.user_id_from_username(ADMIN_USERNAME)
    print(f"✅ تم العثور على حساب المشرف: {ADMIN_USERNAME}")
except Exception as e:
    print("⚠️ لم يتم العثور على حساب المشرف، تأكد من كتابة اليوزر بشكل صحيح. لن يتم إرسال رسائل التنبيه.")
    admin_user_id = None

# قراءة بيانات المنتجات
try:
    with open("final_products.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    products = data.get("data", {}).get("ListProducts", {}).get("Products", [])
except Exception:
    products = []

if not products:
    print("❌ لم يتم العثور على منتجات في الملف.")
    exit()

print(f"\n📦 تم العثور على {len(products)} منتج، سيتم البدء بالنشر (منتج كل 30 دقيقة)...\n")

# حلقة المرور على جميع المنتجات
for index, item in enumerate(products, start=1):
    print(f"--- 🔄 البدء بالمنتج رقم {index} من {len(products)} ---")
    
    name = item.get("Name", "منتج مميز")
    
    # حساب السعر
    try:
        original_price = int(item.get("RRPPrice", 10000))
    except ValueError:
        original_price = 10000
    final_price = original_price + 5000

    # 🌟 الوصف المغري والجديد (تم إلغاء الوصف القديم المخربط)
    hashtags = "#تسوق_اونلاين #العراق #بغداد #اكسبلور #عروض #شروة #تخفيضات #تسوق #بنات_العراق #فد_شي"
    caption = f"🔥 متوفر الآن: {name} 🔥\n\n✨ تميز بأفضل جودة وأرقى تصميم!\n\n💰 السعر: {final_price} دينار عراقي فقط.\n🚚 تتوفر خدمة التوصيل لجميع محافظات العراق.\n\n👇 للحجز والاستفسار، راسلنا على الخاص مباشرة!\n\n{hashtags}"

    # تجهيز الصور
    media_list = item.get("Images", [])
    downloaded_files = []
    
    print(f"🛍️ اسم المنتج: {name}")
    print("📥 جاري تحميل صور المنتج...")

    # تحميل الصور (بحد أقصى 10 صور لأن انستغرام ما يقبل أكثر بالبوست الواحد)
    count = 0
    for img in media_list:
        if count >= 10: 
            break
            
        url = img.get("URL", "")
        if url and "http" in url and not url.endswith(".svg"):
            try:
                img_path = f"temp_img_{index}_{count}.jpg"
                response = requests.get(url)
                with open(img_path, "wb") as f:
                    f.write(response.content)
                downloaded_files.append(img_path)
                count += 1
            except Exception as e:
                pass

    if not downloaded_files:
        print("⚠️ لم يتم العثور على صور صالحة لهذا المنتج، سيتم تخطيه.")
        continue

    # 🚀 عملية النشر
    try:
        if len(downloaded_files) > 1:
            print(f"📸 جاري نشر ألبوم مكون من {len(downloaded_files)} صور...")
            cl.album_upload(downloaded_files, caption)
        else:
            print("📸 جاري نشر صورة واحدة...")
            cl.photo_upload(downloaded_files[0], caption)
            
        print("🎉 تم نشر البوست بنجاح!")
        
        print("⏳ ننتظر 15 ثانية قبل نشر الستوري...")
        time.sleep(15)
        
        print("🎥 جاري نشر الستوري (الصورة الأولى)...")
        cl.photo_upload_to_story(downloaded_files[0], f"🔥 {name}\nبسعر {final_price} دينار فقط! 🔥")
        print("🎉 تم نشر الستوري بنجاح!")
        
        # 📩 إرسال رسالة لحسابك الشخصي
        if admin_user_id:
            print(f"📩 جاري إرسال تنبيه إلى {ADMIN_USERNAME}...")
            dm_text = f"✅ البوت نشر منتج جديد!\n\nالاسم: {name}\nالسعر: {final_price}\n\nجهز نفسك للطلبات 🚀"
            cl.direct_send(dm_text, [admin_user_id])
            print("✉️ تم إرسال الرسالة بنجاح.")

    except Exception as e:
        print(f"\n❌ حدث خطأ أثناء النشر: {e}")
        
    finally:
        # 🧹 تنظيف الذاكرة ومسح الصور المؤقتة
        for file in downloaded_files:
            if os.path.exists(file):
                os.remove(file)
        print("🧹 تم حذف ملفات الصور المؤقتة.")

    # ⏱️ الانتظار 30 دقيقة قبل المنتج التالي (إلا إذا كان آخر منتج)
    if index < len(products):
        print("\n⏳ تم الانتهاء من هذا المنتج. البوت سينتظر 30 دقيقة (1800 ثانية) قبل نشر المنتج التالي...")
        time.sleep(1800)
        print("==========================================\n")

print("\n🎊 تمت العملية بنجاح! تم المرور على جميع المنتجات.")

