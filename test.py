import json

print("🕵️‍♂️ جاري التفتيش الشامل داخل الخريطة (بدون الاعتماد على ترتيب السيرفر)...")

def find_login_info(obj):
    # دالة تبحث بكل زوايا الملف عن أي شي بي تسجيل دخول
    if isinstance(obj, dict):
        name = obj.get("name")
        if isinstance(name, str) and any(x in name.lower() for x in ["login", "auth", "signin", "token"]):
            print(f"\n🎉 لقينا ثغرة الدخول! اسمها: {name}")
            args = obj.get("args")
            if args:
                print("👇 السيرفر يطلب هاي المعلومات حتى نسجل دخول:")
                for arg in args:
                    print(f"  - محتاج: {arg.get('name')}")
        
        # كمل بحث بالباقي
        for value in obj.values():
            find_login_info(value)
            
    elif isinstance(obj, list):
        for item in obj:
            find_login_info(item)

try:
    with open("graphql_schema.json", "r", encoding="utf-8") as f:
        schema_data = json.load(f)
        find_login_info(schema_data)
        print("\n✅ انتهى الفحص الشامل!")
except Exception as e:
    print(f"❌ خطأ: {e}")

