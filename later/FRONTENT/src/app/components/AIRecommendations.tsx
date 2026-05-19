import { Sparkles, ChevronLeft, ChevronRight } from 'lucide-react';
import { useState } from 'react';

interface Recommendation {
  venue: string;
  reason: string;
  image: string;
  deal: string;
}

export function AIRecommendations() {
  const [currentIndex, setCurrentIndex] = useState(0);

  const recommendations: Recommendation[] = [
    {
      venue: 'The Craft House',
      reason: 'Based on your love for craft beers',
      image: 'https://images.unsplash.com/photo-1436076863939-06870fe779c2?w=400',
      deal: '50% off all craft beers 5-7 PM'
    },
    {
      venue: 'Sunset Lounge',
      reason: 'Perfect weather for rooftop dining today',
      image: 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=400',
      deal: 'Buy 1 Get 1 on cocktails'
    },
    {
      venue: 'Vino Italiano',
      reason: 'Trending wine bar near you',
      image: 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=400',
      deal: '$5 house wines all evening'
    },
    {
      venue: 'Urban Taproom',
      reason: 'Popular during tonight\'s game',
      image: 'https://images.unsplash.com/photo-1572116469696-31de0f17cc34?w=400',
      deal: '$3 beers during the match'
    }
  ];

  const next = () => {
    setCurrentIndex((prev) => (prev + 1) % recommendations.length);
  };

  const prev = () => {
    setCurrentIndex((prev) => (prev - 1 + recommendations.length) % recommendations.length);
  };

  return (
    <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl p-6 text-white shadow-xl">
      <div className="flex items-center gap-2 mb-4">
        <Sparkles className="w-6 h-6" />
        <h3 className="text-2xl">AI Picks For You</h3>
      </div>

      <div className="relative">
        <div className="overflow-hidden rounded-xl">
          <div className="flex transition-transform duration-500" style={{ transform: `translateX(-${currentIndex * 100}%)` }}>
            {recommendations.map((rec, idx) => (
              <div key={idx} className="min-w-full">
                <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4">
                  <img src={rec.image} alt={rec.venue} className="w-full h-40 object-cover rounded-lg mb-3" />
                  <h4 className="text-xl mb-1">{rec.venue}</h4>
                  <p className="text-sm text-purple-200 mb-2">✨ {rec.reason}</p>
                  <div className="bg-white/20 p-2 rounded-lg">
                    <p className="text-sm">{rec.deal}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <button
          onClick={prev}
          className="absolute left-2 top-1/2 -translate-y-1/2 bg-white/30 hover:bg-white/50 p-2 rounded-full transition-colors"
        >
          <ChevronLeft className="w-5 h-5" />
        </button>
        <button
          onClick={next}
          className="absolute right-2 top-1/2 -translate-y-1/2 bg-white/30 hover:bg-white/50 p-2 rounded-full transition-colors"
        >
          <ChevronRight className="w-5 h-5" />
        </button>

        <div className="flex justify-center gap-2 mt-4">
          {recommendations.map((_, idx) => (
            <button
              key={idx}
              onClick={() => setCurrentIndex(idx)}
              className={`w-2 h-2 rounded-full transition-all ${
                idx === currentIndex ? 'bg-white w-6' : 'bg-white/50'
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
