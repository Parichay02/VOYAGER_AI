import Message from "./Message";

export default function ChatBox({ messages }) {
  return (
    <div className="flex-1 overflow-y-auto p-6">
      <div className="max-w-4xl mx-auto">
        {messages.map((message, index) => (
          <Message key={index} message={message} />
        ))}
      </div>
    </div>
  );
}