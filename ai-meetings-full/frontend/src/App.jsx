import React, { useEffect, useState } from "react";
import { getMeetings, uploadMeeting } from "./api";
import MeetingList from "./components/MeetingList";
import MeetingDetail from "./components/MeetingDetail";

export default function App() {
  const [meetings, setMeetings] = useState([]);
  const [current, setCurrent] = useState(null);

  useEffect(() => { refresh(); }, []);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws");
    ws.onmessage = (e) => {
      const data = JSON.parse(e.data);
      setMeetings((m) => [data, ...m]);
    };
    return () => ws.close();
  }, []);

  const refresh = () => getMeetings().then((r) => setMeetings(r.data));
  const handleSelect = (m) => setCurrent(m);

  const handleUpload = async (e) => {
    e.preventDefault();
    const form = new FormData(e.target);
    await uploadMeeting(form);
    e.target.reset();
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6 grid grid-cols-3 gap-6">
      <section className="col-span-1 space-y-4">
        <form onSubmit={handleUpload} className="space-y-2">
          <input name="title" required placeholder="Meeting title" className="w-full p-2 border rounded" />
          <input name="file" type="file" accept="audio/*" className="w-full" />
          <textarea name="transcript" placeholder="Or paste transcript…" className="w-full p-2 border rounded" />
          <button className="bg-blue-600 text-white px-4 py-2 rounded w-full">Upload</button>
        </form>
        <MeetingList meetings={meetings} onSelect={handleSelect} />
      </section>
      <section className="col-span-2">
        {current ? <MeetingDetail meeting={current} /> : <p className="text-gray-500">Select a meeting…</p>}
      </section>
    </div>
  );
}
