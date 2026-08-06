import requests
import json
import re

url = "https://web-api.app.fedshi.com/query"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

print("🚀 جاري الفحص الذكي التلقائي لحقل الصور...")

# قائمة بالأسماء المركبة الشائعة في GraphQL
candidates = [
    "FileUrl", "fileUrl", "FullUrl", "fullUrl", "FileName", "fileName", 
    "Name", "name", "Key", "key", "Location", "location", "URI", "uri", 
    "Source", "source", "FilePath", "filePath", "OriginalUrl", "originalUrl",
    "FileLocation", "ImageLocation"
]

success = False

for field in candidates:
    payload = {
        "query": f"query {{ ListProducts(Request: {{ Page: 1 }}) {{ Products {{ ID Name RRPPrice Images {{ {field} }} }} }} }}"
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload)
        data = res.json()
        
        # 1. إذا نجح الكود بدون أي أخطاء
        if "errors" not in data and data.get("data"):
            print(f"\n🎉🎉🎉 أبشرررر! الكلمة الصحيحة لرابط الصورة هي: {field}")
            with open("final_products.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("✅ تم سحب المنتجات كاملة وحفظها بملف final_products.json!")
            success = True
            break
            
        # 2. إذا طلع خطأ، البايثون راح يبحث بداخل الخطأ عن اقتراح "Did you mean"
        errors_str = json.dumps(data.get("errors", []))
        match = re.search(r'Did you mean [\\"]*([^"\\]+)[\\"]*\?', errors_str)
        if match:
            suggested = match.group(1)
            print(f"💡 السيرفر اقترح كلمة: {suggested}! جاري التجربة فوراً...")
            
            p_payload = {
                "query": f"query {{ ListProducts(Request: {{ Page: 1 }}) {{ Products {{ ID Name RRPPrice Images {{ {suggested} }} }} }} }}"
            }
            res2 = requests.post(url, headers=headers, json=p_payload)
            data2 = res2.json()
            
            if "errors" not in data2 and data2.get("data"):
                print(f"\n🎉🎉🎉 أخيرررراً تم السحب بنجاح باستخدام: {suggested}")
                with open("final_products.json", "w", encoding="utf-8") as f:
                    json.dump(data2, f, ensure_ascii=False, indent=2)
                print("✅ تم حفظ الملف final_products.json بنجاح!")
                success = True
                break
    except Exception:
        continue

if not success:
    print("⚠️ لم نصل للكلمة، أظهر استجابة السيرفر لمعاينتها:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

