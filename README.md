# 🧠 AI Meetings Assistant

An AI-powered web application that automatically summarizes meeting transcripts, extracts action items, logs decisions, and provides a live dashboard for real-time collaboration.

---

## 🚀 Features

- 🎙️ Upload Audio or Text – Upload `.wav` files or paste transcripts
- 🧠 AI-Powered Summarization – Uses OpenAI GPT to generate summaries, action items & decision logs
- 🔄 Real-Time Dashboard – WebSocket-based updates on meeting records
- 🎯 Action & Decision Tracking – Automatically structured insights
- 🌐 Modern Stack – Built with FastAPI, React, Vite, and TailwindCSS

---

## 🧱 Tech Stack

- **Frontend:** React, Tailwind CSS, Vite
- **Backend:** FastAPI, SQLAlchemy (async), WebSockets
- **Database:** PostgreSQL
- **AI:** OpenAI GPT (via API)

---

## 📁 Project Structure

```
ai-meetings-full/
├── backend/        # FastAPI app
│   ├── app/
│   ├── .env
│   └── requirements.txt
└── frontend/       # React + Tailwind UI
    ├── src/
    ├── tailwind.config.js
    └── package.json
```

---

## 🔧 Getting Started

### 1. Backend Setup

```bash
cd backend
python -m venv .venv
. .venv/Scripts/activate       # On Windows
# or
source .venv/bin/activate      # On macOS/Linux

pip install -r requirements.txt
```

Create a `.env` file in `backend/`:

```
OPENAI_API_KEY=your-openai-api-key
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost/meetings
```

Ensure PostgreSQL is running and the `meetings` database exists.

Then run:

```bash
uvicorn app.main:app --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) to test the API.

---

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🧪 How to Use

1. Enter a meeting **title**
2. Upload a `.wav` file OR paste a transcript
3. Click **Upload**
4. View:
   - ✨ Summary
   - ✅ Action Items
   - 📌 Decision Log

---

## ⚙️ Environment Variables

| Variable         | Description                          |
|------------------|--------------------------------------|
| OPENAI_API_KEY   | Your OpenAI API key for GPT access   |
| DATABASE_URL     | PostgreSQL connection URL            |

---

## 📦 Deployment Notes

- Use Docker or cloud platforms for deployment
- Keep API keys secret using environment variables
- Extend audio capabilities with Whisper or AssemblyAI if needed

---

## 📄 License

MIT License © 2025 [Your Name]

---

## 🙋 Contact

For help or contributions, reach out:

📧 your.email@example.com  
🐙 GitHub: https://github.com/your-username/ai-meetings  
🔗 LinkedIn: https://linkedin.com/in/your-profile

---

> Built to save teams from hours of notetaking – powered by AI.
