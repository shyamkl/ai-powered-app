import { useEffect, useState } from "react";
import { fetchVenues } from "../services/api";

type Venue = {
  id: number;
  name: string;
  category: string;
  area: string;
  image_url: string;
  rating: number;
};

export default function Home() {
  const [venues, setVenues] = useState<Venue[]>([]);
  const [filters, setFilters] = useState({
    area: "",
    category: "",
    city: ""
  });

  useEffect(() => {
    loadData();
  }, [filters]);

  const loadData = async () => {
    const data = await fetchVenues(filters);
    setVenues(data);
  };

  return (
    <div>
      {/* Filters */}
      <div style={{ display: "flex", gap: 10 }}>
        <input
          placeholder="Area"
          value={filters.area}
          onChange={(e) =>
            setFilters({ ...filters, area: e.target.value })
          }
        />

        <input
          placeholder="Category"
          value={filters.category}
          onChange={(e) =>
            setFilters({ ...filters, category: e.target.value })
          }
        />

        <input
          placeholder="City"
          value={filters.city}
          onChange={(e) =>
            setFilters({ ...filters, city: e.target.value })
          }
        />
      </div>

      {/* Cards */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 20 }}>
        {venues.map((v) => (
          <div key={v.id} style={{ border: "1px solid #ccc", padding: 10 }}>
            <img src={v.image_url} width="100%" />
            <h3>{v.name}</h3>
            <p>{v.category}</p>
            <p>{v.area}</p>
            <p>⭐ {v.rating}</p>
          </div>
        ))}
      </div>
    </div>
  );
}