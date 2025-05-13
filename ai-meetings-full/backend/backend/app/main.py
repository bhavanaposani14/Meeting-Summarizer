import shutil, uuid, asyncio, aiofiles
from pathlib import Path
from typing import Optional, Set, List
from fastapi import FastAPI, UploadFile, File, Depends, WebSocket, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .db import SessionLocal, engine, Base
from .models import Meeting, ActionItem, Decision
from .transcription import transcribe
from .summarizer import summarize
from .calendar import attach_summary
from .schemas import MeetingOut


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients: Set[WebSocket] = set()

@app.on_event("startup")
async def start():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.post("/meetings", response_model=MeetingOut)
async def upload_meeting(
    title: str = Form(...),
    file: Optional[UploadFile] = File(None),
    transcript: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
):
    if not (file or transcript):
        return {"error": "Provide audio file OR transcript"}

    # If a file is uploaded
    if file:
        # Save the file to a temporary path
        tmp_path = Path(f"temp_{uuid.uuid4()}_{file.filename}")
        async with aiofiles.open(tmp_path, "wb") as out_:
            content = await file.read()
            await out_.write(content)

        # If it's a .txt file, treat it as a transcript
        if file.filename.lower().endswith(".txt"):
            async with aiofiles.open(tmp_path, "r", encoding="utf-8") as f:
                transcript = await f.read()

        else:
            # Assume it's an audio file
            transcript = await transcribe(tmp_path)

        tmp_path.unlink()  # Delete the temp file

    summary, items, decisions = await summarize(transcript)

    meet = Meeting(title=title, transcript=transcript, summary=summary)
    db.add(meet)
    await db.flush()

    db.add_all([ActionItem(meeting_id=meet.id, **it) for it in items])
    db.add_all([Decision(meeting_id=meet.id, text=d) for d in decisions])
    await db.commit()
    await db.refresh(meet)

    # Notify WebSocket clients
    data = MeetingOut.from_orm(meet).dict()
    await asyncio.gather(*(c.send_json(data) for c in clients))

    return data

@app.get("/meetings", response_model=List[MeetingOut])
async def list_meetings(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Meeting).order_by(Meeting.created_at.desc()))
    meetings = res.scalars().unique().all()
    return [MeetingOut.from_orm(m) for m in meetings]

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            await ws.receive_text()  # keep alive
    except:
        clients.remove(ws)
