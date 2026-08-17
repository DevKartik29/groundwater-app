// Helper: pick a dot colour based on the station's precomputed status
function getStatusColor(status) {
    // TODO: A. Fill in the switch statement
    switch (status) {
        case "Declining": return "#ef4444";  // red
        case "Stable": return "#f59e0b";  // amber
        case "Recovering": return "#22c55e";  // green
        default: return "#9ca3af";  // grey (null / unknown)
    }
}

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
        let response = await fetch("http://127.0.0.1:8000/api/stations");
        let stations = await response.json();
        // TODO: 2. Create an empty Leaflet bounds object
        let bounds = L.latLngBounds();
        // TODO: 3. Loop through the 'stations' array
        for (let station of stations) {

            // --- INSIDE THE LOOP ---
            // TODO: B. Pick the colour using our helper
            let color = getStatusColor(station.status);

            // TODO: C. Replace L.marker with L.circleMarker
            L.circleMarker([station.lat, station.lon], {
                radius: 8,
                fillColor: color,
                color: '#333',
                weight: 1,
                fillOpacity: 0.9
            }).addTo(map)
                .bindPopup(`<a href="station.html?id=${station.station_id}">View ${station.station_id}</a>`);

            // TODO: 5. Extend the bounds box to include this new marker's coordinates
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