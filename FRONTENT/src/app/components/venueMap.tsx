import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMap
} from 'react-leaflet';

import L from 'leaflet';
import React, { useEffect } from 'react';

import 'leaflet/dist/leaflet.css';

delete (L.Icon.Default.prototype as any)._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',

  iconUrl:
    'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',

  shadowUrl:
    'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});
function ChangeMapView({
  center
}: {
  center: [number, number];
}) {

  const map = useMap();

  useEffect(() => {
    map.setView(center, 13);
  }, [center, map]);

  return null;
}
export default function VenueMap({
  venues,
  userCoordinates
}: any){

  console.log("MAP VENUES:", venues);

  // DEFAULT CENTER
 let center: [number, number] = [13.0827, 80.2707];

// PRIORITY 1 → USER LOCATION
if (
  userCoordinates &&
  userCoordinates.lat &&
  userCoordinates.lon
) {
  center = [
    userCoordinates.lat,
    userCoordinates.lon
  ];
}

// PRIORITY 2 → FIRST VENUE
else if (
  venues &&
  venues.length > 0 &&
  venues[0].lat &&
  venues[0].lon
) {
  center = [
    Number(venues[0].lat),
    Number(venues[0].lon)
  ];
}

  return (
    <MapContainer
      center={center}
      zoom={12}
      style={{
        height: '600px',
        width: '100%',
        borderRadius: '16px'
      }}
    >
      <ChangeMapView center={center} /> 
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {venues.map((venue: any) => {

        console.log(
          "MARKER:",
          venue.name,
          venue.lat,
          venue.lon
        );

        if (!venue.lat || !venue.lon) {
          return null;
        }

        return (
          <Marker
            key={venue.id}
            position={[
              Number(venue.lat),
              Number(venue.lon)
            ]}
          >
            <Popup>
              <div>
                <h3 className="font-bold">
                  {venue.name}
                </h3>

                <p>{venue.address}</p>

                <p>
                  ⭐ {venue.rating}
                </p>

                <p>
                  🎉 {venue.deal}
                </p>
              </div>
            </Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
}