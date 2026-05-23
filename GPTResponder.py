import time
import os
from openai import OpenAI
from prompts import system_instruction

class GPTResponder:
    def __init__(self):
        self.response = ""
        self.last_transcript = ""
        # بررسی وجود کلید در سیستم (جهت جلوگیری از کرش در حالت تست آفلاین)
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            self.client = None
            print("[INFO] OFFLINE MODE: No API Key detected. Credits are safe.")
        else:
            try:
                self.client = OpenAI(api_key=self.api_key)
                print("[INFO] ONLINE MODE: Connected to OpenAI server successfully.")
            except Exception:
                self.client = None

    def generate_response_from_transcript(self, transcript):
        # اگر کلید ست نشده باشد، درخواستی ارسال نمی‌شود
        if self.client is None:
            return "--- [OFFLINE TEST MODE: NO CREDITS USED] ---"

        try:
            api_response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # مدل سریع، فوق‌العاده ارزان و بهینه برای مصاحبه
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": f"Interview transcript so far:\n{transcript}\n\nProvide the answer based on my prepared texts."}
                ],
                temperature=0.4,       # خلاقیت پایین‌تر برای تمرکز دقیق روی متن‌های آماده شما
                max_tokens=700         # فضای کافی برای نمایش کامل پاسخ‌های شما
            )
            return api_response.choices[0].message.content
        except Exception as e:
            return f"Error connecting to server: {str(e)}"

    def respond_to_transcriber(self, transcriber):
        while True:
            transcript_string = transcriber.get_transcript()
            
            # فیلتر ۱: متن تغییر کرده باشد و طول آن بیش از ۶۰ کاراکتر (حدود ۱۰ کلمه معنادار) باشد
            # این کار مانع از تحریک کادر پایین با جملات نصفه و نویزهای صوتی می‌شود
            if transcript_string != self.last_transcript and len(transcript_string.strip()) > 60:
                
                # فیلتر ۲: تبدیل متن به حروف کوچک برای مقایسه هوشمند
                current_res = self.response.lower()
                new_trans = transcript_string.lower()
                
                # استخراج ۵ کلمه آخر شنیده شده
                words_to_check = new_trans.split()[-5:]
                
                # ترفند کاهش مصرف: اگر ۵ کلمه آخر شنیده شده در باکس پاسخ فعلی شما وجود داشته باشد،
                # یعنی شما دارید از روی متن می‌خوانید؛ پس نیازی به درخواست جدید نیست.
                is_reading = all(word in current_res for word in words_to_check) if words_to_check else False

                if is_reading:
                    # فقط آخرین وضعیت را ذخیره کن و به سرور درخواست نفرست
                    self.last_transcript = transcript_string
                    time.sleep(2)
                    continue

                # اگر یک سوال واقعی یا فیدبک جدید از مصاحبه‌کننده بود، پردازش شروع می‌شود
                self.response = "... Analyzing the question ..."
                self.response = self.generate_response_from_transcript(transcript_string)
                self.last_transcript = transcript_string
            
            # مکث ۴ ثانیه‌ای حلقه برای آزاد کردن منابع CPU و جلوگیری از اورلپ شدن تردها
            time.sleep(4)