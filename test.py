from bs4 import BeautifulSoup
import json
import os

print("🔍 جاري قراءة المنتجات مباشرة من ملف الموقع المحفوظ...")

# التأكد من وجود ملف الصفحة
html_file = "live_page.html"
if not os.path.exists(html_file):
    html_file = "page_source.html"

if not os.path.exists(html_file):
    print("❌ لم يتم العثور على ملف HTML في القائمة الجانبية.")
    exit()

with open(html_file, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

products_list = []

# استخراج المنتجات
items = soup.find_all(['div', 'article', 'li'])

counter = 1
for item in items:
    # محاولة البحث عن اسم المنتج، السعر، والصورة
    img_tag = item.find('img')
    if img_tag and (img_tag.get('src') or img_tag.get('data-src')):
        img_url = img_tag.get('src') or img_tag.get('data-src')
        
        # محاولة إيجاد النص (الاسم)
        text_content = item.get_text(strip=True)
        if len(text_content) > 3:
            # هنا صلحنا الخطأ المطبعي ومسحنا السطر الغلط
            products_list.append({
                "ID": str(counter),
                "Name": text_content[:50], # أخذ أول 50 حرف كاسم للمنتج
                "RRPPrice": "10000", # سعر افتراضي
                "Images": [{"URL": img_url}]
            })
            counter += 1

if len(products_list) > 0:
    final_data = {
        "data": {
            "ListProducts": {
                "Products": products_list
            }
        }
    }
    with open("final_products.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    print(f"\n🎉 تم استخراج {len(products_list)} منتج بنجاح وحفظها في final_products.json!")
else:
    print("⚠️ لم يتم العثور على منتجات بالطريقة التقليدية، جاري إنشاء بيانات تجريبية لننتقل للانستغرام فوراً.")
    dummy_data = {
        "data": {
            "ListProducts": {
                "Products": [
                    {
                        "ID": "1",
                        "Name": "منتج تجريبي من البوت",
                        "RRPPrice": "15000",
                        "Images": [{"URL": "https://via.placeholder.com/600"}]
                    }
                ]
            }
        }
    }
    with open("final_products.json", "w", encoding="utf-8") as f:
        json.dump(dummy_data, f, ensure_ascii=False, indent=2)
    print("✅ تم إنشاء ملف final_products.json بنجاح وجاهز للربط!")

