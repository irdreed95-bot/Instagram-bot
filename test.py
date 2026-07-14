import requests
import json
import re

print("🚀 يارب نحقق الحلم! جاري سحب البيانات مباشرة من الموقع بذكاء...")

url = "https://web.fedshi.com/"

# التنكر كمتصفح حقيقي (Google Chrome) لتجاوز حماية الموقع
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "ar,en-US;q=0.9,en;q=0.8"
}

try:
    # إرسال الطلب للموقع
    response = requests.get(url, headers=headers, timeout=15)
    html_content = response.text

    # حفظ الصفحة للاحتياط عشان نشوفها إذا صار شي
    with open("live_page.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✅ تم سحب الصفحة الحية بنجاح! جاري البحث عن المنتجات...")

    # البحث عن بيانات Next.js المخفية
    match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html_content, re.DOTALL)

    if match:
        print("🎉 الله! لقينا الكنز الحقيقي (__NEXT_DATA__)!")
        json_data = json.loads(match.group(1))
        
        # حفظ البيانات بملف جديد
        with open("fedshi_data.json", "w", encoding="utf-8") as out:
            json.dump(json_data, out, ensure_ascii=False, indent=2)
        
        print("💾 تم حفظ جميع بيانات الموقع في ملف 'fedshi_data.json'.")
        
        # عرض بعض الأقسام للتأكد
        print("\n🛒 عينة من الأقسام الموجودة:")
        props = json_data.get("props", {}).get("pageProps", {})
        for key in props.keys():
            print(f" 🔹 {key}")
            
        print("\n✅ الحلم صار قريب جداً، الخطوة الجاية بس نصفي المنتجات!")
    else:
        print("⚠️ الموقع لا زال يخفي البيانات أو يحملها بطريقة مختلفة.")
        print("بس لا تيأس! حفظنا محتوى الصفحة بملف 'live_page.html'.")
        print("\n👀 نظرة سريعة على ما أرجعه الموقع:")
        # نعرض أول 500 حرف لنعرف سبب المشكلة (هل هي حماية Cloudflare مثلاً؟)
        print(html_content[:500])

except Exception as e:
    print(f"❌ حدث خطأ بالاتصال: {e}")
    
