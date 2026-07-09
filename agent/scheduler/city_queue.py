from queue import Queue

city_queue = Queue()

DEFAULT_CITIES = [
    ("London", 51.5074, -0.1278),

    ("Paris", 48.8566, 2.3522),

    ("New York", 40.7128, -74.0060),

    ("Dubai", 25.2048, 55.2708),

    ("Bangalore", 12.9716, 77.5946),

    ("Tokyo", 35.6762, 139.6503),

    ("Singapore", 1.3521, 103.8198),
]

for city in DEFAULT_CITIES:

    city_queue.put(city)