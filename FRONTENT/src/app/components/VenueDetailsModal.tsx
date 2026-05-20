import { X, MapPin, Clock, Star, Users, Phone, Mail, Calendar, Upload, Send } from 'lucide-react';
import { useEffect, useState } from 'react';
import {
    fetchReviews,
    createReview
  } from '../services/api';

interface VenueDetailsModalProps {
  isOpen: boolean;
  onClose: () => void;
  venue: {
    id: number;
    name: string;
    type: string;
    image: string;
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
  } | null;
}

export function VenueDetailsModal({ isOpen, onClose, venue }: VenueDetailsModalProps) {
 
    const handleReservation = () => {

  alert(`Reservation request sent for ${venue.name}`);

};
  // const [reviews, setReviews] = useState<any[]>([]);
//   useEffect(() => {

//   if (venue?.id) {

//     loadReviews();

//   }

// }, [venue]);
useEffect(() => {
  if (isOpen && venue?.id) {
    loadReviews();
  }
}, [isOpen, venue]);
const loadReviews = async () => {
  if (!venue) return;

  try {
    setReviewLoading(true);

    const data = await fetchReviews(venue.id);

    setReviews(data);
  } catch (error) {
    console.error("Failed loading reviews:", error);
  } finally {
    setReviewLoading(false);
  }
};
  const [reservationData, setReservationData] = useState({
    name: '',
    email: '',
    phone: '',
    date: '',
    time: '',
    guests: '2'
  });

  
  const [reviews, setReviews] = useState<any[]>([]);
const [reviewLoading, setReviewLoading] = useState(false);

const [reviewName, setReviewName] = useState("");
const [reviewComment, setReviewComment] = useState("");
const [reviewRating, setReviewRating] = useState(5);
const [reviewImage, setReviewImage] = useState<File | null>(null);
  const [activeTab, setActiveTab] = useState<'details' | 'reserve' | 'reviews'>('details');

  if (!isOpen || !venue) return null;
  
  const handleReviewSubmit = async () => {

  const formData = new FormData();

  formData.append("venue_id", String(venue.id));
  formData.append("user_name", reviewName);
  formData.append("rating", String(reviewRating));
  formData.append("comment", reviewComment);

  if (reviewImage) {
    formData.append("image", reviewImage);
  }

  try {

    const response = await createReview(formData);

    console.log("REVIEW SUBMITTED:", response);

    // RELOAD REVIEWS
    await loadReviews();

    // CLEAR FORM
    setReviewName("");
    setReviewComment("");
    setReviewRating(5);
    setReviewImage(null);

    alert("Review submitted successfully");

  } catch (error) {

    console.error(error);

    alert("Failed to submit review");
  }
};
  
  const handlePhotoUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setReviewData(prev => ({
        ...prev,
        photos: [...prev.photos, ...Array.from(e.target.files!)]
      }));
    }
  };

  const existingReviews = [
    {
      id: 1,
      user: 'Priya Sharma',
      rating: 5,
      comment: 'Amazing happy hour deals! The rooftop ambiance is perfect for evening drinks.',
      date: '2 days ago',
      photos: ['https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=200']
    },
    {
      id: 2,
      user: 'Rahul Kumar',
      rating: 4,
      comment: 'Great selection of craft beers. Service was quick and friendly.',
      date: '1 week ago',
      photos: []
    }
  ];
  
  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-white rounded-3xl shadow-2xl max-w-4xl w-full my-8 relative max-h-[90vh] overflow-hidden flex flex-col">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 bg-white/90 backdrop-blur-sm text-gray-700 hover:text-gray-900 z-10 p-2 rounded-full shadow-lg"
        >
          <X className="w-6 h-6" />
        </button>

        {/* Hero Image */}
        <div className="relative h-64 overflow-hidden">
          <img src={venue.image} alt={venue.name} className="w-full h-full object-cover" />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
          <div className="absolute bottom-6 left-6 text-white">
            <h2 className="text-4xl mb-2">{venue.name}</h2>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-1 bg-white/20 backdrop-blur-sm px-3 py-1 rounded-full">
                <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                <span>{venue.rating}</span>
                <span className="text-sm">({venue.reviews} reviews)</span>
              </div>
              <span className="bg-white/20 backdrop-blur-sm px-3 py-1 rounded-full">{venue.type}</span>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200 bg-white sticky top-0 z-10">
          <div className="flex">
            <button
              onClick={() => setActiveTab('details')}
              className={`flex-1 py-4 px-6 text-center transition-colors ${
                activeTab === 'details'
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Details
            </button>
            <button
              onClick={() => setActiveTab('reserve')}
              className={`flex-1 py-4 px-6 text-center transition-colors ${
                activeTab === 'reserve'
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Reserve Table
            </button>
            <button
              onClick={() => setActiveTab('reviews')}
              className={`flex-1 py-4 px-6 text-center transition-colors ${
                activeTab === 'reviews'
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Reviews
            </button>
            <div className="mt-6">

  {/* <h3 className="text-xl font-bold mb-4">
    User Reviews
  </h3> */}

  

    {reviews.length === 0 ? (
  <p>No reviews yet</p>
) : (
  reviews.map((review: any) => (
    <div key={review.id} className="border-b pb-4 mb-4">
      <div className="flex items-center justify-between">
        {/* <h4 className="font-semibold">{review.user_name}</h4> */}
        {/* <span>{review.rating} ★</span> */}
      </div>

      <p className="text-sm text-gray-600 mt-1">
        {/* {review.comment} */}
      </p>

      {review.photos && review.photos.length > 0 && (
        <div className="flex gap-2 mt-3 flex-wrap">
          {review.photos.map((photo: string, index: number) => (
            <img
              key={index}
              src={`http://127.0.0.1:8000/${photo}`}
              alt=""
              className="w-24 h-24 object-cover rounded"
            />
          ))}
        </div>
      )}
    </div>
  ))
)}



