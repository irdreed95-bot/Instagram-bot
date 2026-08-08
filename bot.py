import json
import os
import requests
from instagrapi import Client

# ==========================================
# 🔑 الصق مفتاح الجلسة (sessionid) الذي نسخته بين العلامتين أدناه
SESSION_ID = "58780692906%3AZUtwc85clhQdUu%3A21%3AAYjsW1fzKHYuHS2a1Lfa4BeoUdFpqYPerv4gUzRewg"


# ==========================================

print("🚀 جاري الاتصال بانستغرام باستخدام مفتاح الجلسة الآمن...")

FALLBACK_IMAGE = "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop"

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

item = products[0]
name = item.get("Name", "منتج مميز")
try:
    original_price = int(item.get("RRPPrice", 10000))
except ValueError:
    original_price = 10000

final_price = original_price + 5000  # إضافة الربح

images_list = item.get("Images", [])
img_url = images_list[0].get("URL") if images_list else FALLBACK_IMAGE

if not img_url or ".svg" in img_url.lower() or img_url.startswith("/"):
    img_url = FALLBACK_IMAGE

print(f"📦 المنتج: {name}")
print(f"💵 السعر بعد الربح: {final_price} دينار")

img_path = "temp_post.jpg"
try:
    img_bytes = requests.get(img_url).content
    with open(img_path, "wb") as f:
        f.write(img_bytes)
    print("📥 تم تحميل صورة المنتج بنجاح.")
except Exception as e:
    print(f"❌ فشل تحميل الصورة: {e}")
    exit()

cl = Client()
try:
    # استخدام Session ID يتجاوز الحظر تماماً
    cl.login_by_sessionid(SESSION_ID)
    
    caption = f"✨ {name} ✨\n\n💰 السعر: {final_price} دينار\n\n📌 للحجز والاستفسار راسلنا على الخاص!"
    
    cl.photo_upload(img_path, caption)
    print("\n🎉🎉🎉 تم نشر المنشور بنجاح على حسابك في الانستغرام بدون أي مشاكل!")
    
except Exception as e:
    print(f"\n❌ حدث خطأ: {e}")
finally:
    if os.path.exists(img_path):
        os.remove(img_path)

