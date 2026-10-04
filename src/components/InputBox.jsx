import { useState } from "react";

export default function InputBox({ sendQuery }) {
  const [query, setQuery] = useState("");

  const submit = () => {
    if (!query.trim()) return;

    sendQuery(query);
    setQuery("");
  };

  return (
    <div
      style={{
        display: "flex",
        marginTop: 20,
      }}
    >
      <input
        style={{
          flex: 1,
          padding: 12,
        }}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask VoyagerAI..."
        onKeyDown={(e) => e.key === "Enter" && submit()}
      />

      <button onClick={submit}>Send</button>
    </div>
  );
}