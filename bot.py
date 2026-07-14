import os
import requests
from bs4 import BeautifulSoup
from instagrapi import Client
import time
import random

# --- الثوابت وإعدادات البوت ---
# رابط القسم اللي تريد تسحب منه في "فد شي" (مثال: قسم العطور)
FADSHI_CATEGORY_URL = "أدخل_رابط_قسم_المنتجات_هنا" 

# أسماء الكلاسات (Classes) لعناصر HTML من تطبيق/موقع "فد شي"
# !!هذه مجرد أمثلة وتحتاج إلى تحديث بناءً على الموقع الفعلي!!
FADSHI_PRODUCT_ITEM_CLASS = "product-item"
FADSHI_PRODUCT_TITLE_CLASS = "product-title"
FADSHI_PRODUCT_PRICE_CLASS = "product-price"
FADSHI_PRODUCT_IMAGE_CLASS = "product-image"

# ملف لحفظ معرفات المنتجات التي تم نشرها سابقاً
POSTED_IDS_FILE = "posted_ids.txt"

# --- دالة حساب السعر الجديد (معادلة الربح الذكي) ---
def calculate_new_price(original_price):
    if original_price < 15000:
        return original_price + 4000
    elif 15000 <= original_price <= 50000:
        return original_price + 8000
    else:
        return original_price + 15000

# --- دالة سحب بيانات المنتجات من "فد شي" ---
def scrape_new_product(url):
    try:
        response = requests.get(url)
        response.raise_for_status() # التأكد من نجاح الطلب
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # البحث عن أول منتج لم يتم نشره بعد
        product_items = soup.find_all(class_=FADSHI_PRODUCT_ITEM_CLASS)
        
        # قراءة المعرفات المنشورة سابقاً
        posted_ids = []
        if os.path.exists(POSTED_IDS_FILE):
            with open(POSTED_IDS_FILE, 'r') as f:
                posted_ids = [line.strip() for line in f.readlines()]
                
        for product in product_items:
            # افتراضاً، سنستخدم رابط الصورة كمعرف فريد
            image_url = product.find('img', class_=FADSHI_PRODUCT_IMAGE_CLASS)['src']
            
            if image_url not in posted_ids:
                # سحب بيانات المنتج
                title = product.find(class_=FADSHI_PRODUCT_TITLE_CLASS).get_text(strip=True)
                price_text = product.find(class_=FADSHI_PRODUCT_PRICE_CLASS).get_text(strip=True)
                
                # استخراج السعر كقيمة رقمية (مثال: "25,000 د.ع" -> 25000)
                # !!هذه الخطوة تحتاج إلى تعديل بناءً على تنسيق السعر في الموقع!!
                original_price = int(''.join(filter(str.isdigit, price_text)))
                
                new_price = calculate_new_price(original_price)
                
                # إعداد الوصف النهائي (Caption)
                caption = f"✨ {title} ✨\n\n💰 السعر: {new_price:,} د.ع\n\n#تسوق_الكتروني #فد_شي #عروض #العراق"
                
                return {
                    'image_url': image_url,
                    'title': title,
                    'original_price': original_price,
                    'new_price': new_price,
                    'caption': caption
                }
                
        print("لا توجد منتجات جديدة للنشر.")
        return None
        
    except Exception as e:
        print(f"حدث خطأ أثناء سحب البيانات: {e}")
        return None

# --- دالة النشر على إنستكرام ---
def post_to_instagram(product_data, credentials):
    try:
        cl = Client()
        
        # استخدام ملف كوكيز (Cookies) لتجنب تسجيل الدخول المتكرر (مهم للحظر)
        cookies_file = "instagram_cookies.json"
        if os.path.exists(cookies_file):
            cl.load_settings(cookies_file)
            print("تم تحميل إعدادات الكوكيز.")
            
        print("جاري تسجيل الدخول...")
        cl.login(credentials['username'], credentials['password'])
        
        if not os.path.exists(cookies_file):
            cl.dump_settings(cookies_file) # حفظ الكوكيز بعد أول تسجيل دخول ناجح
            print("تم حفظ إعدادات الكوكيز.")
            
        print("جاري تحميل الصورة ونشر البوست...")
        
        # تحميل الصورة ونشر البوست
        photo_path = cl.photo_upload(
            product_data['image_url'], # يمكن استخدام رابط الصورة مباشرة
            product_data['caption']
        )
        
        print("تم نشر البوست بنجاح!")
        
        # إضافة معرف المنتج (رابط الصورة) إلى قائمة المنشور سابقاً
        with open(POSTED_IDS_FILE, 'a') as f:
            f.write(f"{product_data['image_url']}\n")
            
        return True
        
    except Exception as e:
        print(f"حدث خطأ أثناء النشر على إنستكرام: {e}")
        # إذا فشل النشر، يجب حذف الكوكيز لإعادة تسجيل الدخول بالمرة القادمة
        if os.path.exists(cookies_file):
            os.remove(cookies_file)
        return False

# --- الوظيفة الرئيسية لتشغيل البوت ---
def main():
    # !!من المهم جداً عدم وضع بيانات الاعتماد هنا مباشرة في الكود النهائي!!
    # !!استخدم متقيرات البيئة (Environment Variables) للحماية!!
    instagram_credentials = {
        'username': 'اسم_حسابك_هنا',
        'password': 'كلمة_سر_حسابك_هنا'
    }

    print("جاري سحب بيانات منتج جديد...")
    product_data = scrape_new_product(FADSHI_CATEGORY_URL)
    
    if product_data:
        print(f"تم العثور على منتج: {product_data['title']}")
        print(f"السعر الأصلي: {product_data['original_price']:,} د.ع")
        print(f"السعر الجديد: {product_data['new_price']:,} د.ع")
        
        print("جاري النشر على إنستكرام...")
        # إضافة تأخير عشوائي قبل النشر لتقليل خطر الحظر
        delay = random.randint(30, 60)
        print(f"الانتظار {delay} ثانية...")
        time.sleep(delay)
        
        success = post_to_instagram(product_data, instagram_credentials)
        
        if success:
            print("اكتملت العملية بنجاح.")
        else:
            print("فشلت عملية النشر.")
    else:
        print("لا توجد منتجات جديدة للعمل عليها.")

if __name__ == "__main__":
    main()
  
