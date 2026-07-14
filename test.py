import json
import os

print("🔍 جاري قراءة وتحليل ملف next_data.json المحلي لاستخراج المنتجات...")

# التأكد من وجود الملف محلياً
if not os.path.exists("next_data.json"):
    print("❌ لم يتم العثور على ملف next_data.json.")
    print("يرجى التأكد من تشغيل السكربت في المجلد الصحيح.")
    exit()

try:
    with open("next_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    products_found = []
    
    # دالة ذكية للبحث عن قوائم المنتجات داخل الـ JSON
    def search_deep(node, current_path=""):
        if isinstance(node, dict):
            for k, v in node.items():
                # البحث عن كلمات مفتاحية تدل على المنتجات
                if k.lower() in ["products", "items", "productlist", "data_list", "rows"]:
                    if isinstance(v, list) and len(v) > 0:
                        products_found.append((current_path + f" -> {k}", v))
                search_deep(v, current_path + f" -> {k}")
        elif isinstance(node, list):
            for i, item in enumerate(node):
                search_deep(item, current_path + f"[{i}]")

    search_deep(data)

    if products_found:
        print(f"\n🎉 تم اكتشاف {len(products_found)} قائمة منتجات بنجاح داخل الملف!")
        for path, plist in products_found:
            print(f"\n📌 المسار داخل الملف: {path}")
            print(f"📦 عدد المنتجات المتوفرة: {len(plist)}")
            print("-" * 50)
            
            # طباعة عينة من المنتجات لتراها بعينك
            for index, prod in enumerate(plist[:5]):  # طباعة أول 5 منتجات
                print(f"🔹 المنتج {index + 1}:")
                if isinstance(prod, dict):
                    name = prod.get("name") or prod.get("title") or prod.get("arName") or "بدون اسم"
                    price = prod.get("price") or prod.get("wholesalePrice") or "غير محدد"
                    sku = prod.get("sku") or prod.get("id") or "لا يوجد ID"
                    print(f"   - الاسم: {name}")
                    print(f"   - السعر: {price}")
                    print(f"   - الكود (ID): {sku}")
                else:
                    print(f"   - تفاصيل: {prod}")
            print("-" * 50)
    else:
        print("\n⚠️ لم نجد هيكل منتجات بالأسماء القياسية، سنعرض لك محتوى الملف الأساسي:")
        print("=" * 50)
        print(json.dumps(data, indent=2, ensure_ascii=False)[:1200])
        print("=" * 50)

except Exception as e:
    print(f"❌ حدث خطأ أثناء قراءة البيانات: {e}")
    
