// TODO: 1. Read the station ID from the URL (e.g. ?id=PB-001)
// Hint: let params = new URLSearchParams(window.location.search);
// let stationId = ...
let params = new URLSearchParams(window.location.search);
let stationId = params.get('id');

async function loadStationData() {
    if (!stationId) {
        document.getElementById('station-name').innerText = "Error: No station ID provided!";
        document.getElementById('chart-status').innerText = "Cannot load chart without a station ID.";
        return;
    }

    try {
        document.getElementById('station-name').innerText = "Station " + stationId;

        let response = await fetch(
            `http://127.0.0.1:8000/api/stations/${stationId}/timeseries?days=1095`
        );

        // TODO: A. Check if the server returned an error (e.g. 404 station not found)
        if (!response.ok) {
            document.getElementById('chart-status').innerText = "Error: Station not found.";
            return;
        }

        let data = await response.json();

        // TODO: B. Check if the data array is empty (station exists but has no readings)
        if (data.length === 0) {
            document.getElementById('chart-status').innerText = "No readings available for this station.";
            return;
        }

        // TODO: C. If we got here, data is good — hide the status message
        document.getElementById('chart-status').innerText = "";

        let dates = data.map(row => row.ts.split('T')[0]);
        let levels = data.map(row => row.water_level_m_bgl);

        const ctx = document.getElementById('hydrograph').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Water Level (m bgl)',
                    data: levels,
                    borderColor: 'blue',
                    borderWidth: 2,
                    pointRadius: 0
                }]
            },
            options: {
                scales: {
                    y: { reverse: true }
                }
            }
        });

    } catch (error) {
        // TODO: D. Show a user-friendly error when the server is completely unreachable
        document.getElementById('chart-status').innerText = "Could not connect to the server. Is it running?";
        console.error("Failed to load station data:", error);
    }
}

// Call the function to actually run it!
loadStationData();

async function loadAnalyticsData() {
    if (!stationId) return;

    try {
        // TODO: 7. Fetch the analytics data for this station
        let response = await fetch(`http://127.0.0.1:8000/api/stations/${stationId}/analytics`);
        let data = await response.json();

        // TODO: 8. Update the Trend box using DOM selection
        document.getElementById('trend-val').innerText = data.trend.message;

        // TODO: 9. Update the Recharge box
        document.getElementById('recharge-val').innerText = data.recharge.recharge_mm + " mm";

        // TODO: 10. Update the Anomalies box
        document.getElementById('anomalies-val').innerText = data.anomalies.total + " readings flagged";

        // TODO: 11. Update the Overall Status box
        document.getElementById('status-val').innerText = data.overall_status;

    } catch (error) {
        console.error("Failed to load analytics:", error);
    }
}

// TODO: 12. Call the loadAnalyticsData function to actually run it!
loadAnalyticsData();
