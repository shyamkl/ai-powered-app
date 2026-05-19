import { Filter, MapPin, Utensils, Wine, DollarSign } from 'lucide-react';

interface FilterPanelProps {
  filters: {
    country: string;
    state: string;
    city: string;
    venueType: string;
    foodType: string;
    drinkType: string;
    menuType: string;
    showPremiumOnly: boolean;
  };
  onFilterChange: (key: string, value: string | boolean) => void;
}

export function FilterPanel({ filters, onFilterChange }: FilterPanelProps) {
  return (
    <div className="bg-white rounded-2xl shadow-lg p-6 sticky top-4">
      <div className="flex items-center gap-2 mb-6">
        <Filter className="w-5 h-5 text-blue-600" />
        <h3 className="text-xl">Filters</h3>
      </div>

      <div className="space-y-5">
        {/* Location */}
        <div>
          <label className="flex items-center gap-2 text-sm mb-2 text-gray-700">
            <MapPin className="w-4 h-4" />
            Country
          </label>
          <select
            value={filters.country}
            onChange={(e) => onFilterChange('country', e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Countries</option>
            <option value="Thailand">Thailand</option>
            <option value="India">India</option>
          </select>
        </div>

        <div>
          <label className="text-sm mb-2 block text-gray-700">State/Province</label>
          <select
            value={filters.state}
            onChange={(e) => onFilterChange('state', e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All States</option>
            <option value="Bangkok">Bangkok</option>
            <option value="Maharashtra">Maharashtra</option>
            <option value="Karnataka">Karnataka</option>
            <option value="Delhi">Delhi</option>
            <option value="Tamil Nadu">Tamil Nadu</option>
          </select>
        </div>

        <div>
          <label className="text-sm mb-2 block text-gray-700">City</label>
          <select
            value={filters.city}
            onChange={(e) => onFilterChange('city', e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Cities</option>
            <option value="Bangkok">Bangkok</option>
            <option value="Mumbai">Mumbai</option>
            <option value="Bangalore">Bangalore</option>
            <option value="Delhi">Delhi</option>
            <option value="Chennai">Chennai</option>
            <option value="Pune">Pune</option>
            <option value="Hyderabad">Hyderabad</option>
          </select>
        </div>

        {/* Venue Type */}
        <div>
          <label className="flex items-center gap-2 text-sm mb-2 text-gray-700">
            <Utensils className="w-4 h-4" />
            Venue Type
          </label>
          <select
            value={filters.venueType}
            onChange={(e) => onFilterChange('venueType', e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Venues</option>
            <option value="Restaurant">Restaurant</option>
            <option value="Pub">Pub</option>
            <option value="Bar">Bar</option>
            <option value="Lounge">Lounge</option>
          </select>
        </div>

        {/* Food Type */}
        <div>
          <label className="text-sm mb-2 block text-gray-700">Food Preference</label>
          <select
            value={filters.foodType}
            onChange={(e) => onFilterChange('foodType', e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All</option>
            <option value="Veg">Vegetarian</option>
            <option value="Non-Veg">Non-Vegetarian</option>
            <option value="Vegan">Vegan</option>
          </select>
        </div>

        {/* Drink Type */}
        <div>
          <label className="flex items-center gap-2 text-sm mb-2 text-gray-700">
            <Wine className="w-4 h-4" />
            Drink Type
          </label>
          <select
            value={filters.drinkType}
            onChange={(e) => onFilterChange('drinkType', e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Drinks</option>
            <option value="Beer">Beer</option>
            <option value="Wine">Wine</option>
            <option value="Cocktails">Cocktails</option>
            <option value="Whiskey">Whiskey</option>
          </select>
        </div>

        {/* Menu Type */}
        <div>
          <label className="text-sm mb-2 block text-gray-700">Menu Type</label>
          <select
            value={filters.menuType}
            onChange={(e) => onFilterChange('menuType', e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All</option>
            <option value="A la Carte">A la Carte</option>
            <option value="Buffet">Buffet</option>
            <option value="Set Menu">Set Menu</option>
          </select>
        </div>

        {/* Premium Toggle */}
        <div>
          <label className="flex items-center gap-2 text-sm text-gray-700 cursor-pointer">
            <input
              type="checkbox"
              checked={filters.showPremiumOnly}
              onChange={(e) => onFilterChange('showPremiumOnly', e.target.checked)}
              className="w-5 h-5 text-amber-600 rounded focus:ring-2 focus:ring-amber-500"
            />
            <DollarSign className="w-4 h-4 text-amber-600" />
            <span>Premium Venues Only</span>
          </label>
        </div>

        <button
          onClick={() => {
            Object.keys(filters).forEach(key => {
              onFilterChange(key, key === 'showPremiumOnly' ? false : '');
            });
          }}
          className="w-full py-2 text-sm text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
        >
          Clear All Filters
        </button>
      </div>
    </div>
  );
}
