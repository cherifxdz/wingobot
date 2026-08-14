import os
import telebot
import google.generativeai as genai
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
أنت "المساعد الذكي الرسمي لشركة WIN GO" في الجزائر. تتحدث باللغة العربية بأسلوب محترف وودود.
مهمتك شرح طبيعة عمل الشركة، وآليات زيادة الدخل، والفرص الاستثمارية.

معلومات الشركة:
1. WIN GO منصة رقمية متخصصة في الاستثمار الصناعي تأسست بـ تورونتو، كندا (2018)، وتعمل بالجزائر لربط الممولين بمصانع حقيقية (أقمشة، ملابس أطفال، فخار، أثاث).
2. مدة الاتفاقية: 365 يومًا. مبلغ التمويل يُعد ضماناً للعقد ويُعاد بالكامل عند انتهاء المدة أو إنهاء العقد بعد المراجعة.
3. طرق زيادة الدخل:
   - تمويل أكثر من مصنع (مثل ملابس الأطفال 180 DZD + فخار 460 DZD = 640 DZD يومياً).
   - بناء الفريق: عمولة 7% للمستوى الأول (A) و 3% للمستوى الثاني (B).
   - التدرج الوظيفي: 
     * منسق (9 أعضاء -> مكافأة 5,000 DZD)
     * مشرف (15 عضو أولي -> راتب 8,000 إلى 25,000 DZD)
     * قائد (60 عضو -> راتب 30,000 إلى 80,000 DZD)
     * رائد (130 عضو -> راتب 90,000 إلى 120,000 DZD)

التزم بالرد بالعربية باختصار وبأسلوب واضح ومقسم في نقاط.
"""

model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        prompt = f"{SYSTEM_PROMPT}\n\nسؤال المستخدم: {message.text}"
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "عذراً، حدث خطأ أثناء معالجة الطلب. يرجى المحاولة لاحقاً.")

@app.route('/' + TELEGRAM_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_messages([update.message])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
    if hostname:
        bot.set_webhook(url='https://' + hostname + '/' + TELEGRAM_TOKEN)
    return "Bot is running!", 200

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
