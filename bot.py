import json
import os
import requests
import time
import random
from pathlib import Path
from instagrapi import Client

# ==========================================
# 🔑 الإعدادات الأساسية
SESSION_ID = "48878484782%3AB0HBPJKQa0M5m2%3A16%3AAYhhbnzsaAMH0uihHHL6-MWUcXVPpCNU3Xol9-v43Q"
ADMIN_USERNAME = "d_d3.d" 

# 🎵 كلمات البحث عن الأغاني (البوت راح يختار وحدة عشوائياً كل مرة)
MUSIC_KEYWORDS = ["ترند عراقي", "ريمكس", "عروض", "حماسي", "اغاني ترند"]
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

try:
    admin_user_id = cl.user_id_from_username(ADMIN_USERNAME)
except Exception as e:
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

print(f"\n📦 تم العثور على {len(products)} منتج، سيتم البدء بالنشر...\n")

for index, item in enumerate(products, start=1):
    print(f"--- 🔄 البدء بالمنتج رقم {index} من {len(products)} ---")
    
    name = item.get("Name", "منتج مميز")
    
    try:
        original_price = int(item.get("RRPPrice", 10000))
    except ValueError:
        original_price = 10000
    final_price = original_price + 5000

    hashtags = "#تسوق_اونلاين #العراق #بغداد #اكسبلور #عروض #شروة #تخفيضات #تسوق #بنات_العراق #فد_شي"
    caption = f"🔥 متوفر الآن: {name} 🔥\n\n✨ تميز بأفضل جودة وأرقى تصميم!\n\n💰 السعر: {final_price} دينار عراقي فقط.\n🚚 تتوفر خدمة التوصيل لجميع محافظات العراق.\n\n👇 للحجز والاستفسار، راسلنا على الخاص مباشرة!\n\n{hashtags}"

    media_list = item.get("Images", [])
    downloaded_files = []
    
    print("📥 جاري تحميل صور المنتج...")
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
        continue

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
        
        # ==========================================
        # 🎵 إضافة الأغنية للستوري
        # ==========================================
        try:
            print("🎵 جاري البحث عن مقطع موسيقي للستوري...")
            # اختيار كلمة بحث عشوائية من القائمة
            random_keyword = random.choice(MUSIC_KEYWORDS)
            
            # البحث عن الأغنية في انستغرام
            track = cl.search_music(random_keyword)[0]
            print(f"🎶 تم العثور على الأغنية: {track.title} - {track.display_artist}")
            
            print("🎥 جاري نشر الستوري مع الأغنية...")
            # دمج الصورة مع الأغنية ونشرها
            cl.photo_upload_to_story_with_music(
                path=Path(downloaded_files[0]),  
                caption=f"🔥 {name}\nبسعر {final_price} دينار فقط! 🔥",
                track=track,
                duration=15.0 # مدة الستوري 15 ثانية
            )
            print("🎉 تم نشر الستوري مع الموسيقى بنجاح!")
            
        except Exception as music_e:
            print(f"⚠️ فشل إضافة الموسيقى (سيتم النشر بدونها). السبب: {music_e}")
            print("🎥 جاري نشر الستوري كصورة عادية...")
            cl.photo_upload_to_story(downloaded_files[0], f"🔥 {name}\nبسعر {final_price} دينار فقط! 🔥")
            print("🎉 تم نشر الستوري بنجاح!")
        # ==========================================
        
        if admin_user_id:
            dm_text = f"✅ البوت نشر منتج جديد!\n\nالاسم: {name}\nالسعر: {final_price}\n\nجهز نفسك للطلبات 🚀"
            cl.direct_send(dm_text, [admin_user_id])
            print("✉️ تم إرسال رسالة التنبيه بنجاح.")

    except Exception as e:
        print(f"\n❌ حدث خطأ أثناء النشر: {e}")
        
    finally:
        for file in downloaded_files:
            if os.path.exists(file):
                os.remove(file)

    if index < len(products):
        print("\n⏳ ننتظر 30 دقيقة قبل المنتج التالي...")
        time.sleep(1800)

print("\n🎊 تمت العملية بنجاح! تم المرور على جميع المنتجات.")

