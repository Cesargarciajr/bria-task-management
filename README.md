# 🛠️ Site Support Request App

A simple, web-based request submission system for managing website-related support tickets. Built with Flask, SQLAlchemy, and deployed on Heroku. Ideal for teams that need to track page issues, enhancements, or urgent updates.

---

## 🚀 Features

- 📝 Submit requests with file attachments
- 📬 Email, page name, and urgency tracking
- 📂 Upload files securely
- 📊 Admin panel to view, filter, and toggle completion status
- 🕵️ View request details with timestamps
- 🗃️ Powered by SQLite (local) or PostgreSQL (e.g., Neon on Heroku)

---

## 📦 Tech Stack

- Python 3.13
- Flask 3.1.1
- SQLAlchemy + Flask-SQLAlchemy
- Gunicorn (for production)
- PostgreSQL or SQLite
- Heroku (Deployment)

---

## 🧱 Folder Structure

```
.
├── app.py                # Main Flask app
├── requirements.txt      # Python dependencies
├── Procfile              # Heroku process file
├── templates/            # HTML templates
│   ├── form.html
│   ├── requests.html
│   ├── admin.html
│   └── details.html
├── uploads/              # Uploaded files
│   └── .keep             # (Ensure folder exists in Git)
└── .python-version       # Python version (e.g. 3.13)
```

---

## ⚙️ Environment Variables

Set these in Heroku (⚙️ → Settings → Reveal Config Vars):

| Variable       | Description                        |
|----------------|------------------------------------|
| `SECRET_KEY`   | Flask secret key (any random str)  |
| `DATABASE_URL` | PostgreSQL database URI            |

---

## 💻 Local Development

1. **Clone the repo**:
   ```bash
   git clone https://github.com/your-username/site-support-app.git
   cd site-support-app
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the App**
   ```bash
   python app.py
   ```

4. **Access in your browser:**
   Visit [http://localhost:5000](http://localhost:5000)

---

## 🚢 Deploy to Heroku

1. **Create Heroku app:**
   ```bash
   heroku create
   ```

2. **Set environment variables:**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DATABASE_URL=your-neon-db-url
   ```

3. **Deploy the app:**
   ```bash
   git push heroku main
   ```

4. **Open in browser:**
   ```bash
   heroku open
   ```

---

## 🔧 Admin Panel

Visit `/admin` to view all requests.

You can filter by:
- ✅ Completion status (pending or done)
- 🚨 Urgency level (low, medium, high, etc.)
- 📅 Submission date (query param: `?date=YYYY-MM-DD`)

Click any request to view full details and toggle completion status.

---

## 📌 Notes

- Ensure the `uploads/` folder exists in production. You can include a `.keep` file to track it in Git.
- Use the following command to view Heroku logs for debugging:
  ```bash
  heroku logs --tail
  ```

---

## 🧡 License

MIT License — free to use, modify, and deploy!

---

## 🙌 Acknowledgments

Built with love using Flask 💖 and deployed via Heroku ☁️

---
