// Initialize the map (Wait to set the view until later!)
let map = L.map('map');

// Add the base map tiles
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

// The async function to fetch data and plot markers
async function loadStations() {
    try {
        // TODO: 1. Fetch the data from the FastAPI backend
        // Hint: let response = await fetch("http://127.0.0.1:8000/api/stations");
        // Hint: let stations = await response.json();
        let response = await fetch("http://127.0.0.1:8000/api/stations");
        let stations = await response.json();
        // TODO: 2. Create an empty Leaflet bounds object
        // Hint: let bounds = L.latLngBounds();
        let bounds = L.latLngBounds();
        // TODO: 3. Loop through the 'stations' array
        // Hint: for (let station of stations) { ... }
        for (let station of stations) {

            // --- INSIDE THE LOOP ---
            // TODO: 4. Create a marker for each station and add it to the map
            // Hint: L.marker([station.lat, station.lon]).addTo(map).bindPopup(station.station_id);
            L.marker([station.lat, station.lon])
                .addTo(map)
                .bindPopup(station.station_id);
            // TODO: 5. Extend the bounds box to include this new marker's coordinates
            // Hint: bounds.extend([station.lat, station.lon]);
            bounds.extend([station.lat, station.lon]);
            // --- END OF LOOP ---

        }


        // TODO: 6. Tell the map to fit exactly to our calculated bounds
        // Hint: map.fitBounds(bounds);
        map.fitBounds(bounds);

    } catch (error) {
        console.error("Failed to load stations:", error);
    }
}

// Call the function to actually run it!
loadStations();