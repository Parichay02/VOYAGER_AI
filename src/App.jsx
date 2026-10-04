import { useEffect, useState } from "react";
import ChatBox from "./components/ChatBox";
import InputBox from "./components/InputBox";
import useTravelSocket from "./hooks/useTravelSocket";
import { createSession } from "./services/api";

export default function App() {
  const [sessionId, setSessionId] = useState(null);

  useEffect(() => {
    createSession().then((data) => {
      setSessionId(data.session_id);
    });
  }, []);

  const { connected, messages, sendQuery } = useTravelSocket(sessionId);

  if (!sessionId) {
    return (
      <div className="h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-slate-300 text-xl">
          Starting VoyagerAI...
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen bg-slate-950 flex flex-col">
      <header className="border-b border-slate-800 px-6 py-4">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <h1 className="text-2xl font-bold text-white">
            VoyagerAI
          </h1>
          <div
            className={`w-3 h-3 rounded-full ${
              connected ? "bg-green-500" : "bg-red-500"
            }`}
          />
        </div>
      </header>

      <ChatBox messages={messages} />

      <div className="border-t border-slate-800 p-4">
        <div className="max-w-4xl mx-auto">
          <InputBox sendQuery={sendQuery} />
        </div>
      </div>
    </div>
  );
}