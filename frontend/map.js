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

// Add the base map tiles (CartoDB Dark Matter)
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
}).addTo(map);

// The async function to fetch data and plot markers
async function loadStations() {
    try {
        // TODO: 1. Fetch the data from the FastAPI backend
        let response = await fetch("/api/stations");
        let stations = await response.json();

        // Update Dashboard Summary, Chart, and Interpretation
        if (document.getElementById('donut-declining')) {
            let counts = { "Declining": 0, "Stable": 0, "Recovering": 0, "Unknown": 0 };
            let maxDecline = null;
            let maxRecovery = null;
            let maxAnomalies = null;

            for (let s of stations) {
                if (s.status === "Declining") counts["Declining"]++;
                else if (s.status === "Recovering") counts["Recovering"]++;
                else if (s.status === "Stable") counts["Stable"]++;
                else counts["Unknown"]++;

                // Track extremes for highlights
                if (s.trend_m_per_year !== null) {
                    if (!maxDecline || s.trend_m_per_year > maxDecline.trend_m_per_year) maxDecline = s;
                    if (!maxRecovery || s.trend_m_per_year < maxRecovery.trend_m_per_year) maxRecovery = s;
                }
                if (!maxAnomalies || s.anomaly_count > maxAnomalies.anomaly_count) maxAnomalies = s;
            }

            document.getElementById('donut-declining').innerText = counts["Declining"];
            document.getElementById('donut-stable').innerText = counts["Stable"];
            document.getElementById('donut-recovering').innerText = counts["Recovering"];

            // Interpretation Text
            let interpretation = `Most monitored stations are currently classified as Stable or Awaiting Data.`;
            let networkStatus = "ANALYZING NETWORK...";
            if (counts["Declining"] > counts["Recovering"] && counts["Declining"] > counts["Stable"]) {
                interpretation = `⚠ <strong class="text-red">High Network Stress</strong><br><br>Most stations show a positive depth trend, indicating increasing depth to groundwater.`;
                networkStatus = `<span class="text-red">⚠ NETWORK STRESS DETECTED</span>`;
            } else if (counts["Recovering"] > counts["Declining"] && counts["Recovering"] > counts["Stable"]) {
                interpretation = `✓ <strong class="text-green">Network Recovering</strong><br><br>Most stations show a negative groundwater-depth trend, indicating decreasing depth to groundwater.`;
                networkStatus = `<span class="text-green">✓ NETWORK RECOVERING</span>`;
            } else {
                networkStatus = `<span class="text-amber">NETWORK STABLE</span>`;
            }
            document.getElementById('interpretation-text').innerHTML = interpretation;
            if (document.getElementById('header-status')) {
                document.getElementById('header-status').innerHTML = `STATUS: ${networkStatus}`;
            }

            // Network Highlights
            if (maxDecline && maxRecovery && maxAnomalies) {
                document.getElementById('highlights-container').innerHTML = `
                    <a href="station.html?id=${maxDecline.station_id}" class="highlight-link">
                        <div style="font-size: 0.75rem; color: var(--text-tertiary); font-weight: 700; margin-bottom: 0.25rem;">⚠ MOST SEVERE DECLINE</div>
                        <strong class="text-bright" style="font-size: 1.1rem;">${maxDecline.station_id}</strong>
                        <span class="text-red" style="font-weight: 600; margin-left: 0.5rem;">+${maxDecline.trend_m_per_year} m/yr</span>
                    </a>
                    <a href="station.html?id=${maxRecovery.station_id}" class="highlight-link">
                        <div style="font-size: 0.75rem; color: var(--text-tertiary); font-weight: 700; margin-bottom: 0.25rem;">✓ STRONGEST RECOVERY</div>
                        <strong class="text-bright" style="font-size: 1.1rem;">${maxRecovery.station_id}</strong>
                        <span class="text-green" style="font-weight: 600; margin-left: 0.5rem;">${maxRecovery.trend_m_per_year} m/yr</span>
                    </a>
                    <a href="station.html?id=${maxAnomalies.station_id}" class="highlight-link">
                        <div style="font-size: 0.75rem; color: var(--text-tertiary); font-weight: 700; margin-bottom: 0.25rem;">⚠ MOST ANOMALIES</div>
                        <strong class="text-bright" style="font-size: 1.1rem;">${maxAnomalies.station_id}</strong>
                        <span class="text-red" style="font-weight: 600; margin-left: 0.5rem;">${maxAnomalies.anomaly_count} flagged</span>
                    </a>
                `;
            }

            if (document.getElementById('status-donut')) {
                const ctx = document.getElementById('status-donut').getContext('2d');
                new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Declining', 'Stable', 'Recovering', 'Awaiting Data'],
                        datasets: [{
                            data: [counts["Declining"], counts["Stable"], counts["Recovering"], counts["Unknown"]],
                            backgroundColor: ['#ef4444', '#f59e0b', '#10b981', '#64748b'],
                            borderColor: '#0f172a',
                            borderWidth: 2,
                            hoverOffset: 4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        cutout: '75%',
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                backgroundColor: 'rgba(15, 23, 42, 0.9)',
                                titleColor: '#f8fafc',
                                bodyColor: '#f8fafc',
                                borderColor: 'rgba(255,255,255,0.1)',
                                borderWidth: 1,
                                callbacks: {
                                    label: function(context) {
                                        let percentage = Math.round((context.parsed / stations.length) * 100);
                                        return ` ${context.label}: ${context.parsed} (${percentage}%)`;
                                    }
                                }
                            }
                        }
                    }
                });
            }
        }

        // TODO: 2. Create an empty Leaflet bounds object
        let bounds = L.latLngBounds();

        // TODO: 3. Loop through the 'stations' array
        for (let station of stations) {
            
            // TODO: B. Get the color based on the station's status
            let color = getStatusColor(station.status);
            
            let statusIcon = "⚫";
            if (station.status === "Declining") statusIcon = "🔴";
            else if (station.status === "Recovering") statusIcon = "🟢";
            else if (station.status === "Stable") statusIcon = "🟠";
            
            let trendFormatted = station.trend_m_per_year !== null ? (station.trend_m_per_year > 0 ? "+" + station.trend_m_per_year : station.trend_m_per_year) + " m/year" : "N/A";
            let trendSubtext = "";
            if (station.trend_m_per_year > 0) trendSubtext = "Groundwater depth increasing";
            else if (station.trend_m_per_year < 0) trendSubtext = "Groundwater depth decreasing";

            // TODO: C. Replace L.marker with L.circleMarker
            let marker = L.circleMarker([station.lat, station.lon], {
                radius: 8,
                fillColor: color,
                color: '#0f172a',
                weight: 2,
                fillOpacity: 1
            }).addTo(map)
                .bindPopup(`
                    <div style="padding: 16px; font-family: 'Inter', sans-serif;">
                        <div style="text-transform: uppercase; font-size: 1.1rem; font-weight: 800; letter-spacing: -0.02em; color: var(--text-primary);">${station.name}</div>
                        <div style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 12px; font-weight: 500;">${station.state} &bull; ${station.station_id}</div>
                        
                        <div style="font-size: 0.95rem; font-weight: 700; color: var(--color-${(station.status || 'unknown').toLowerCase()}); margin-bottom: 4px; text-transform: uppercase;">
                            ${statusIcon} ${station.status || 'Unknown'}
                        </div>
                        <div style="font-size: 0.95rem; font-weight: 700; color: var(--text-primary);">${trendFormatted}</div>
                        
                        ${trendSubtext ? `<div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 4px; margin-bottom: 16px;">${trendSubtext}</div>` : '<div style="margin-bottom: 16px;"></div>'}
                        
                        <a href="station.html?id=${station.station_id}" style="display: block; width: 100%; text-align: center; background: rgba(255,255,255,0.1); color: var(--text-primary); text-decoration: none; padding: 8px; border-radius: 6px; font-weight: 600; font-size: 0.9rem; border: 1px solid rgba(255,255,255,0.2); transition: background 0.1s;">View Station HUD &rarr;</a>
                    </div>
                `, { className: 'custom-popup' });
            
            // Hover interaction
            marker.on('mouseover', function(e) {
                this.setRadius(10);
                this.setStyle({ weight: 2 });
            });
            marker.on('mouseout', function(e) {
                this.setRadius(8);
                this.setStyle({ weight: 1.5 });
            });

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