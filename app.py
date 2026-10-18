"""
منصة تسجيل الاهتمام بالسيارات المستوردة (أقل من 3 سنوات) - GLOBAL CAR

التشغيل:
    pip install flask gunicorn
    python app.py

في الإنتاج: استعمل gunicorn عبر خوادم مثل Render أو PythonAnywhere.
"""
import os
from flask import Flask, redirect, render_template, request
from jinja2 import DictLoader

# ───────────────────────── الإعدادات ─────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BRAND = os.environ.get("BRAND_NAME", "GLOBAL CAR")
CONTACT_PHONE = os.environ.get("CONTACT_PHONE", "")
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "")
CONTACT_ADDRESS = os.environ.get("CONTACT_ADDRESS", "")

# رابط الـ SmartLink الخاص بعروض الجزائر لجميع المشغلين
PROMOTION_URL = os.environ.get(
    "PROMOTION_URL",
    "https://126d62c9b5d0.sunrise-brook.com/?wid=152076&wid_hmac=b1c2c12d5102bb869f9b49099a0bb922&p=30075"
)

app = Flask(__name__, static_folder=os.path.join(BASE_DIR, "static"))
app.secret_key = os.environ.get("SECRET_KEY", "global_car_direct_flow_secret")

# السيارات: (المفتاح، الاسم اللاتيني، الاسم العربي، السعر التقديري بمليون سنتيم)
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

def static_exists(name):
    return os.path.isfile(os.path.join(BASE_DIR, "static", name))

@app.context_processor
def inject_globals():
    return dict(
        brand=BRAND,
        contact_phone=CONTACT_PHONE,
        contact_email=CONTACT_EMAIL,
        contact_address=CONTACT_ADDRESS,
        has_logo=static_exists("logo.png"),
        has_hero=static_exists("hero.jpg"),
        promo_url=PROMOTION_URL,
    )

# ───────────────────────── المسارات ─────────────────────────
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # بمجرد اختيار السيارة والنقر على الزر، يتم تحويل الزائر مباشرة للرابط الترويجي
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
:root{--navy:#0E2230;--navy2:#16384D;--ink:#14232E;--paper:#F4F6F5;--card:#fff;--steel:#5B6B76;--line:#D9DEDB;
--accent:#0F6B63;--accent-d:#0A524C;--accent-bg:#E6F4F1;--gold:#C9A24B;--err:#9A2A12;--err-bg:#FDEEE9}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:"IBM Plex Sans Arabic",system-ui,sans-serif;background:var(--paper);
color:var(--ink);line-height:1.75;min-height:100vh;display:flex;flex-direction:column}
a{color:var(--accent)}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}

/* الترويسة */
.top{background:var(--card);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:20}
.top .wrap{display:flex;justify-content:space-between;align-items:center;height:72px;gap:16px}
.brand{display:flex;align-items:center;gap:12px;text-decoration:none;color:var(--navy)}
.brand .mark{width:46px;height:46px;flex:none}
.brand img{height:46px;width:auto;display:block}
.brand .name{font-weight:700;font-size:1.15rem;letter-spacing:.04em;line-height:1.1}
.brand .name small{display:block;font-weight:500;font-size:.68rem;letter-spacing:0;color:var(--steel)}
.nav{display:flex;align-items:center;gap:22px;font-size:.93rem}
.nav a{color:var(--ink);text-decoration:none;font-weight:500}
.nav a:hover{color:var(--accent)}
.nav .tel{background:var(--accent-bg);color:var(--accent-d);padding:7px 14px;border-radius:99px;font-weight:600}
@media(max-width:760px){.nav a.l{display:none}}

main{flex:1}
.section{padding:56px 0}
.section.tight{padding:36px 0 56px}
.eyebrow{color:var(--accent);font-weight:600;font-size:.85rem;margin-bottom:6px}
h1{font-size:clamp(1.8rem,4vw,2.6rem);line-height:1.35;margin:0 0 14px;font-weight:700}
h2{font-size:1.25rem;margin:0 0 6px}
h2.s{font-size:1.6rem;margin:0 0 8px}
.lead{color:var(--steel);font-size:1.05rem;max-width:50ch;margin:0 0 24px}

