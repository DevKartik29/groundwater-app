// TODO: 1. Read the station ID from the URL (e.g. ?id=PB-001)
// Hint: let params = new URLSearchParams(window.location.search);
// let stationId = ...
let params = new URLSearchParams(window.location.search);
let stationId = params.get('id');

async function loadStationData() {
    if (!stationId) {
        document.getElementById('station-name').innerText = "Error: No station ID provided!";
        return;
    }

    try {
        // TODO: 2. Update the H1 tag to show the station ID
        // Hint: document.getElementById('station-name').innerText = "Station " + stationId;
        document.getElementById('station-name').innerText = "Station " + stationId;

        // TODO: 3. Fetch the timeseries data for this specific station
        // Hint: let response = await fetch(`http://127.0.0.1:8000/api/stations/${stationId}/timeseries?days=1095`);
        // let data = await response.json();
        let response = await fetch(
            `http://127.0.0.1:8000/api/stations/${stationId}/timeseries?days=1095`
        );

        let data = await response.json();
        // TODO: 4. Extract arrays for the X and Y axes
        // Hint: We need two separate arrays for Chart.js. One for the dates, one for the water levels.
        // let dates = data.map(row => row.ts.split('T')[0]); // Splits "2023-06-01T00:00:00" to just "2023-06-01"
        // let levels = data.map(row => row.water_level_m_bgl);
        let dates = data.map(row => row.ts.split('T')[0]);
        let levels = data.map(row => row.water_level_m_bgl);
        // TODO: 5. Draw the Chart.js line chart

        const ctx = document.getElementById('hydrograph').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates, // X-axis
                datasets: [{
                    label: 'Water Level (m bgl)',
                    data: levels, // Y-axis
                    borderColor: 'blue',
                    borderWidth: 2,
                    pointRadius: 0 // Hide dots, just show the line
                }]
            },
            options: {
                scales: {
                    // TODO: 6. VERY IMPORTANT - Reverse the Y-axis!
                    // Hint: y: { reverse: true }
                    y: { reverse: true }
                }
            }
        });


    } catch (error) {
        console.error("Failed to load station data:", error);
        document.getElementById('station-name').innerText = "Error loading data!";
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
