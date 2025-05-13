"""
Either run Whisper locally (small model = fastest) *or*
call AssemblyAI.  The choice is controlled by settings.USE_LOCAL_WHISPER.
"""
import tempfile, asyncio, aiofiles
from pathlib import Path
from .settings import get_settings

settings = get_settings()

async def transcribe(file_path: Path) -> str:
    if settings.USE_LOCAL_WHISPER:
        import whisper
        model = whisper.load_model("small")
        result = await asyncio.to_thread(model.transcribe, str(file_path))
        return result["text"]
    else:
        import aiohttp
        url = "https://api.assemblyai.com/v2/upload"
        headers = {"authorization": settings.ASSEMBLYAI_KEY}
        async with aiohttp.ClientSession() as sess:
            async with aiofiles.open(file_path, "rb") as f:
                data = await f.read()
            async with sess.post(url, data=data, headers=headers) as r:
                upload_url = (await r.json())["upload_url"]

            endpoint = "https://api.assemblyai.com/v2/transcript"
            payload  = {"audio_url": upload_url}
            async with sess.post(endpoint, json=payload, headers=headers) as r2:
                tid = (await r2.json())["id"]

            status = "queued"
            while status not in {"completed", "error"}:
                await asyncio.sleep(2)
                async with sess.get(f"{endpoint}/{tid}", headers=headers) as r3:
                    resp = await r3.json()
                    status = resp["status"]
            if status == "completed":
                return resp["text"]
            raise RuntimeError(resp.get("error", "AssemblyAI error"))
