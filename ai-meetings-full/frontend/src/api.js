import axios from "axios";
const api = axios.create({ baseURL: "http://localhost:8000" });
export const getMeetings = () => api.get("/meetings");
export const uploadMeeting = (data) =>
  api.post("/meetings", data, { headers: { "Content-Type": "multipart/form-data" } });
export default api;
