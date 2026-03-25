# Content Monitoring and Flagging System

## 📌 Overview

This project is a backend system that monitors content based on predefined keywords. It scans content items, matches them with keywords, generates flags, and allows reviewers to mark them as relevant or irrelevant.

The system also includes a suppression mechanism to prevent repeatedly showing irrelevant content unless the content is updated.

---

## ⚙️ Tech Stack

* Python
* Django
* Django REST Framework
* SQLite

---

## 🚀 Features

* Add keywords dynamically
* Import and scan content from a mock JSON dataset
* Match keywords with content (title/body)
* Assign relevance scores (100 / 70 / 40)
* Generate flags for matched content
* Review flags (pending / relevant / irrelevant)
* Suppress irrelevant flags until content changes
* Re-surface flags when content is updated

---

## 📡 API Endpoints

### 1. Create Keyword

POST `/keywords/`

Example:

```json
{
  "name": "python"
}
```

---

### 2. Trigger Scan

POST `/scan/`

* Loads content from mock JSON
* Matches keywords
* Creates/updates flags

---

### 3. Get All Flags

GET `/flags/`

---

### 4. Update Flag Status

PATCH `/flags/<id>/`

Example:

```json
{
  "status": "irrelevant"
}
```

---

## 🛠️ Setup Instructions

```bash
git clone https://github.com/Rahman-s/content-monitoring-system

cd content_monitoring

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

Server will run at:
http://127.0.0.1:8000/

---

## 🧪 Testing Steps

1. Create keywords using `/keywords/`
2. Run scan using `/scan/`
3. Check flags using `/flags/`
4. Mark a flag as `irrelevant`
5. Run scan again → flag should be suppressed
6. Update `last_updated` in mock_data.json
7. Run scan again → flag should reappear

---

## 🧠 Assumptions

* Mock JSON dataset is used instead of external API
* Content uniqueness is based on `title + source`
* Suppression is handled using `suppressed_at_content_update` field

---

## ⚖️ Trade-offs

* No authentication implemented
* No pagination/filtering added
* No external API integration (to keep solution simple and focused)

---

## 📂 Project Structure

```
content_monitoring/
│
├── manage.py
├── requirements.txt
├── README.md
│
├── content_monitoring/
│
└── monitor/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── services.py
    ├── urls.py
    └── mock_data.json
```

---

## ✅ Conclusion

This system demonstrates a clean and scalable approach to content monitoring, keyword matching, and intelligent suppression logic for real-world use cases like moderation, analytics, and data filtering.
