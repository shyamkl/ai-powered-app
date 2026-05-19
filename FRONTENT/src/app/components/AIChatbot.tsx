import { MessageCircle, X, Send } from 'lucide-react';
import { useState } from 'react';

export function AIChatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { text: 'Hi! I\'m your AI assistant. I can help you find the perfect venue, suggest deals, or handle any complaints. What can I do for you today?', isBot: true }
  ]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (!input.trim()) return;

    setMessages(prev => [...prev, { text: input, isBot: false }]);

    setTimeout(() => {
      const response = generateResponse(input);
      setMessages(prev => [...prev, { text: response, isBot: true }]);
    }, 1000);

    setInput('');
  };

  const generateResponse = (userInput: string): string => {
    const lower = userInput.toLowerCase();

    if (lower.includes('recommend') || lower.includes('suggest')) {
      return 'Based on your location and preferences, I recommend checking out "The Craft House" - they have 50% off craft beers from 5-7 PM today! Would you like to see more options?';
    } else if (lower.includes('complaint') || lower.includes('issue') || lower.includes('problem')) {
      return 'I\'m sorry to hear you\'re having an issue. Could you please provide more details about the problem? I\'ll make sure to escalate this to our support team right away.';
    } else if (lower.includes('crowd') || lower.includes('busy')) {
      return 'Currently, "Sunset Lounge" has a LOW crowd level - perfect for a relaxed evening! "Urban Taproom" is moderately busy with the game tonight.';
    } else if (lower.includes('deal') || lower.includes('offer')) {
      return 'Great deals right now: 1) The Craft House - 50% off beers, 2) Vino Italiano - $5 house wines, 3) Urban Taproom - $3 beers during games. Which interests you?';
    } else {
      return 'I can help you find venues, check deals, see crowd levels, or address any concerns. What would you like to know?';
    }
  };

  return (
    <>
      {/* Chat Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 rounded-full shadow-2xl hover:shadow-3xl transition-all hover:scale-110 z-50"
        >
          <MessageCircle className="w-6 h-6" />
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 w-96 max-w-[calc(100vw-3rem)] bg-white rounded-2xl shadow-2xl z-50 flex flex-col h-[500px]">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 rounded-t-2xl flex items-center justify-between">
            <div className="flex items-center gap-2">
              <MessageCircle className="w-5 h-5" />
              <span>AI Assistant</span>
            </div>
            <button onClick={() => setIsOpen(false)} className="hover:bg-white/20 p-1 rounded">
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.isBot ? 'justify-start' : 'justify-end'}`}>
                <div className={`max-w-[80%] p-3 rounded-2xl ${
                  msg.isBot
                    ? 'bg-gray-100 text-gray-800'
                    : 'bg-gradient-to-r from-blue-600 to-purple-600 text-white'
                }`}>
                  {msg.text}
                </div>
              </div>
            ))}
          </div>

          {/* Input */}
          <div className="p-4 border-t border-gray-200">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Type your message..."
                className="flex-1 p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                onClick={handleSend}
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
