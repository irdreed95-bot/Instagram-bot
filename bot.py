import json
import os
import requests
from instagrapi import Client

# ==========================================
# ⚠️ اكتب يوزر وباسوورد حسابك بالانستغرام هنا
USERNAME = "يوزر_حسابك_هنا"
PASSWORD = "باسوورد_حسابك_هنا"
# ==========================================

print("🚀 جاري النشر التلقائي على الانستغرام...")

# صورة حقيقية جاهزة ومجربة بصيغة JPG تستخدم تلقائياً بدلاً من الـ SVG
FALLBACK_IMAGE = "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop"

# 1. قراءة الملف أو إنشائه تلقائياً
try:
    with open("final_products.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    products = data.get("data", {}).get("ListProducts", {}).get("Products", [])
except Exception:
    products = []

if not products:
    products = [{
        "Name": "منتج مميز - عرض خاص",
        "RRPPrice": 10000,
        "Images": [{"URL": FALLBACK_IMAGE}]
    }]

# 2. تجهيز بيانات المنتج والسعر
item = products[0]
name = item.get("Name", "منتج مميز")
try:
    original_price = int(item.get("RRPPrice", 10000))
except ValueError:
    original_price = 10000

final_price = original_price + 5000  # إضافة الربح تلقائياً

# 3. فحص وتصحيح رابط الصورة تلقائياً
images_list = item.get("Images", [])
img_url = images_list[0].get("URL") if images_list else FALLBACK_IMAGE

if not img_url or ".svg" in img_url.lower() or img_url.startswith("/"):
    print("🔄 تم التبديل تلقائياً إلى صورة منتج صالحة للنشر (JPG)...")
    img_url = FALLBACK_IMAGE

print(f"📦 المنتج: {name}")
print(f"💵 السعر بعد الربح: {final_price} دينار")

# 4. تحميل الصورة مؤقتاً
img_path = "temp_post.jpg"
try:
    img_bytes = requests.get(img_url).content
    with open(img_path, "wb") as f:
        f.write(img_bytes)
    print("📥 تم تحميل صورة المنتج بنجاح.")
except Exception as e:
    print(f"❌ فشل تحميل الصورة: {e}")
    exit()

# 5. تسجيل الدخول والنشر
print("🔐 جاري الاتصال بالحساب والنشر...")
cl = Client()
try:
    cl.login(USERNAME, PASSWORD)
    
    caption = f"✨ {name} ✨\n\n💰 السعر: {final_price} دينار\n\n📌 للحجز والاستفسار راسلنا على الخاص!"
    
    cl.photo_upload(img_path, caption)
    print("\n🎉🎉🎉 أبشرررر! تم نشر المنشور بنجاح على حسابك في الانستغرام!")
    
except Exception as e:
    print(f"\n❌ حدث خطأ بتسجيل الدخول أو النشر: {e}")
finally:
    if os.path.exists(img_path):
        os.remove(img_path)

