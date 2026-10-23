export const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ??
  (import.meta.env.DEV ? "http://127.0.0.1:8000" : "/api")
).replace(/\/$/, "");

export const apiUrl = (path: string) =>
  `${API_BASE_URL}/${path.replace(/^\/+/, "")}`;

export interface Venue {
  id: string | number;
  name: string;
  category: string;
  image_url: string;
  address: string;
  city: string;
  state: string;
  country: string;
  deal: string;
  timing: string;
  rating: number;
  reviews_count: number;
  area?: string;
  lat: number;
  lon: number;

  food_type?: string;
  drink_type?: string;
  menu_type?: string;

  is_premium?: boolean;
}

// ======================
// FETCH VENUES
// ======================


export async function fetchVenues(filters?: any) {

  const params = new URLSearchParams();

    if (filters?.latitude) {
    params.append("latitude", filters.latitude);
  }

  if (filters?.longitude) {
    params.append("longitude", filters.longitude);
  }

  if (filters?.country) {
    params.append("country", filters.country);
  }

  if (filters?.state) {
    params.append("state", filters.state);
  }

  if (filters?.city) {
    params.append("city", filters.city);
  }

  if (filters?.area) {
    params.append("area", filters.area);
  }

  if (filters?.category) {
    params.append("category", filters.category);
  }

  if (filters?.food_type) {
    params.append("food_type", filters.food_type);
  }

  if (filters?.drink_type) {
    params.append("drink_type", filters.drink_type);
  }

  if (filters?.menu_type) {
    params.append("menu_type", filters.menu_type);
  }

  if (filters?.search) {
    params.append("search", filters.search);
  }

  if (filters?.premium_only) {
    params.append("premium_only", "true");
  }

  params.append("page", String(filters?.page || 1));
  params.append("limit", String(filters?.limit || 50));
  console.log(
    "REQUEST URL:",
    `${API_BASE_URL}/venues?${params.toString()}`
  );
  const response = await fetch(
    `${API_BASE_URL}/venues?${params.toString()}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch venues");
  }

  return response.json();
}

// ======================
// CREATE REVIEW
// ======================

export const createReview = async (formData: FormData) => {

  const response = await fetch(
    `${API_BASE_URL}/reviews`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    throw new Error("Failed to submit review");
  }

  return response.json();
};

// ======================
// FETCH REVIEWS
// ======================

export const fetchReviews = async (venueId: string | number) => {

  const response = await fetch(
    `${API_BASE_URL}/reviews/${encodeURIComponent(String(venueId))}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch reviews");
  }

  return response.json();
};

// ======================
// CHATBOT
// ======================

export const sendChatMessage = async (message: string) => {

  const response = await fetch(
    `${API_BASE_URL}/chat`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        message,
      }),
    }
  );

  if (!response.ok) {
    throw new Error("Failed to send message");
  }

  return response.json();
};

// ======================
// FAVORITES
// ======================

export const addFavorite = async (venueId: number) => {
  const response = await fetch(`${API_BASE_URL}/favorites`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ venue_id: venueId }),
  });

  if (!response.ok) throw new Error("Failed to update favorite");
  return response.json();
};

export const removeFavorite = async (venueId: number) => {
  // The backend exposes a toggle endpoint, so posting an existing favorite removes it.
  const response = await fetch(`${API_BASE_URL}/favorites`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ venue_id: venueId }),
  });

  if (!response.ok) throw new Error("Failed to update favorite");
  return response.json();
};

export const fetchFavorites = async () => {

  const response = await fetch(
    `${API_BASE_URL}/favorites`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch favorites");
  }

  return response.json();
};

// =========================
// UPLOAD VENUE IMAGE
// =========================

export const uploadVenueImage = async (
  venueId: number,
  imageFile: File
) => {

  const formData = new FormData();

  formData.append("image", imageFile);

  const response = await fetch(
    `${API_BASE_URL}/venues/${venueId}/upload-image`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    throw new Error("Failed to upload image");
  }

  return response.json();
};

// ======================
// FETCH VENUE DEALS
// ======================

export interface VenueDeal {
   id: number;
  venue_id: string;
  title: string;
  description?: string | null;
  deal_type: string;
  category?: string | null;
  discount_value?: string | null;
  discount_unit?: string | null;
  items?: string[];
  days?: string[];
  start_time?: string | null;
  end_time?: string | null;
  source_url: string;
  source_type: string;
  confidence?: number | null;
  is_active?: boolean;
  verified_at?: string | null;
  first_seen_at?: string | null;
  last_seen_at?: string | null;
  created_at?: string | null;
  updated_at?: string | null;
}


export const fetchVenueDeals = async (
  venueId: string | number
): Promise<VenueDeal[]> => {
  const response = await fetch(
    `${API_BASE_URL}/deals/${encodeURIComponent(String(venueId))}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch venue deals");
  }

  const data = await response.json();

  return data.map((deal: any) => {
    let items: string[] = [];
    let days: string[] = [];

    try {
      if (Array.isArray(deal.items)) {
        items = deal.items;
      } else if (typeof deal.items === "string") {
        const parsed = JSON.parse(deal.items);
        items = Array.isArray(parsed) ? parsed : [];
      }
    } catch {
      items = [];
    }

    try {
      if (Array.isArray(deal.days)) {
        days = deal.days;
      } else if (typeof deal.days === "string") {
        const parsed = JSON.parse(deal.days);
        days = Array.isArray(parsed) ? parsed : [];
      }
    } catch {
      days = [];
    }

    return {
      ...deal,
      items,
      days,
    };
  });
};