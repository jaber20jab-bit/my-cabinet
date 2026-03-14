# 🗄️ خزانتي الرقمية / My Digital Cabinet

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

منصة رقمية شخصية لتنظيم المقالات والمذكرات والوصول إليها من أي مكان.

A personal digital platform to organize articles and notes, accessible from anywhere.

---

## ✨ المميزات / Features

- 📚 **مقالات** — إضافة وتعديل وحذف المقالات مع تصنيفات ووسوم
- 📝 **مذكرات** — ملاحظات سريعة مع تثبيت في الأعلى
- 🔍 **بحث شامل** — ابحث في المقالات والمذكرات (Ctrl+K)
- 🌐 **ثنائي اللغة** — عربي وإنجليزي
- 🌙 **وضع OLED داكن** — واجهة سوداء أنيقة للشاشات OLED
- 📱 **تصميم متجاوب** — يعمل على الموبايل والتابلت والديسكتوب
- 🏷️ **تصنيفات ووسوم** — تنظيم مرن للمحتوى

## 🚀 التشغيل / Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python run.py

# Open in browser
http://localhost:8000
```

## 🏗️ التقنيات / Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | FastAPI |
| Database | SQLite |
| Frontend | HTML + CSS + JS |
| Styling | Custom (Astro Paper inspired) |

## 📁 الهيكل / Project Structure

```
my-cabinet/
├── app/
│   ├── main.py          # FastAPI app & routes
│   └── database.py      # SQLite database
├── templates/            # Jinja2 HTML templates
├── static/
│   ├── css/style.css     # OLED dark theme
│   └── js/main.js        # Interactions
├── requirements.txt
├── run.py                # Entry point
└── README.md
```

## 📸 Screenshots

> Coming soon...

## 📄 License

MIT

---

**صُنع بـ 🤖 بواسطة تومي**
