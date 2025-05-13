export default function MeetingList({ meetings, onSelect }) {
  return (
    <ul className="space-y-2 overflow-y-auto h-[70vh] pr-2">
      {meetings.map((m) => (
        <li
          key={m.id}
          onClick={() => onSelect(m)}
          className="cursor-pointer bg-white rounded-xl shadow p-3 hover:bg-gray-100"
        >
          <h3 className="font-semibold">{m.title}</h3>
          <p className="text-sm text-gray-500">{new Date(m.created_at).toLocaleString()}</p>
        </li>
      ))}
    </ul>
  );
}
