import { Filter, MapPin, Utensils, Wine, DollarSign } from 'lucide-react';

interface FilterPanelProps {
  filters: {
    country: string;
    state: string;
    city: string;
    area: string;
    venueType: string;
    foodType: string;
    drinkType: string;
    menuType: string;
    showPremiumOnly: boolean;
  };

  onFilterChange: (key: string, value: string | boolean) => void;
}

export function FilterPanel({
  filters,
  onFilterChange,
}: FilterPanelProps) {
  const stateOptions: Record<string, string[]> = {
    India: [
      'Tamil Nadu',
      'Maharashtra',
    ],

    Thailand: ['Bangkok'],
  };

  const cityOptions: Record<string, string[]> = {
    India: [
      'Chennai',
      'Mumbai',
      
    ],

    Thailand: ['Bangkok'],
  };
  const stateCityMap: Record<string, string[]> = {
  "Tamil Nadu": [
    "Chennai",
  ],

  "Maharashtra": [
    "Mumbai",
  ],

 
  "Bangkok": [
    "Bangkok"
  ]
};
  return (
    <div className="bg-white rounded-2xl shadow-lg p-6 sticky top-4">
      <div className="flex items-center gap-2 mb-6">
        <Filter className="w-5 h-5 text-blue-600" />
        <h3 className="text-xl font-semibold">Filters</h3>
      </div>

      <div className="space-y-5">

        {/* COUNTRY */}
        <div>
          <label className="flex items-center gap-2 text-sm mb-2 text-gray-700">
            <MapPin className="w-4 h-4" />
            Country
          </label>

          <select
            value={filters.country}
            onChange={(e) =>
              onFilterChange('country', e.target.value)
            }
            className="w-full p-3 border border-gray-300 rounded-lg"
          >
            <option value="">All Countries</option>

            <option value="India">India</option>
            <option value="Thailand">Thailand</option>
          </select>
        </div>

        {/* STATE */}
        <div>
          <label className="text-sm mb-2 block text-gray-700">
            State
          </label>

          <select
            value={filters.state}
            onChange={(e) =>
              onFilterChange('state', e.target.value)
            }
            className="w-full p-3 border border-gray-300 rounded-lg"
          >
            <option value="">All States</option>

            {filters.country &&
              stateOptions[filters.country]?.map((state) => (
                <option key={state} value={state}>
                  {state}
                </option>
              ))}
          </select>
        </div>

        {/* CITY */}
              <div>
                <label className="text-sm mb-2 block text-gray-700">
                  City
                </label>

                <select
                  value={filters.city}
                  onChange={(e) =>
                    onFilterChange("city", e.target.value)
                  }
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">All Cities</option>

                  {filters.state &&
                    stateCityMap[filters.state]?.map((city) => (
                      <option key={city} value={city}>
                        {city}
                      </option>
                    ))}
                </select>
              </div>

        {/* AREA */}
          {/* Area Search */}
            <div>
              <label className="text-sm mb-2 block text-gray-700">
                Area / Locality
              </label>

              <input
                type="text"
                placeholder="Enter area (e.g. Bandra, Indiranagar)"
                value={filters.area}
                onChange={(e) =>
                  onFilterChange("area", e.target.value)
                }
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

        {/* VENUE TYPE */}
        <div>
          <label className="flex items-center gap-2 text-sm mb-2 text-gray-700">
            <Utensils className="w-4 h-4" />
            Venue Type
          </label>

          <select
            value={filters.venueType}
            onChange={(e) =>
              onFilterChange('venueType', e.target.value)
            }
            className="w-full p-3 border border-gray-300 rounded-lg"
          >
            <option value="">All Venue Types</option>

            <option value="restaurant">Restaurant</option>
            <option value="pub">Pub</option>
            <option value="bar">Bar</option>
            <option value="cafe">Cafe</option>
            <option value="fast_food">Fast Food</option>
            <option value="nightclub">Nightclub</option>
          </select>
        </div>

        {/* FOOD */}
        <div>
          <label className="text-sm mb-2 block text-gray-700">
            Food Preference
          </label>

          <select
            value={filters.foodType}
            onChange={(e) =>
              onFilterChange('foodType', e.target.value)
            }
            className="w-full p-3 border border-gray-300 rounded-lg"
          >
            <option value="">All</option>

            <option value="Veg">Vegetarian</option>
            <option value="Non-Veg">Non Vegetarian</option>
            <option value="Vegan">Vegan</option>
          </select>
        </div>

        {/* DRINK */}
          {["bar", "pub", "nightclub", "bar/pub"].includes(filters.venueType) && (
            <div>
              <label className="flex items-center gap-2 text-sm mb-2 text-gray-700">
                <Wine className="w-4 h-4" />
                Drink Type
              </label>

              <select
                value={filters.drinkType}
                onChange={(e) =>
                  onFilterChange("drinkType", e.target.value)
                }
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">All Drinks</option>
                <option value="Beer">Beer</option>
                <option value="Wine">Wine</option>
                <option value="Cocktails">Cocktails</option>
                <option value="Whiskey">Whiskey</option>
              </select>
            </div>
          )}
        {/* MENU */}
        <div>
          <label className="text-sm mb-2 block text-gray-700">
            Menu Type
          </label>

          <select
            value={filters.menuType}
            onChange={(e) =>
              onFilterChange('menuType', e.target.value)
            }
            className="w-full p-3 border border-gray-300 rounded-lg"
          >
            <option value="">All</option>

            <option value="A la Carte">A la Carte</option>
            <option value="Buffet">Buffet</option>
            <option value="Set Menu">Set Menu</option>
          </select>
        </div>

        {/* PREMIUM */}
        <div>
          <label className="flex items-center gap-2 text-sm text-gray-700 cursor-pointer">
            {/* <input
              type="checkbox"
              checked={filters.showPremiumOnly}
              onChange={(e) =>
                onFilterChange(
                  'showPremiumOnly',
                  e.target.checked
                )
              }
              className="w-5 h-5"
            /> */}

            {/* <DollarSign className="w-4 h-4 text-amber-600" /> */}

            {/* <span>Premium Venues Only</span> */}
          </label>
        </div>

        {/* CLEAR */}
        <button
          onClick={() => {
            Object.keys(filters).forEach((key) => {
              onFilterChange(
                key,
                key === 'showPremiumOnly' ? false : ''
              );
            });
          }}
          className="w-full py-2 text-sm text-blue-600 hover:bg-blue-50 rounded-lg"
        >
          Clear All Filters
        </button>
      </div>
    </div>
  );
}