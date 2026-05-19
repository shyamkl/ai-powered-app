const BASE_URL = "http://127.0.0.1:8000";

export const getVenues = async () => {
  const res = await fetch(`${BASE_URL}/venues`);
  return res.json();
};