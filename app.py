from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date
import requests

app = Flask(__name__)
app.secret_key = "secret123"

# 🔹 Telegram config
TELEGRAM_TOKEN = "8286847352:AAFcoQWxJ1JBM-dOv_SBQOPxtMBLggpwDW8"
CHAT_ID = "-4835473371"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=data)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        form_data = {
            "التاريخ": request.form.get("date"),
            "الفرقة": request.form.get("group"),
            "نوع النشاط": request.form.get("activity_type"),
            "المكان": request.form.get("place"),
            "وقت التنفيذ": request.form.get("time"),
            "عدد القادة": request.form.get("leaders"),
            "عدد الكشفيين": request.form.get("scouts"),
            "عدد غير الكشفيين": request.form.get("non_scouts"),
            "مناسبة النشاط": request.form.get("occasion") or "لا يوجد",
            "الفقرات المنفذة": request.form.getlist("paragraphs[]")
        }

        # Validation
        if not form_data["الفقرات المنفذة"] or all(not p.strip() for p in form_data["الفقرات المنفذة"]):
            flash("يجب إضافة فقرة واحدة على الأقل.", "error")
            return redirect(url_for("index"))

        # 🔹 Create Telegram message
        msg = f"📌 <b>نموذج النشاط تم الإرسال</b>\n"
        for k, v in form_data.items():
            if k == "الفقرات المنفذة":
                paragraphs = "\n".join([f"- {p}" for p in v if p.strip()])
                msg += f"{k}:\n{paragraphs}\n"
            else:
                msg += f"{k}: {v}\n"

        send_telegram(msg)
        flash("تم إرسال النموذج إلى تيليجرام بنجاح!", "success")
        return redirect(url_for("index"))

    return render_template("index.html", today=date.today().isoformat())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

