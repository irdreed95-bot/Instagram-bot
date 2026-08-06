import json
import os
import requests
from instagrapi import Client

# ==========================================
# ⚠️ ضع معلومات حساب الانستغرام الخاص بك هنا
USERNAME = "يوزر_حسابك_هنا"
PASSWORD = "باسوورد_حسابك_هنا"
BASE_WEBSITE_URL = "https://www.example.com" # ضع رابط الموقع الأصلي هنا إذا كان الرابط المستخرج ناقص
# ==========================================

print("🤖 جاري تشغيل بوت الانستغرام...")

try:
    # قراءة المنتجات
    with open("final_products.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    products = data.get("data", {}).get("ListProducts", {}).get("Products", [])
    
    if len(products) > 0:
        item = products[0] # راح نجرب ننشر أول منتج فقط
        name = item.get("Name", "منتج جديد")
        original_price = int(item.get("RRPPrice", 0))
        my_price = original_price + 5000 
        
        images_list = item.get("Images", [])
        image_url = images_list[0].get("URL") if len(images_list) > 0 else ""

        # تعديل الرابط إذا كان يبدأ بـ / (رابط نسبي)
        if image_url.startswith("/"):
            image_url = BASE_WEBSITE_URL + image_url
        
        # فحص صيغة الصورة
        if ".svg" in image_url.lower():
            print(f"⚠️ الصورة المستخرجة بصيغة SVG ولا تصلح للنشر.")
            print(f"الرابط: {image_url}")
            print("الانستغرام يقبل الصور بصيغة JPG أو PNG فقط. افتح ملف final_products.json وغير الرابط بصورة حقيقية لتجربة النشر.")
        else:
            print(f"📦 جاري تحميل صورة المنتج: {name}")
            
            # تحميل الصورة مؤقتاً للنشر
            img_data = requests.get(image_url).content
            img_path = "temp_image.jpg"
            with open(img_path, 'wb') as handler:
                handler.write(img_data)
            
            # تسجيل الدخول والنشر
            print("⏳ جاري تسجيل الدخول للانستغرام... (قد يستغرق بضع ثواني)")
            cl = Client()
            cl.login(USERNAME, PASSWORD)
            
            caption = f"🔥 {name} 🔥\n\nالسعر: {my_price} دينار فقط!\n\n#تسوق #عروض #منتجات"
            
            print("🚀 جاري رفع المنشور...")
            cl.photo_upload(img_path, caption)
            
            print("✅ تم النشر بنجااااااح على انستغرام!")
            
            # تنظيف الملفات المؤقتة
            if os.path.exists(img_path):
                os.remove(img_path)
            
    else:
        print("⚠️ الملف فارغ، لا توجد منتجات للنشر.")
        
except Exception as e:
    print(f"❌ حدث خطأ: {e}")

