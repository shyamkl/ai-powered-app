const BASE_URL = "http://127.0.0.1:8000";

export const fetchVenues = async (params?: {
  area?: string;
  category?: string;
  city?: string;
}) => {
  const query = new URLSearchParams(params as any).toString();

  const res = await fetch(`${BASE_URL}/venues?${query}`);
  return res.json();
};