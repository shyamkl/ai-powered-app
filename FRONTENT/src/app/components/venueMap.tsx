import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Circle,
  useMap
} from 'react-leaflet';
import './venueMap.css';
import L from 'leaflet';
import React, { useEffect } from 'react';

import 'leaflet-routing-machine';
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

const userIcon = new L.Icon({
  iconUrl:
    'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png',

  shadowUrl:
    'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',

  iconSize: [40, 65],
  iconAnchor: [20, 65],
  popupAnchor: [0, -60]
});
const navigationIcon = new L.Icon({
  iconUrl:
    'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-violet.png',

  shadowUrl:
    'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',

  iconSize: [35, 57],
  iconAnchor: [17, 57]
});
function MyLocationButton() {

  const map = useMap();

  const goToMyLocation = () => {

    navigator.geolocation.getCurrentPosition(
      (position) => {

        map.setView(
          [
            position.coords.latitude,
            position.coords.longitude
          ],
          15
        );

      }
    );

  };

  return (

    <button
      onClick={goToMyLocation}
      style={{
        position: "absolute",
        top: "10px",
        right: "10px",
        zIndex: 1000,
        background: "#2563eb",
        color: "white",
        padding: "10px 14px",
        borderRadius: "10px",
        border: "none",
        cursor: "pointer",
        fontWeight: "bold"
      }}
    >
      📍 My Location
    </button>

  );
}
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