</div>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {/* Details Tab */}
          {activeTab === 'details' && (
            <div className="space-y-6">
              <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-2xl border border-blue-100">
                <h3 className="text-xl mb-2">Happy Hour Special</h3>
                <p className="text-2xl text-blue-600 mb-2">{venue.deal}</p>
                <div className="flex items-center gap-2 text-gray-600">
                  <Clock className="w-5 h-5" />
                  <span>{venue.happyHour}</span>
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div className="flex items-start gap-3">
                    <MapPin className="w-5 h-5 text-blue-600 mt-1" />
                    <div>
                      <h4 className="font-medium mb-1">Location</h4>
                      <p className="text-gray-600">{venue.address}</p>
                      <p className="text-sm text-gray-500">{venue.distance} away</p>
                    </div>
                  </div>

                  <div className="flex items-start gap-3">
                    <Users className="w-5 h-5 text-orange-600 mt-1" />
                    <div>
                      <h4 className="font-medium mb-1">Crowd Level</h4>
                      <p className="text-gray-600">{venue.crowdLevel}</p>
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium mb-2">Food Options</h4>
                    <div className="flex flex-wrap gap-2">
                      {venue.foodType.map((type, idx) => (
                        <span key={idx} className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">
                          {type}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h4 className="font-medium mb-2">Drink Selection</h4>
                    <div className="flex flex-wrap gap-2">
                      {venue.drinkTypes.map((type, idx) => (
                        <span key={idx} className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">
                          {type}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h4 className="font-medium mb-2">Menu Type</h4>
                    <div className="flex flex-wrap gap-2">
                      {venue.menuType.map((type, idx) => (
                        <span key={idx} className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                          {type}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-gray-50 p-4 rounded-xl">
                <h4 className="font-medium mb-2">Contact Information</h4>
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-gray-600">
                    <Phone className="w-4 h-4" />
                    <span>+91 98765 43210</span>
                  </div>
                  <div className="flex items-center gap-2 text-gray-600">
                    <Mail className="w-4 h-4" />
                    <span>contact@{venue.name.toLowerCase().replace(/\s+/g, '')}.com</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Reserve Tab */}
          {activeTab === 'reserve' && (
            <div>
              <h3 className="text-2xl mb-6">Reserve Your Table</h3>
              <form onSubmit={handleReservation} className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm mb-2 text-gray-700">Full Name *</label>
                    <input
                      type="text"
                      required
                      value={reservationData.name}
                      onChange={(e) => setReservationData(prev => ({ ...prev, name: e.target.value }))}
                      className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="John Doe"
                    />
                  </div>


                  <div>
                    <label className="block text-sm mb-2 text-gray-700">Email *</label>
                    <input
                      type="email"
                      required
                      value={reservationData.email}
                      onChange={(e) => setReservationData(prev => ({ ...prev, email: e.target.value }))}
                      className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="john@example.com"
                    />
                  </div>

                  <div>
                    <label className="block text-sm mb-2 text-gray-700">Phone *</label>
                    <input
                      type="tel"
                      required
                      value={reservationData.phone}
                      onChange={(e) => setReservationData(prev => ({ ...prev, phone: e.target.value }))}
                      className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="+91 98765 43210"
                    />
                  </div>

                  <div>
                    <label className="block text-sm mb-2 text-gray-700">Number of Guests *</label>
                    <select
                      required
                      value={reservationData.guests}
                      onChange={(e) => setReservationData(prev => ({ ...prev, guests: e.target.value }))}
                      className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      {[1, 2, 3, 4, 5, 6, 7, 8].map(num => (
                        <option key={num} value={num}>{num} {num === 1 ? 'Guest' : 'Guests'}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm mb-2 text-gray-700">Date *</label>
                    <input
                      type="date"
                      required
                      value={reservationData.date}
                      onChange={(e) => setReservationData(prev => ({ ...prev, date: e.target.value }))}
                      className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>

                  <div>
                    <label className="block text-sm mb-2 text-gray-700">Time *</label>
                    <input
                      type="time"
                      required
                      value={reservationData.time}
                      onChange={(e) => setReservationData(prev => ({ ...prev, time: e.target.value }))}
                      className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 rounded-xl text-lg hover:shadow-lg transition-all flex items-center justify-center gap-2"
                >
                  <Calendar className="w-5 h-5" />
                  Confirm Reservation
                </button>
              </form>
            </div>
          )}

          {/* Reviews Tab */}
          {activeTab === 'reviews' && (
            <div className="space-y-8">
              {/* Write Review */}
              <div className="bg-gray-50 p-6 rounded-2xl">
                <h3 className="text-xl mb-4">Write a Review</h3>
                <form
  onSubmit={(e) => {
    e.preventDefault();
    handleReviewSubmit();
  }}
  className="space-y-4"
>

  <div>
    <label className="block text-sm mb-2 text-gray-700">
      Your Name
    </label>

    <input
      type="text"
      value={reviewName}
      onChange={(e) => setReviewName(e.target.value)}
      className="w-full p-3 border border-gray-300 rounded-xl"
      placeholder="Enter your name"
      required
    />
  </div>

  <div>
    <label className="block text-sm mb-2 text-gray-700">
      Your Rating
    </label>

    <div className="flex gap-2">
      {[1, 2, 3, 4, 5].map((star) => (
        <button
          key={star}
          type="button"
          onClick={() => setReviewRating(star)}
          className="focus:outline-none"
        >
          <Star
            className={`w-8 h-8 ${
              star <= reviewRating
                ? "fill-yellow-400 text-yellow-400"
                : "text-gray-300"
            }`}
          />
        </button>
      ))}
    </div>
  </div>

  <div>
    <label className="block text-sm mb-2 text-gray-700">
      Your Review
    </label>

    <textarea
      value={reviewComment}
      onChange={(e) => setReviewComment(e.target.value)}
      className="w-full p-3 border border-gray-300 rounded-xl h-24 resize-none"
      placeholder="Share your experience..."
      required
    />
  </div>

  <div>
    <label className="block text-sm mb-2 text-gray-700">
      Upload Photo (Optional)
    </label>

    <input
      type="file"
      onChange={(e) => {
        if (e.target.files?.[0]) {
          setReviewImage(e.target.files[0]);
        }
      }}
      className="w-full"
    />
  </div>

  <button
    type="submit"
    className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 rounded-xl hover:shadow-lg transition-all flex items-center justify-center gap-2"
  >
    <Send className="w-5 h-5" />
    Submit Review
  </button>

</form>
              </div>

              {/* Existing Reviews */}
              <div className="mt-6">
  <h3 className="text-xl font-bold mb-4">Reviews</h3>

  {reviewLoading ? (
    <p>Loading reviews...</p>
  ) : reviews.length === 0 ? (
    <p>No reviews yet</p>
  ) : (
    reviews.map((review: any) => (
      <div
        key={review.id}
        className="border rounded-lg p-4 mb-4"
      >
        <div className="flex justify-between">
          <h4 className="font-semibold">
            {review.user_name}
          </h4>

          <span>
            ⭐ {review.rating}
          </span>
        </div>

        <p className="mt-2">
          {review.comment}
        </p>

        {review.image_url && (
          <img
            src={`http://127.0.0.1:8000${review.image_url}`}
            alt="review"
            className="w-40 mt-3 rounded-lg"
          />
        )}
      </div>
    ))
  )}
</div>
              {/* <div>
                <h3 className="text-xl mb-4">Customer Reviews</h3>
                <div className="space-y-4">
                  {existingReviews.map(review => (
                    <div key={review.id} className="bg-white border border-gray-200 rounded-xl p-4">
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <h4 className="font-medium">{review.user}</h4>
                          <div className="flex items-center gap-2 mt-1">
                            <div className="flex">
                              {[1, 2, 3, 4, 5].map(star => (
                                <Star
                                  key={star}
                                  className={`w-4 h-4 ${
                                    star <= review.rating
                                      ? 'fill-yellow-400 text-yellow-400'
                                      : 'text-gray-300'
                                  }`}
                                />
                              ))}
                            </div>
                            <span className="text-sm text-gray-500">{review.date}</span>
                          </div>
                        </div>
                      </div>
                      <p className="text-gray-700 mb-3">{review.comment}</p>
                      {review.photos.length > 0 && (
                        <div className="flex gap-2">
                          {review.photos.map((photo, idx) => (
                            <img
                              key={idx}
                              src={photo}
                              alt="Review"
                              className="w-20 h-20 object-cover rounded-lg"
                            />
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div> */}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
