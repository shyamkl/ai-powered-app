const API_BASE_URL = "http://127.0.0.1:8000";

export interface Venue {
  id: number;
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
  area: string;
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

export const fetchReviews = async (venueId: number) => {

  const response = await fetch(
    `${API_BASE_URL}/reviews/${venueId}`
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

