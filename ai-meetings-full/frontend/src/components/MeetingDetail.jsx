export default function MeetingDetail({ meeting }) {
  return (
    <div className="bg-white rounded-xl shadow p-6 space-y-4 overflow-y-auto h-[80vh]">
      <h2 className="text-2xl font-bold">{meeting.title}</h2>
      <h3 className="font-semibold">Summary</h3>
      <p>{meeting.summary}</p>

      <h3 className="font-semibold">Action Items</h3>
      <ul className="list-disc ml-6">
        {meeting.action_items.map((a) => (
          <li key={a.description}>
            <strong>{a.owner}</strong> — {a.description} {a.due_date && <em>({a.due_date})</em>}
          </li>
        ))}
      </ul>

      <h3 className="font-semibold">Decisions</h3>
      <ol className="list-decimal ml-6">
        {meeting.decisions.map((d) => (
          <li key={d.text}>{d.text}</li>
        ))}
      </ol>

      <details>
        <summary className="cursor-pointer mt-4 text-blue-600">Raw transcript</summary>
        <pre className="whitespace-pre-wrap mt-2">{meeting.transcript}</pre>
      </details>
    </div>
  );
}