/* الواجهة الرئيسية */
.hero{background:linear-gradient(135deg,var(--navy) 0%,var(--navy2) 100%);color:#fff;position:relative;overflow:hidden}
.hero.photo{background-size:cover;background-position:center}
.hero.photo::before{content:"";position:absolute;inset:0;background:linear-gradient(135deg,rgba(14,34,48,.92),rgba(22,56,77,.78))}
.hero .wrap{position:relative;display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center;padding-top:56px;padding-bottom:56px}
.hero h1{color:#fff}
.hero .lead{color:#C7D3DA}
.hero .eyebrow{color:var(--gold)}
.hero .art{width:100%;max-width:460px;justify-self:center}
.cta{display:inline-block;background:var(--gold);color:#1B1606;text-decoration:none;font-weight:700;
padding:13px 26px;border-radius:10px}
.cta:hover{filter:brightness(1.07)}
.cta.o{background:transparent;color:#fff;border:1px solid rgba(255,255,255,.4);margin-inline-start:10px}
@media(max-width:860px){.hero .wrap{grid-template-columns:1fr;padding-top:36px;padding-bottom:36px}.hero .art{max-width:320px}}

/* شريط الثقة */
.trust{background:var(--card);border-bottom:1px solid var(--line)}
.trust .wrap{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;padding-top:22px;padding-bottom:22px}
.tr{display:flex;gap:12px;align-items:flex-start}
.tr svg{width:34px;height:34px;flex:none;color:var(--accent)}
.tr b{display:block;font-size:.95rem}.tr span{color:var(--steel);font-size:.84rem;line-height:1.5;display:block}
@media(max-width:760px){.trust .wrap{grid-template-columns:1fr}}

/* الخطوات والنموذج */
.grid{display:grid;grid-template-columns:1fr 1.05fr;gap:48px;align-items:start}
.steps{list-style:none;margin:0 0 24px;padding:0;counter-reset:s}
.steps li{counter-increment:s;display:flex;gap:14px;margin-bottom:16px}
.steps li::before{content:counter(s);flex:none;width:32px;height:32px;border-radius:50%;
background:var(--navy);color:#fff;display:grid;place-items:center;font-weight:600;font-size:.9rem}
.steps b{display:block}.steps span{color:var(--steel);font-size:.92rem}
.note{border-right:3px solid var(--gold);padding:4px 14px;color:var(--steel);font-size:.88rem;max-width:52ch}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:28px;box-shadow:0 8px 28px rgba(14,34,48,.07)}
fieldset{border:0;margin:0 0 20px;padding:0}
.group{display:flex;align-items:center;gap:8px;font-size:.84rem;color:var(--steel);margin:16px 0 8px;font-weight:600}
.group svg{width:34px;height:20px;color:var(--accent)}
.opts{display:grid;gap:8px}
.opt{position:relative;display:flex;justify-content:space-between;align-items:center;gap:12px;
padding:11px 14px;border:1px solid var(--line);border-radius:10px;cursor:pointer;background:#fff}
.opt:hover{border-color:#9DB5B0}
.opt input{position:absolute;opacity:0;inset:0;cursor:pointer}
.opt:has(input:checked){border-color:var(--accent);background:var(--accent-bg)}
.opt .n{font-weight:600}.opt .n small{display:block;font-weight:400;color:var(--steel)}
.opt .p{font-size:.88rem;color:var(--steel);white-space:nowrap}
.btn{width:100%;padding:13px 18px;border:0;border-radius:10px;background:var(--accent);color:#fff;
font:inherit;font-weight:600;cursor:pointer;text-align:center;text-decoration:none;display:block}
.btn:hover{background:var(--accent-d)}

/* الأسئلة الشائعة */
.faq{background:var(--card);border-top:1px solid var(--line)}
.faq details{border:1px solid var(--line);border-radius:12px;padding:14px 18px;margin-bottom:10px;background:#fff;max-width:760px}
.faq summary{cursor:pointer;font-weight:600}
.faq p{margin:10px 0 0;color:var(--steel);font-size:.93rem}

/* التذييل */
footer{background:var(--navy);color:#B7C4CC;font-size:.88rem}
footer .wrap{display:grid;grid-template-columns:1.3fr 1fr 1fr;gap:32px;padding-top:40px;padding-bottom:28px}
footer h3{color:#fff;font-size:.95rem;margin:0 0 10px}
footer a{color:#B7C4CC}
footer .mark{width:40px;height:40px;color:#fff}
footer .fb{display:flex;align-items:center;gap:10px;color:#fff;font-weight:700;letter-spacing:.04em;margin-bottom:10px}
footer ul{list-style:none;margin:0;padding:0}footer li{margin-bottom:6px}
footer .legal{border-top:1px solid rgba(255,255,255,.12);padding:14px 0;font-size:.8rem;color:#8FA0AA}
@media(max-width:760px){footer .wrap{grid-template-columns:1fr}}
@media(max-width:860px){.grid{grid-template-columns:1fr;gap:28px}.card{padding:20px}.section{padding:40px 0}}
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <defs>
    <symbol id="logo-mark" viewBox="0 0 64 64">
      <rect x="1" y="1" width="62" height="62" rx="14" fill="#0E2230"/>
      <circle cx="32" cy="32" r="22" fill="none" stroke="#C9A24B" stroke-width="2.2" opacity=".9"/>
      <ellipse cx="32" cy="32" rx="9" ry="22" fill="none" stroke="#C9A24B" stroke-width="1.4" opacity=".55"/>
      <path d="M10 32h44" stroke="#C9A24B" stroke-width="1.4" opacity=".55"/>
      <path d="M15 38l3-7c1-2 3-3 6-3h14c3 0 5 1 7 4l3 3c2 .5 3 1.5 3 3.5V41H15z" fill="#fff"/>
      <circle cx="23" cy="42" r="3.6" fill="#0E2230" stroke="#fff" stroke-width="2"/>
      <circle cx="43" cy="42" r="3.6" fill="#0E2230" stroke="#fff" stroke-width="2"/>
    </symbol>
    <symbol id="car-sedan" viewBox="0 0 60 28">
      <path d="M3 20l3-6c1-2 3-3 6-3h6l6-6c1-1 3-2 5-2h8c3 0 5 1 7 4l4 5 5 1c2 .4 3 1.4 3 3.4V20c0 1-1 2-2 2H5c-1 0-2-1-2-2z" fill="currentColor"/>
      <circle cx="16" cy="22" r="4.2" fill="#fff" stroke="currentColor" stroke-width="2.4"/>
      <circle cx="46" cy="22" r="4.2" fill="#fff" stroke="currentColor" stroke-width="2.4"/>
    </symbol>
    <symbol id="car-hatch" viewBox="0 0 60 28">
      <path d="M3 20l2-6c1-2 3-4 6-4h6l7-6c1-1 3-2 5-2h10c3 0 5 2 6 4l3 5 6 2c1 .3 2 1.4 2 2.6V20c0 1-1 2-2 2H5c-1 0-2-1-2-2z" fill="currentColor"/>
      <circle cx="16" cy="22" r="4.2" fill="#fff" stroke="currentColor" stroke-width="2.4"/>
      <circle cx="46" cy="22" r="4.2" fill="#fff" stroke="currentColor" stroke-width="2.4"/>
    </symbol>
    <symbol id="i-check" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" d="M12 3l7 3v5c0 5-3 8-7 10-4-2-7-5-7-10V6l7-3zM9 12l2 2 4-4"/></symbol>
    <symbol id="i-phone" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" d="M7 3h10a1 1 0 011 1v16a1 1 0 01-1 1H7a1 1 0 01-1-1V4a1 1 0 011-1zM11 18h2"/></symbol>
    <symbol id="i-lock" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" d="M6 11h12v9H6zM8 11V8a4 4 0 018 0v3"/></symbol>
  </defs>
</svg>

<header class="top"><div class="wrap">
  <a class="brand" href="/" aria-label="{{ brand }}">
    {% if has_logo %}<img src="/static/logo.png" alt="{{ brand }}">
    {% else %}<svg class="mark" aria-hidden="true"><use href="#logo-mark"/></svg>
    <span class="name">{{ brand }}<small>استيراد السيارات الحديثة</small></span>{% endif %}
  </a>
  {% block nav %}
  <nav class="nav" aria-label="التنقل">
    <a class="l" href="/#how">كيف نعمل</a>
    <a class="l" href="/#register">التسجيل</a>
    <a class="l" href="/#faq">أسئلة شائعة</a>
    {% if contact_phone %}<a class="tel" dir="ltr" href="tel:{{ contact_phone|replace(' ','') }}">{{ contact_phone }}</a>{% endif %}
  </nav>
  {% endblock %}
</div></header>

<main>{% block main %}{% endblock %}</main>

<footer>
  <div class="wrap">
    <div>
      <div class="fb"><svg class="mark" aria-hidden="true"><use href="#logo-mark"/></svg>{{ brand }}</div>
      <p style="margin:0;max-width:34ch">نساعدك على التعرّف على السيارات المستوردة الحديثة (أقل من 3 سنوات) وتكلفتها بوضوح.</p>
    </div>
    <div>
      <h3>روابط</h3>
      <ul>
        <li><a href="/#how">كيف نعمل</a></li>
        <li><a href="/#register">سجّل اهتمامك</a></li>
        <li><a href="/#faq">أسئلة شائعة</a></li>
      </ul>
    </div>
    <div>
      <h3>تواصل معنا</h3>
      <ul>
        {% if contact_phone %}<li dir="ltr" style="text-align:right">{{ contact_phone }}</li>{% endif %}
        {% if contact_email %}<li dir="ltr" style="text-align:right"><a href="mailto:{{ contact_email }}">{{ contact_email }}</a></li>{% endif %}
        {% if contact_address %}<li>{{ contact_address }}</li>{% endif %}
        {% if not (contact_phone or contact_email or contact_address) %}<li>سيتم إضافة بيانات التواصل قريباً.</li>{% endif %}
      </ul>
    </div>
  </div>
  <div class="wrap legal">© {{ brand }}. جميع الحقوق محفوظة.</div>
</footer>
</body></html>"""

INDEX = """{% extends "base.html" %}
{% block title %}سجّل اهتمامك بسيارة مستوردة · {{ brand }}{% endblock %}
{% block main %}
<section class="hero{{ ' photo' if has_hero }}"{% if has_hero %} style="background-image:url('/static/hero.jpg')"{% endif %}>
  <div class="wrap">
    <div>
      <div class="eyebrow">سيارات مستوردة أقل من 3 سنوات</div>
      <h1>اعرف سيارتك وتكلفتها قبل أن تلتزم</h1>
      <p class="lead">اختر السيارة التي تهمّك وسجّل اهتمامك لمتابعة الطلب مباشرة عبر شبكة هاتفك.</p>
      <a class="cta" href="#register">سجّل اهتمامك الآن</a>
      <a class="cta o" href="#how">كيف نعمل؟</a>
    </div>
    <svg class="art" viewBox="0 0 460 250" role="img" aria-label="رسم توضيحي لسيارة">
      <ellipse cx="230" cy="214" rx="190" ry="10" fill="#000" opacity=".25"/>
      <g transform="translate(40 50) scale(6.1)" style="color:#fff"><use href="#car-sedan" width="60" height="28"/></g>
      <path d="M30 222h400" stroke="#C9A24B" stroke-width="2" stroke-dasharray="10 10" opacity=".6"/>
    </svg>
  </div>
</section>

<section class="trust">
  <div class="wrap">
    <div class="tr"><svg aria-hidden="true"><use href="#i-check"/></svg><div><b>خدمة أوتوماتيكية</b><span>مخصصة لجميع متعاملي الجزائر (جيزي، أوريدو، موبيليس).</span></div></div>
    <div class="tr"><svg aria-hidden="true"><use href="#i-phone"/></svg><div><b>تأكيد بضغطة زر</b><span>تأكيد سريع عبر شريحة الهاتف دون تعقيدات.</span></div></div>
    <div class="tr"><svg aria-hidden="true"><use href="#i-lock"/></svg><div><b>تصفح آمن</b><span>حماية كاملة لبياناتك وخصوصيتك.</span></div></div>
  </div>
</section>

<section class="section tight" id="how">
  <div class="wrap grid">
    <div>
      <div class="eyebrow">خطوات بسيطة</div>
      <h2 class="s">كيف نعمل</h2>
      <p class="lead">خطوات سريعة لاختيار وتأكيد طلبك.</p>
      <ol class="steps">
        <li><div><b>اختر السيارة</b><span>حدد السيارة المناسبة لك من القائمة مع السعر التقديري.</span></div></li>
        <li><div><b>متابعة الطلب</b><span>اضغط على زر التأكيد ليتم توجيهك إلى صفحة الخدمة الرسمية لشبكتك.</span></div></li>
      </ol>
      <p class="note">الأسعار تقديرية وتتغيّر حسب الطراز والسنة وسعر الصرف والرسوم.</p>
    </div>

    <section class="card" id="register" aria-labelledby="ft">
      <h2 id="ft">اختر السيارة ومتابعة الطلب</h2>
      <form method="post" style="margin-top:20px">
        <fieldset>
          <legend style="font-weight:600;margin-bottom:12px">السيارات المتاحة والسعر التقديري</legend>
          {% for title, items in groups %}
            <div class="group"><svg aria-hidden="true"><use href="#{{ 'car-hatch' if loop.first else 'car-sedan' }}"/></svg>{{ title }}</div>
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
</section>

<section class="section faq" id="faq">
  <div class="wrap">
    <div class="eyebrow">أسئلة شائعة</div>
    <h2 class="s" style="margin-bottom:18px">قبل أن تسجّل</h2>
    <details><summary>هل الخدمة تعمل مع كل المشغلين في الجزائر؟</summary><p>نعم، النظام يتعرف آلياً على نوع شريحتك (جيزي، أوريدو، موبيليس).</p></details>
    <details><summary>هل الأسعار المعروضة نهائية؟</summary><p>لا، هي أسعار تقديرية تتغيّر حسب الطراز والسنة وسعر الصرف والرسوم.</p></details>
  </div>
</section>
{% endblock %}"""

app.jinja_loader = DictLoader({
    "base.html": BASE, "index.html": INDEX
})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)