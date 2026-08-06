import json

print("🤖 جاري تشغيل بوت الانستغرام...")

try:
    # قراءة الملف مع دعم الحروف العربية لتجنب أخطاء الـ parse
    with open("final_products.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # استخراج المنتجات
    products = data.get("data", {}).get("ListProducts", {}).get("Products", [])
    
    if len(products) > 0:
        print(f"✅ تم العثور على {len(products)} منتجات! جاري تجهيزها...")
        
        for item in products:
            name = item.get("Name", "منتج جديد")
            
            # السعر الأصلي وإضافة الربح (مثلاً 5000 دينار)
            original_price = int(item.get("RRPPrice", 0))
            my_price = original_price + 5000 
            
            # رابط الصورة
            images_list = item.get("Images", [])
            image_url = images_list[0].get("URL") if len(images_list) > 0 else "لا توجد صورة"
            
            print("---------------------------------")
            print(f"📦 اسم المنتج: {name}")
            print(f"💵 السعر النهائي للبيع: {my_price} دينار")
            print(f"🔗 رابط الصورة: {image_url}")
            print("🚀 المنشور جاهز تماماً للرفع على انستغرام!")
            print("---------------------------------")
            
    else:
        print("⚠️ الملف فارغ، لا توجد منتجات للنشر.")
        
except Exception as e:
    print(f"❌ حدث خطأ أثناء تشغيل البوت: {e}")

