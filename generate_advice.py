import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def generate_advice(user_query, matched_products, max_retries=3):
    match = matched_products[0]
    p = match["product"]

    product_context = f"""
المنتج: {p['اسم_المنتج']}
- النوع: {p['النوع']}
- الموسم المناسب: {p['الموسم']}
- التصنيف العطري: {p['التصنيف العطري']}
- النوتات: {p['النوتات الرئيسية']}
- درجة الحلاوة: {p['درجة الحلاوة']}
"""

    prompt = f"""أنت مستشار عطور محترف. مهمتك تكتب نصيحة قصيرة وودودة بالعربي للعميل عن منتج واحد فقط.

سؤال العميل: "{user_query}"

هذا هو المنتج المقترح (اعتمد فقط على هذه المعلومات، ولا تخترع أي معلومة غير موجودة هنا):
{product_context}

اكتب نصيحة تشرح لماذا هذا العطر مناسب لسؤال العميل، ومتى الأفضل استخدامه (صباحاً أم مساءً بناءً على بيانات الموسم/النوع)، بأسلوب ودود ومختصر (4-5 جمل كحد أقصى). لا تذكر أي معلومة (مثل السعر أو مكونات إضافية) غير مذكورة في البيانات أعلاه. اختم كلامك بجملة ودودة تسأل العميل هل يعجبه هذا الاقتراح أم يفضل رؤية خيار آخر."""

    last_error = None
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )
            return response.text
        except Exception as e:
            last_error = e
            print(f"محاولة {attempt + 1} فشلت، جاري إعادة المحاولة...")
            time.sleep(2)

    return "عذراً، حدث خطأ مؤقت في توليد النصيحة. برجاء المحاولة مرة أخرى."