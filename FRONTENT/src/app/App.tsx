import { useState, useRef, useEffect  } from 'react';
import { Menu, X, User, Briefcase, MapPin, Star, Crown, QrCode, Mail, Phone, Search, Map, Box } from 'lucide-react';
import { VenueCard } from './components/VenueCard';
import { FilterPanel } from './components/FilterPanel';
import { AIRecommendations } from './components/AIRecommendations';
import { AIChatbot } from './components/AIChatbot';
import { LoginModal } from './components/LoginModal';
import { PremiumModal } from './components/PremiumModal';
import { VenueDetailsModal } from './components/VenueDetailsModal';
import { fetchVenues, Venue } from './services/api';
import VenueMap from './components/VenueMap';

export default function App() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [loginModalOpen, setLoginModalOpen] = useState(false);
  const [loginType, setLoginType] = useState<'customer' | 'vendor'>('customer');
  const [isPremiumMember, setIsPremiumMember] = useState(false);
  const [premiumModalOpen, setPremiumModalOpen] = useState(false);
  const [venueDetailsModalOpen, setVenueDetailsModalOpen] = useState(false);
  const [selectedVenue, setSelectedVenue] = useState<typeof venues[0] | null>(null);
  const [favorites, setFavorites] = useState<number[]>([]);
  const [sortBy, setSortBy] = useState('distance');
  const [viewMode, setViewMode] = useState<'grid' | 'map'>('grid');
  const [userLocation, setUserLocation] = useState('India');
  const [searchQuery, setSearchQuery] = useState('');
  const [reviews, setReviews] = useState<any[]>([]);
  const [reviewName, setReviewName] = useState('');
  const [reviewComment, setReviewComment] = useState('');
  const [reviewRating, setReviewRating] = useState(5);
  const [reviewImage, setReviewImage] = useState<File | null>(null);
  const [userCoordinates, setUserCoordinates] = useState<{
  lat: number;
  lon: number;
} | null>(null);
  const [filters, setFilters] = useState({
    country: '',
    state: '',
    city: '',
    area: '',
    venueType: '',
    foodType: '',
    drinkType: '',
    menuType: '',
    showPremiumOnly: false
  });
  const [venues, setVenues] = useState<Venue[]>([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState('');
  const mapSectionRef = useRef<HTMLDivElement>(null);
  const [currentPage, setCurrentPage] = useState(1);

const [totalPages, setTotalPages] = useState(1);

const ITEMS_PER_PAGE = 50;

  // const venues = [
  //   {
  //     id: 1,
  //     name: 'Sky Bar Bangkok',
  //     type: 'Bar',
  //     image: 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800',
  //     rating: 4.9,
  //     reviews: 823,
  //     distance: '0.8 km',
  //     happyHour: '5:00 PM - 7:00 PM',
  //     deal: '40% off all cocktails & premium spirits',
  //     address: 'Silom, Bangkok',
  //     crowdLevel: 'Medium',
  //     foodType: ['Non-Veg', 'Veg'],
  //     drinkTypes: ['Cocktails', 'Wine'],
  //     isPremium: true,
  //     menuType: ['A la Carte'],
  //     country: 'Thailand',
  //     state: 'Bangkok',
  //     city: 'Bangkok'
  //   },
  //   {
  //     id: 2,
  //     name: 'Soi 11 Pub',
  //     type: 'Pub',
  //     image: 'https://images.unsplash.com/photo-1436076863939-06870fe779c2?w=800',
  //     rating: 4.7,
  //     reviews: 456,
  //     distance: '1.2 km',
  //     happyHour: '4:00 PM - 8:00 PM',
  //     deal: 'Buy 2 Get 1 free on all beers',
  //     address: 'Sukhumvit, Bangkok',
  //     crowdLevel: 'High',
  //     foodType: ['Non-Veg', 'Veg'],
  //     drinkTypes: ['Beer'],
  //     isPremium: false,
  //     menuType: ['A la Carte', 'Buffet'],
  //     country: 'Thailand',
  //     state: 'Bangkok',
  //     city: 'Bangkok'
  //   },
  //   {
  //     id: 3,
  //     name: 'Moonshine Lounge Mumbai',
  //     type: 'Lounge',
  //     image: 'https://images.unsplash.com/photo-1470337458703-46ad1756a187?w=800',
  //     rating: 4.8,
  //     reviews: 672,
  //     distance: '0.5 km',
  //     happyHour: '5:30 PM - 7:30 PM',
  //     deal: '₹299 unlimited beer & house spirits',
  //     address: 'Bandra West, Mumbai',
  //     crowdLevel: 'Low',
  //     foodType: ['Non-Veg', 'Veg'],
  //     drinkTypes: ['Beer', 'Whiskey', 'Cocktails'],
  //     isPremium: true,
  //     menuType: ['A la Carte'],
  //     country: 'India',
  //     state: 'Maharashtra',
  //     city: 'Mumbai'
  //   },
  //   {
  //     id: 4,
  //     name: 'The Biere Club Bangalore',
  //     type: 'Pub',
  //     image: 'https://images.unsplash.com/photo-1572116469696-31de0f17cc34?w=800',
  //     rating: 4.6,
  //     reviews: 534,
  //     distance: '2.1 km',
  //     happyHour: '4:00 PM - 7:00 PM',
  //     deal: '50% off craft beers & imported ales',
  //     address: 'Indiranagar, Bangalore',
  //     crowdLevel: 'Medium',
  //     foodType: ['Non-Veg', 'Veg'],
  //     drinkTypes: ['Beer', 'Wine'],
  //     isPremium: true,
  //     menuType: ['A la Carte'],
  //     country: 'India',
  //     state: 'Karnataka',
  //     city: 'Bangalore'
  //   },
  //   {
  //     id: 5,
  //     name: 'Social Delhi',
  //     type: 'Restaurant',
  //     image: 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800',
  //     rating: 4.5,
  //     reviews: 892,
  //     distance: '1.8 km',
  //     happyHour: '3:00 PM - 6:00 PM',
  //     deal: '₹199 house cocktails & ₹99 beers',
  //     address: 'Hauz Khas Village, Delhi',
  //     crowdLevel: 'High',
  //     foodType: ['Non-Veg', 'Veg', 'Vegan'],
  //     drinkTypes: ['Cocktails', 'Beer'],
  //     isPremium: false,
  //     menuType: ['A la Carte', 'Set Menu'],
  //     country: 'India',
  //     state: 'Delhi',
  //     city: 'Delhi'
  //   },
  //   {
  //     id: 6,
  //     name: 'Octave Rooftop Bangkok',
  //     type: 'Bar',
  //     image: 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800',
  //     rating: 4.9,
  //     reviews: 1023,
  //     distance: '3.5 km',
  //     happyHour: '6:00 PM - 8:00 PM',
  //     deal: '2 for 1 on signature cocktails',
  //     address: 'Thonglor, Bangkok',
  //     crowdLevel: 'Low',
  //     foodType: ['Non-Veg', 'Veg'],
  //     drinkTypes: ['Cocktails', 'Wine', 'Whiskey'],
  //     isPremium: true,
  //     menuType: ['A la Carte'],
  //     country: 'Thailand',
  //     state: 'Bangkok',
  //     city: 'Bangkok'
  //   },
  //   {
  //     id: 7,
  //     name: 'Hard Rock Cafe Pune',
  //     type: 'Restaurant',
  //     image: 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800',
  //     rating: 4.4,
  //     reviews: 445,
  //     distance: '2.8 km',
  //     happyHour: '4:30 PM - 7:30 PM',
  //     deal: 'Buy 1 Get 1 on all beverages',
  //     address: 'Koregaon Park, Pune',
  //     crowdLevel: 'Medium',
  //     foodType: ['Non-Veg', 'Veg'],
  //     drinkTypes: ['Beer', 'Cocktails'],
  //     isPremium: false,
  //     menuType: ['A la Carte'],
  //     country: 'India',
  //     state: 'Maharashtra',
  //     city: 'Pune'
  //   },
  //   {
  //     id: 8,
  //     name: 'Toit Brewpub Bangalore',
  //     type: 'Pub',
  //     image: 'https://images.unsplash.com/photo-1436076863939-06870fe779c2?w=800',
  //     rating: 4.7,
  //     reviews: 1256,
  //     distance: '1.5 km',
  //     happyHour: '12:00 PM - 7:00 PM',
  //     deal: '₹150 craft beers all day',
  //     address: 'Indiranagar, Bangalore',
  //     crowdLevel: 'High',
  //     foodType: ['Non-Veg', 'Veg'],
  //     drinkTypes: ['Beer'],
  //     isPremium: true,
  //     menuType: ['A la Carte'],
  //     country: 'India',
  //     state: 'Karnataka',
  //     city: 'Bangalore'
  //   }
  // ];
  useEffect(() => {
  loadVenues();
}, [filters,currentPage]);
useEffect(() => {

  if (venues?.id) {

    fetchReviews(venues.id)
      .then(data => setReviews(data))
      .catch(console.error);
   loadReviews();    
  }

}, [venues]);
useEffect(() => {

  navigator.geolocation.getCurrentPosition(

    (position) => {

      setUserCoordinates({
        lat: position.coords.latitude,
        lon: position.coords.longitude
      });

      console.log(
        "USER LOCATION:",
        position.coords.latitude,
        position.coords.longitude
      );
    },

    (error) => {
      console.error("Location error:", error);
    }

  );

}, []);
const loadVenues = async () => {
  try {
    setLoading(true);
    console.log("FILTERS BEFORE API:", filters);
  const data = await fetchVenues({
  country: filters.country?.trim(),
state: filters.state?.trim(),
city: filters.city?.trim(),
area: filters.area?.trim(),
search: searchQuery,
category: filters.venueType?.trim(),
  

  food_type: filters.foodType,
  drink_type: filters.drinkType,
  menu_type: filters.menuType,

  premium_only: filters.showPremiumOnly,

  page: currentPage,
  limit: ITEMS_PER_PAGE,
});
  console.log("FULL API RESPONSE:", data);
console.log("TOTAL VENUES:", data.length);
    const transformedData = data.map((venue: any) => ({
      id: venue.id,
      name: venue.name,
      lat: venue.lat,
      lon: venue.lon,
      type: (venue.category || "Venue").toLowerCase(),
      area: venue.area || "",

      image:
        venue.image_url ||
        "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800",

      rating: venue.rating || 4.5,

      reviews: venue.reviews_count || 0,

      distance: "Nearby",

      happyHour: venue.timing || "Happy Hours Available",

      deal: venue.deal || "Special offers available",

      address: venue.address || "Address unavailable",

      crowdLevel: "Medium",

      foodType: venue.food_type
      ? [venue.food_type]
      : [],

      drinkTypes: venue.drink_type
      ? [venue.drink_type]
      : [],

      isPremium: venue.is_premium || false,

      menuType: venue.menu_type
      ? [venue.menu_type]
      : [],

      country: venue.country || "",

      state: venue.state || "",

      city: venue.city || "",
    }));

    setVenues(transformedData);

  } catch (err) {
    console.error(err);
    setError("Failed to load venues");
  } finally {
    setLoading(false);
  }
};
  const handleFilterChange = (key: string, value: string | boolean) => {

  setFilters(prev => {

    const updated = {
      ...prev,
      [key]: value
    };

    // RESET DEPENDENT FILTERS

    if (key === "country") {
      updated.state = "";
      updated.city = "";
      updated.area = "";
    }

    if (key === "state") {
      updated.city = "";
      updated.area = "";
    }

    if (key === "city") {
      updated.area = "";
    }

    if (key === "venueType"){
      updated.drinkType = "";
    }
    return updated;
  });

  setCurrentPage(1);
};

  const toggleFavorite = (id: number) => {
    setFavorites(prev =>
      prev.includes(id) ? prev.filter(fav => fav !== id) : [...prev, id]
    );
  };

  const handleViewDetails = (venue: typeof venues[0]) => {
    setSelectedVenue(venue);
    setVenueDetailsModalOpen(true);
  };

  const handleMapViewToggle = () => {
    if (viewMode === 'grid') {
      setViewMode('map');
      setTimeout(() => {
        mapSectionRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    } else {
      setViewMode('grid');
    }
  };

  const handlePremiumSubscribe = () => {
    setIsPremiumMember(true);
    alert('Welcome to Premium! Enjoy your exclusive benefits.');
  };

  // const filteredVenues = venues.filter(venue => {
  //   if (filters.country && venue.country !== filters.country) return false;
  //   if (filters.state && venue.state !== filters.state) return false;
  //   if (filters.city && venue.city !== filters.city) return false;
  //   if (filters.venueType && venue.type !== filters.venueType) return false;
  //   if (filters.foodType && !venue.foodType.includes(filters.foodType)) return false;
  //   if (filters.drinkType && !venue.drinkTypes.includes(filters.drinkType)) return false;
  //   if (filters.menuType && !venue.menuType.includes(filters.menuType)) return false;
  //   if (filters.showPremiumOnly && !venue.isPremium) return false;
  //   return true;
  // });

  const sortedVenues = [...venues].sort((a, b) => {
    switch (sortBy) {
      case 'distance':
        return parseFloat(a.distance) - parseFloat(b.distance);
      case 'rating':
        return b.rating - a.rating;
      case 'deals':
        return b.reviews - a.reviews;
      default:
        return 0;
    }
  });
  const handleSearch = () => {

  // RESET NON-LOCATION FILTERS
  setFilters(prev => ({
    ...prev,

    area: '',
    venueType: '',
    foodType: '',
    drinkType: '',
    menuType: '',
    showPremiumOnly: false
  }));

  setCurrentPage(1);

  loadVenues();
};

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-md sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <Star className="w-8 h-8 text-blue-600 fill-blue-600" />
              <span className="text-2xl">HappyHourFinder</span>
            </div>

            <div className="hidden md:flex items-center gap-6">
              <button
                onClick={handleMapViewToggle}
                className="flex items-center gap-2 text-gray-700 hover:text-blue-600 transition-colors"
              >
                <Map className="w-5 h-5" />
                <span>{viewMode === 'grid' ? 'Map View' : 'Grid View'}</span>
              </button>
              {/* <button
                onClick={() => {
                  setLoginType('customer');
                  setLoginModalOpen(true);
                }}
                className="flex items-center gap-2 text-gray-700 hover:text-blue-600 transition-colors"
              >
                <User className="w-5 h-5" />
                <span>Customer Login</span>
              </button> */}
              {/* <button
                onClick={() => {
                  setLoginType('vendor');
                  setLoginModalOpen(true);
                }}
                className="flex items-center gap-2 text-gray-700 hover:text-purple-600 transition-colors"
              >
                <Briefcase className="w-5 h-5" />
                <span>Vendor Login</span>
              </button> */}
              {/* <button
                onClick={() => setPremiumModalOpen(true)}
                className={`flex items-center gap-2 px-4 py-2 rounded-xl transition-all ${
                  isPremiumMember
                    ? 'bg-gradient-to-r from-amber-500 to-yellow-500 text-white shadow-lg'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <Crown className="w-5 h-5" />
                <span>{isPremiumMember ? 'Premium Active' : 'Go Premium'}</span>
              </button> */}
            </div>

            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

          {mobileMenuOpen && (
            <div className="md:hidden py-4 space-y-3 border-t border-gray-200">
              <button
                onClick={() => {
                  handleMapViewToggle();
                  setMobileMenuOpen(false);
                }}
                className="flex items-center gap-2 w-full px-4 py-2 text-gray-700"
              >
                <Map className="w-5 h-5" />
                <span>{viewMode === 'grid' ? 'Map View' : 'Grid View'}</span>
              </button>
              {/* <button
                onClick={() => {
                  setLoginType('customer');
                  setLoginModalOpen(true);
                  setMobileMenuOpen(false);
                }}
                className="flex items-center gap-2 w-full px-4 py-2 text-gray-700"
              >
                <User className="w-5 h-5" />
                <span>Customer Login</span>
              </button> */}
              {/* <button
                onClick={() => {
                  setLoginType('vendor');
                  setLoginModalOpen(true);
                  setMobileMenuOpen(false);
                }}
                className="flex items-center gap-2 w-full px-4 py-2 text-gray-700"
              >
                <Briefcase className="w-5 h-5" />
                <span>Vendor Login</span>
              </button> */}
              {/* <button
                onClick={() => {
                  setPremiumModalOpen(true);
                  setMobileMenuOpen(false);
                }}
                className={`flex items-center gap-2 w-full px-4 py-2 rounded-xl ${
                  isPremiumMember ? 'bg-amber-500 text-white' : 'bg-gray-100 text-gray-700'
                }`}
              >
                <Crown className="w-5 h-5" />
                <span>{isPremiumMember ? 'Premium Active' : 'Go Premium'}</span>
              </button> */}
            </div>
          )}
        </div>
      </nav>

      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white py-16 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl mb-4">Discover the Best Happy Hours Near You</h1>
          <p className="text-xl mb-8 opacity-90">AI-powered recommendations, live crowd updates, and unbeatable deals</p>

          <div className="max-w-2xl mx-auto bg-white rounded-2xl p-2 flex gap-2">
            <input 
              type="text"
              placeholder="Search venue name..."
              className="flex-1 px-4 py-3 rounded-xl text-gray-800 focus:outline-none"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button
              onClick={handleSearch}
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-xl hover:shadow-lg transition-all flex items-center gap-2"
              >
              <Search className="w-5 h-5" />
              <span className="hidden sm:inline">Search</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* AI Recommendations */}
        <div className="mb-8">
          <AIRecommendations />
        </div>

        {/* Sort Options */}
        <div className="mb-6 flex flex-wrap gap-4 items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-gray-700">Sort by:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="distance">Nearest First</option>
              <option value="rating">Highest Rated</option>
              <option value="deals">Best Deals</option>
            </select>
          </div>
          <div className="text-gray-600">
            {sortedVenues.length} venues found
          </div>
        </div>

        {/* Grid Layout */}
        <div className="grid lg:grid-cols-4 gap-6">
          {/* Filters Sidebar */}
          <div className="lg:col-span-1">
            <FilterPanel filters={filters} onFilterChange={handleFilterChange} />
          </div>

          {/* Venues Grid */}
          <div className="lg:col-span-3">
            {loading && (
              <div className="text-center py-10">
                  <p className="text-xl text-gray-600">Loading venues...</p>
              </div>        
            )}

            {error && (
              <div className="text-center py-10">
                <p className="text-red-500">{error}</p>
              </div>
            )}

            {viewMode === 'grid' ? (

            <div className="grid md:grid-cols-2 gap-6">
              {sortedVenues.map((venue) => (
                <VenueCard
                  key={venue.id}
                  venue={venue}
                  isPremiumMember={isPremiumMember}
                  onFavorite={toggleFavorite}
                  isFavorited={favorites.includes(venue.id)}
                  onViewDetails={() => handleViewDetails(venue)}
                />
              ))}
            </div>
      
            ) : (
            
            <div
              ref={mapSectionRef}
              className="bg-white rounded-2xl shadow-lg p-4"
            >
              <VenueMap
                venues={sortedVenues}
                userCoordinates={userCoordinates}
              />

              <div className="mt-4 text-center">
                <button
                  onClick={() => setViewMode('grid')}
                  className="px-6 py-3 bg-blue-600 text-white rounded-xl hover:shadow-lg transition-all"
                >
                  Back to Grid View
                </button>
              </div>
            </div>

            )}
            <div className="flex justify-center items-center gap-4 mt-8">
              <button
                onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                disabled={currentPage === 1}
                className="px-4 py-2 bg-gray-200 rounded-lg disabled:opacity-50"
              >
                Previous
              </button>

              <span className="text-lg font-medium">
                Page {currentPage}
              </span>

              <button
                onClick={() => setCurrentPage(prev => prev + 1)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg"
              >
                Next
              </button>
            </div>
          </div>
        </div>

  
        {/* AR Feature Banner */}
        <div className="mt-12 bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl p-8 text-white text-center">
          <Box className="w-12 h-12 mx-auto mb-4" />
          <h3 className="text-3xl mb-3">AR Menu Preview Coming Soon!</h3>
          <p className="text-lg opacity-90 mb-4">
            Visualize drinks and dishes on your table before ordering with Augmented Reality
          </p>
          <button className="bg-white text-purple-600 px-8 py-3 rounded-xl hover:shadow-lg transition-all">
            Learn More
          </button>
         
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white mt-16">
        <div className="max-w-7xl mx-auto px-4 py-12">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <h4 className="text-xl mb-4 flex items-center gap-2">
                <Star className="w-6 h-6 fill-blue-500 text-blue-500" />
                HappyHourFinder
              </h4>
              <p className="text-gray-400 text-sm">
                Discover the best happy hour deals near you with AI-powered recommendations
              </p>
            </div>

            <div>
              <h4 className="text-lg mb-4">Quick Links</h4>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li><a href="#" className="hover:text-white transition-colors">About Us</a></li>
                <li><a href="#" className="hover:text-white transition-colors">How It Works</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Premium Membership</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Vendor Portal</a></li>
              </ul>
            </div>

            <div>
              <h4 className="text-lg mb-4">Contact Us</h4>
              <div className="space-y-3 text-gray-400 text-sm">
                <div className="flex items-center gap-2">
                  <Mail className="w-4 h-4" />
                  <span>support@happyhourfinder.com</span>
                </div>
                <div className="flex items-center gap-2">
                  <Phone className="w-4 h-4" />
                  <span>1-800-HAPPY-HR</span>
                </div>
              </div>
            </div>

            <div>
              <h4 className="text-lg mb-4">Scan for Mobile App</h4>
              <div className="bg-white p-4 rounded-xl inline-block">
                <QrCode className="w-24 h-24 text-gray-900" />
              </div>
              <p className="text-gray-400 text-xs mt-2">Scan to download our app</p>
            </div>
          </div>

          <div className="border-t border-gray-800 pt-8 text-center text-gray-400 text-sm">
            <p>&copy; 2026 HappyHourFinder. All rights reserved. Drink Responsibly.</p>
          </div>
        </div>
      </footer>

      {/* Modals & Floating Components */}
      <LoginModal
        isOpen={loginModalOpen}
        onClose={() => setLoginModalOpen(false)}
        type={loginType}
      />
      <PremiumModal
        isOpen={premiumModalOpen}
        onClose={() => setPremiumModalOpen(false)}
        onSubscribe={handlePremiumSubscribe}
        userLocation={userLocation}
        isPremiumMember={isPremiumMember}
      />
      <VenueDetailsModal
        isOpen={venueDetailsModalOpen}
        onClose={() => setVenueDetailsModalOpen(false)}
        venue={selectedVenue}
      />
      <AIChatbot />
    </div>
  );
}
