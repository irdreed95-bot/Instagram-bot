import json

print("🕵️‍♂️ جاري فحص خريطة السيرفر (Schema) لاكتشاف ثغرة تسجيل الدخول...")

try:
    with open("graphql_schema.json", "r", encoding="utf-8") as f:
        schema_data = json.load(f)
        
        # استخراج أنواع البيانات من الخريطة
        types = schema_data.get("data", {}).get("__schema", {}).get("types", [])
        
        # البحث عن دوال الـ Mutation (الدوّال المسؤولة عن تسجيل الدخول)
        mutation_found = False
        for t in types:
            if t.get("name") in ["Mutation", "RootMutationType"]:
                fields = t.get("fields", [])
                for field in fields:
                    name = field.get("name", "").lower()
                    if "login" in name or "auth" in name or "signin" in name or "token" in name:
                        print(f"\n🎉 لقينا دالة الدخول المخفية واسمها: {field['name']}")
                        args = field.get("args", [])
                        print("👇 السيرفر يطلب من عندنا هاي المعلومات حتى يعطينا الدخول:")
                        for arg in args:
                            arg_type = arg.get("type", {})
                            while arg_type.get("ofType"):
                                arg_type = arg_type.get("ofType")
                            print(f"  - محتاج: {arg.get('name')} (النوع: {arg_type.get('name')})")
                        mutation_found = True
                        
        if not mutation_found:
            print("\n⚠️ ما لقينا دالة الدخول المباشرة، السيرفر قد يستخدم طريقة ثانية.")
            
except Exception as e:
    print(f"❌ خطأ بقراءة الملف: {e}")

