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
}









// FETCH VENUES
export async function fetchVenues(filters?: {
  country?: string;
  state?: string;
  city?: string;
  area?: string;

  category?: string;

  food_type?: string;
  drink_type?: string;
  menu_type?: string;

  premium_only?: boolean;

  page?: number;
  limit?: number;

  search?: string;
}) {

  const params = new URLSearchParams();

  // LOCATION FILTERS
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

  // CATEGORY
  if (filters?.category) {
    params.append("category", filters.category);
  }

  // EXTRA FILTERS
  if (filters?.food_type) {
    params.append("food_type", filters.food_type);
  }

  if (filters?.drink_type) {
    params.append("drink_type", filters.drink_type);
  }

  if (filters?.menu_type) {
    params.append("menu_type", filters.menu_type);
  }

  if (filters?.premium_only) {
    params.append("premium_only", "true");
  }

  // SEARCH
  if (filters?.search) {
    params.append("search", filters.search);
  }

  // PAGINATION
  if (filters?.page) {
    params.append("page", filters.page.toString());
  }

  if (filters?.limit) {
    params.append("limit", filters.limit.toString());
  }

  const url = `${API_BASE_URL}/venues?${params.toString()}`;

  console.log("API URL:", url);

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Failed to fetch venues");
  }

  return response.json();
}









// CREATE REVIEW
export const createReview = async (formData: FormData) => {

  const response = await fetch(
    `${API_BASE_URL}/reviews`,
    {
      method: "POST",
      body: formData
    }
  );

  if (!response.ok) {
    throw new Error("Failed to submit review");
  }

  return response.json();
};









// FETCH REVIEWS
export const fetchReviews = async (venueId: number) => {

  const response = await fetch(
    `${API_BASE_URL}/reviews/${venueId}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch reviews");
  }

  return response.json();
};