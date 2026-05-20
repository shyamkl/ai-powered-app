import { MessageCircle, X, Send } from 'lucide-react';
import { useState } from 'react';
import { sendChatMessage } from "../services/api";

export function AIChatbot() {

  const [isOpen, setIsOpen] = useState(false);

  const [messages, setMessages] = useState<any[]>([
    {
      sender: "bot",
      text: "Hi! I'm your AI assistant. I can help you find venues, suggest deals, and answer questions."
    }
  ]);

  const [inputMessage, setInputMessage] = useState("");

  const handleSendMessage = async () => {

    if (!inputMessage.trim()) return;

    const userMessage = {
      sender: "user",
      text: inputMessage,
    };

    setMessages(prev => [...prev, userMessage]);

    const currentMessage = inputMessage;

    setInputMessage("");

    try {

      const response = await sendChatMessage(currentMessage);

      const botMessage = {
        sender: "bot",
        text: response.reply,
      };

      setMessages(prev => [...prev, botMessage]);

    } catch (error) {

      console.error(error);

      setMessages(prev => [
        ...prev,
        {
          sender: "bot",
          text: "Sorry, something went wrong."
        }
      ]);
    }
  };

  return (
    <>
      {/* Floating Chat Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 rounded-full shadow-2xl hover:scale-110 transition-all z-50"
        >
          <MessageCircle className="w-6 h-6" />
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 w-96 max-w-[calc(100vw-2rem)] h-[500px] bg-white rounded-2xl shadow-2xl z-50 flex flex-col overflow-hidden">

          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <MessageCircle className="w-5 h-5" />
              <span className="font-semibold">AI Assistant</span>
            </div>

            <button
              onClick={() => setIsOpen(false)}
              className="hover:bg-white/20 p-1 rounded"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50">

            {messages.map((msg, idx) => (

              <div
                key={idx}
                className={`flex ${
                  msg.sender === "bot"
                    ? "justify-start"
                    : "justify-end"
                }`}
              >

                <div
                  className={`max-w-[80%] p-3 rounded-2xl ${
                    msg.sender === "bot"
                      ? "bg-white text-gray-800 shadow"
                      : "bg-gradient-to-r from-blue-600 to-purple-600 text-white"
                  }`}
                >
                  {msg.text}
                </div>

              </div>

            ))}

          </div>

          {/* Input */}
          <div className="p-4 border-t bg-white">
            <div className="flex gap-2">

              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    handleSendMessage();
                  }
                }}
                placeholder="Type your message..."
                className="flex-1 border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />

              <button
                onClick={handleSendMessage}
                className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-3 rounded-xl hover:shadow-lg transition-all"
              >
                <Send className="w-5 h-5" />
              </button>

            </div>
          </div>

        </div>
      )}
    </>
  );
}