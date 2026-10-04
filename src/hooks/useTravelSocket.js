import { useEffect, useRef, useState } from "react";

export default function useTravelSocket(sessionId) {
  const socket = useRef(null);

  const [connected, setConnected] = useState(false);
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    if (!sessionId) return;

    socket.current = new WebSocket("ws://localhost:8000/ws/travel");

    socket.current.onopen = () => {
      setConnected(true);
    };

    socket.current.onclose = () => {
      setConnected(false);
    };

    socket.current.onerror = () => {
      setConnected(false);
    };

    socket.current.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === "node_update") {
        setMessages((prev) => [
          ...prev,
          {
            sender: "assistant",
            node: data.node,
            output: data.output,
          },
        ]);
      }

      if (data.type === "done") {
        // Optional: add a completion indicator later
      }
    };

    return () => {
      socket.current?.close();
    };
  }, [sessionId]);

  const sendQuery = (query) => {
    if (!socket.current || socket.current.readyState !== WebSocket.OPEN) {
      return;
    }

    // User bubble
    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: query,
      },
    ]);

    // Send to backend
    socket.current.send(
      JSON.stringify({
        query,
        session_id: sessionId,
      })
    );
  };

  return {
    connected,
    messages,
    sendQuery,
  };
}