function FitBounds({ venues }: any) {

  const map = useMap();

  useEffect(() => {

    if (!venues.length) return;

    const bounds = venues
      .filter((v:any)=>v.lat && v.lon)
      .map((v:any)=>[
        Number(v.lat),
        Number(v.lon)
      ]);

    map.fitBounds(bounds, {
      padding: [50, 50]
    });

  }, [venues]);

  return null;
}
function RoutingMachine({
  userCoordinates,
  liveLocation,
  selectedVenue
}: any) {

  const map = useMap();

  useEffect(() => {

    if (
      !userCoordinates ||
      !selectedVenue
    ) return;

    const routingControl =
      (L as any).Routing.control({

        waypoints: [

          L.latLng(
           liveLocation?.lat || userCoordinates.lat,
           liveLocation?.lon || userCoordinates.lon
          ),

          L.latLng(
            selectedVenue.lat,
            selectedVenue.lon
          )

        ],

        routeWhileDragging: false,

        addWaypoints: false,

        draggableWaypoints: false,

        fitSelectedRoutes: true,

        show: true

      }).addTo(map);

    return () => {
      map.removeControl(routingControl);
    };

  }, [selectedVenue, liveLocation]);

  return null;
}
function LiveLocationTracker({
  setLiveLocation
}: any) {

  useEffect(() => {

    const watchId =
      navigator.geolocation.watchPosition(

        (position) => {

          console.log(
  "LIVE GPS:",
  position.coords.latitude,
  position.coords.longitude
);
console.log(
  "LIVE LOCATION STATE UPDATED"
);
setLiveLocation({
  lat: position.coords.latitude,
  lon: position.coords.longitude
});

        },

        (error) => {
          console.error(error);
        },

        {
          enableHighAccuracy: true,
          maximumAge: 0,
          timeout: 10000
        }

      );

    return () => {

      navigator.geolocation.clearWatch(
        watchId
      );

    };

  }, []);

  return null;

}
function FollowUser({
  liveLocation
}: any) {

  const map = useMap();

  useEffect(() => {
    console.log(
  "FOLLOW USER:",
  liveLocation
);
    if (!liveLocation) return;

    map.setView(
      [
        liveLocation.lat,
        liveLocation.lon
      ],
      map.getZoom()
    );

  }, [liveLocation]);

  return null;

}
export default function VenueMap({
  venues,
  userCoordinates
}: any) {
  const [liveLocation, setLiveLocation] =
  React.useState<any>(null);
const [smoothLocation, setSmoothLocation] =
  React.useState<any>(null);
const [navigationActive, setNavigationActive] =
  React.useState(false);
const [selectedVenue, setSelectedVenue] = React.useState<any>(null);
const [showDirections, setShowDirections] =
  React.useState(false);
  const [directionsPanelVisible, setDirectionsPanelVisible] =
  React.useState(true);
  console.log("MAP VENUES:", venues);
  let center: [number, number] = [13.0827, 80.2707];

  if (liveLocation) {

  center = [
    liveLocation.lat,
    liveLocation.lon
  ];

}
else if (
  userCoordinates &&
  userCoordinates.lat &&
  userCoordinates.lon
) {

  center = [
    userCoordinates.lat,
    userCoordinates.lon
  ];

}
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
  console.log("VENUE COUNT:", venues.length);

console.log(
  "FIRST VENUE:",
  venues[0]
);
useEffect(() => {

  if (!liveLocation) return;

  if (!smoothLocation) {

    setSmoothLocation(liveLocation);
    return;

  }

  const startLat = smoothLocation.lat;
  const startLon = smoothLocation.lon;

  const endLat = liveLocation.lat;
  const endLon = liveLocation.lon;

  let step = 0;

  const animation = setInterval(() => {

    step++;

    const progress = step / 20;

    if (progress >= 1) {

      setSmoothLocation(liveLocation);

      clearInterval(animation);

      return;

    }

    setSmoothLocation({
      lat:
        startLat +
        (endLat - startLat) * progress,

      lon:
        startLon +
        (endLon - startLon) * progress
    });

  }, 50);

  return () => clearInterval(animation);

}, [liveLocation]);
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
      {navigationActive && (
      <LiveLocationTracker
      setLiveLocation={setLiveLocation}
      />
    )}
    {liveLocation && (
    <FollowUser
    liveLocation={liveLocation}
    />
  )}
    <FitBounds venues={venues} />
    
    <ChangeMapView center={center} />
    <MyLocationButton />
    {showDirections && (

  <button
    onClick={() => {

      const panel =
        document.querySelector(
          ".leaflet-routing-container"
        ) as HTMLElement;

      if(panel){

        const newState =
          !directionsPanelVisible;

        setDirectionsPanelVisible(
          newState
        );

        panel.style.display =
          newState
            ? "block"
            : "none";

      }

    }}
    style={{
      position: "absolute",
      top: "95px",
      left: "10px",
      zIndex: 1001,
      background: "white",
      padding: "10px 14px",
      borderRadius: "10px",
      border: "1px solid #ddd",
      cursor: "pointer",
      fontWeight: "bold",
      boxShadow:
        "0 2px 8px rgba(0,0,0,0.15)"
    }}
  >
    {directionsPanelVisible
      ? "📋 Hide Directions"
      : "📋 Show Directions"}
  </button>

)}
    {showDirections && (
      <RoutingMachine
      userCoordinates={userCoordinates}
      liveLocation={liveLocation}
      selectedVenue={selectedVenue}
  />
)}
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      
      {(liveLocation || userCoordinates) && (
  <>
    <Circle
      center={[
        (smoothLocation || liveLocation || userCoordinates).lat,
        (smoothLocation || liveLocation || userCoordinates).lon
      ]}
      radius={50}
      pathOptions={{
        color: "#2563eb",
        fillColor: "#60a5fa",
        fillOpacity: 0.25
      }}
    />
        <Marker
          position={[
            (smoothLocation || liveLocation || userCoordinates).lat,
            (smoothLocation || liveLocation || userCoordinates).lon
          ]}
          icon={
  navigationActive
    ? navigationIcon
    : userIcon
}
        >
          <Popup>
  <div>
    <b>You are here</b>

    <br />

    Lat:
    {(liveLocation || userCoordinates).lat}

    <br />

    Lon:
    {(liveLocation || userCoordinates).lon}
  </div>
</Popup>
        </Marker>
        </>
      )}

      {venues.map((venue: any) => {

        if (!venue.lat || !venue.lon) {
          return null;
        }
        
        return (
          <Marker
            key={venue.id}
            eventHandlers={{
              click: () => {
                setSelectedVenue(venue);
                setShowDirections(true);
                setTimeout(() => {

      const panel =
  document.querySelector(
    ".leaflet-routing-container"
  ) as HTMLElement;

if(panel){

  if(panel.style.visibility === "hidden"){

    panel.style.visibility = "visible";

  } else {

    panel.style.visibility = "hidden";

  }

}

    }, 300);
              }
            }}
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
  {venue.city}
</p>

<button
  onClick={() => {

    setNavigationActive(true);

  }}
  className="mt-2 px-3 py-2 bg-green-600 text-white rounded"
>
  Start Navigation
</button>

</div>
</Popup>
</Marker>
);

})}

</MapContainer>
);
}