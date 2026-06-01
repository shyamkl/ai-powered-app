import { MapPin, Clock, Star, Heart, TrendingUp } from 'lucide-react';
import { uploadVenueImage } from "../api";

interface VenueCardProps {
  venue: {
    id: number;
    name: string;
    type: string;
    area?: string;
    image: string;
    image_url?: string;
    local_image?: string;
    rating: number;
    reviews: number;
    distance: string;
    happyHour: string;
    deal: string;
    address: string;
    crowdLevel: string;
    foodType: string[];
    drinkTypes: string[];
    isPremium: boolean;
    menuType: string[];
  };

  isPremiumMember: boolean;

  onFavorite: (id: number) => void;

  isFavorited: boolean;

  onViewDetails: () => void;
}

export function VenueCard({
  venue,
  isPremiumMember,
  onFavorite,
  isFavorited,
  onViewDetails,
}: VenueCardProps) {

  return (
    <div className="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300 hover:-translate-y-1">

      {/* IMAGE */}
      <div className="relative h-48 overflow-hidden">

        {/* <img
          src={venue.image}
          alt={venue.name}
          className="w-full h-full object-cover"
        /> */}
       {/* <img
  src={
    // USER UPLOADED IMAGE
    venue.local_image
      ? `http://127.0.0.1:8000${venue.local_image}`

      // EXISTING DATABASE IMAGE
      : venue.image_url
      ? venue.image_url

      // FALLBACK IMAGE
      : "https://placehold.co/600x400?text=No+Image"
  }

  alt={venue.name}

  className="w-full h-48 object-cover rounded"

  onError={(e) => {

    // FALLBACK ONLY IF IMAGE FAILS
    (e.currentTarget as HTMLImageElement).src =
      "https://placehold.co/600x400?text=No+Image";
  }}
/> */}
<img
  src={venue.image}
  alt={venue.name}
  className="w-full h-48 object-cover rounded"
  onError={(e) => {

    const target = e.currentTarget;

    // prevent infinite loop
    target.onerror = null;

    target.src =
      "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800";
  }}
/>
        {/* TOP RIGHT BUTTONS */}
        <div className="absolute top-3 right-3 flex gap-2">

          <button
            onClick={() => onFavorite(venue.id)}
            className={`p-2 rounded-full backdrop-blur-sm transition-all duration-300 ${
              isFavorited
                ? 'bg-red-500 text-white'
                : 'bg-white/80 text-gray-700 hover:bg-red-500 hover:text-white'
            }`}
          >
            <Heart
              className={`w-5 h-5 transition-all ${
                isFavorited ? 'fill-current text-white' : ''
              }`}
            />
          </button>

        </div>

        {/* TOP LEFT BADGES */}
        <div className="absolute top-3 left-3 flex gap-2">

          {venue.isPremium && (
            <span className="px-3 py-1 bg-gradient-to-r from-amber-500 to-yellow-500 text-white text-xs rounded-full">
              PREMIUM
            </span>
          )}
            
          <span
            className={`px-3 py-1 text-white text-xs rounded-full ${
              venue.crowdLevel === 'Low'
                ? 'bg-green-500'
                : venue.crowdLevel === 'Medium'
                ? 'bg-orange-500'
                : 'bg-red-500'
            }`}
          >
            <TrendingUp className="w-3 h-3 inline mr-1" />
            {venue.crowdLevel} Crowd
          </span>
           
        </div>
            
        {/* PREMIUM MEMBER */}
        {isPremiumMember && (
          <div className="absolute bottom-3 left-3">
            <span className="px-3 py-1 bg-purple-600 text-white text-sm rounded-full">
              +20% OFF Member Deal
            </span>
          </div>
        )}
              
      </div>

      {/* CONTENT */}
      <div className="p-5">
        
        {/* TITLE */}
        <div className="flex items-start justify-between mb-2">

          <div className="flex-1">
            <h3 className="text-xl font-semibold mb-1">
              
              {venue.name}
            </h3>

            <span className="text-sm text-gray-500">
              {venue.type}
            </span>
          </div>

          {venue.rating !== null && venue.reviews > 0 && (
  <div className="flex items-center gap-1 bg-green-50 px-2 py-1 rounded-lg">

    <Star className="w-4 h-4 fill-green-600 text-green-600" />

    <span className="text-sm font-medium">
      {venue.rating}
    </span>

    <span className="text-xs text-gray-500">
      ({venue.reviews})
    </span>

  </div>
)}

        </div>

        {/* DETAILS */}
        <div className="space-y-2 mb-4">

          <div className="flex items-center gap-2 text-sm text-gray-600">

            <MapPin className="w-4 h-4 text-blue-500" />

            <span>
              {venue.distance} • {
                venue.address?.trim()
                  ? venue.address
                  : venue.area?.trim()
                  ? venue.area
                  : "Location unavailable"
              }
            </span>

          </div>

          <div className="flex items-center gap-2 text-sm text-gray-600">

            <Clock className="w-4 h-4 text-orange-500" />

            <span>
              {venue.happyHour}
            </span>

          </div>

        </div>

        {/* DEAL */}
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-3 rounded-lg mb-3">

          <p className="text-sm font-medium">
            {venue.deal}
          </p>
          
        </div>

        {/* FOOD TAGS */}
        <div className="flex flex-wrap gap-2 mb-4">

          {venue.foodType?.map((type, idx) => (
            <span
              key={idx}
              className="px-2 py-1 bg-gray-100 text-xs rounded-full text-gray-700"
            >
              {type}
            </span>
          ))}
          
        </div>
          
        {/* BUTTON */}
        <button
          onClick={onViewDetails}
          className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 rounded-xl hover:shadow-lg transition-all duration-300"
        >
          View Details & Reserve
        </button>

      </div>

    </div>
  );
}