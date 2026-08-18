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

        let statusDiv = document.getElementById('chart-status');

        // TODO: A. Check if the server returned an error (e.g. 404 station not found)
        if (!response.ok) {
            statusDiv.innerText = "Error: Station not found.";
            statusDiv.classList.add('error-state');
            return;
        }

        let data = await response.json();

        // TODO: B. Check if the data array is empty (station exists but has no readings)
        if (data.length === 0) {
            statusDiv.innerText = "No readings available for this station.";
            statusDiv.classList.add('error-state');
            return;
        }

        // TODO: C. If we got here, data is good — hide the status message
        statusDiv.style.display = "none";

        let dates = data.map(row => row.ts.split('T')[0]);
        let levels = data.map(row => row.water_level_m_bgl);

        let pointColors = levels.map((val, i, arr) => {
            let isSpike = false;
            if (i > 0 && Math.abs(val - arr[i-1]) > 5) isSpike = true;
            if (i < arr.length - 1 && Math.abs(val - arr[i+1]) > 5) isSpike = true;
            return (data[i].flagged || isSpike) ? '#ef4444' : '#3b82f6';
        });

        let pointRadii = pointColors.map(c => c === '#ef4444' ? 6 : 0);
        let pointStyles = pointColors.map(c => c === '#ef4444' ? 'crossRot' : 'circle');
        let pointBorderWidths = pointColors.map(c => c === '#ef4444' ? 2 : 1);

        const ctx = document.getElementById('hydrograph').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Water Level (m bgl)',
                    data: levels,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    pointBackgroundColor: pointColors,
                    pointBorderColor: pointColors,
                    pointRadius: pointRadii,
                    pointStyle: pointStyles,
                    pointBorderWidth: pointBorderWidths
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { 
                        reverse: true,
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#94a3b8' },
                        title: { display: true, text: 'Depth (m bgl)', color: '#94a3b8' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#94a3b8' }
                    }
                },
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
                                return formatDepth(context.parsed.y);
                            }
                        }
                    }
                }
            }
        });

    } catch (error) {
        // TODO: D. Show a user-friendly error when the server is completely unreachable
        let statusDiv = document.getElementById('chart-status');
        statusDiv.innerText = "Could not connect to the server. Is it running?";
        statusDiv.classList.add('error-state');
        statusDiv.style.display = "block";
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

        // 8. Update the Trend box
        let slopeStr = data.trend.slope_m_per_year;
        let trendIcon = "➡";
        let trendColorClass = "text-amber";
        let trendSub = "Water table is stable";
        
        if (data.trend.direction === "falling") {
            trendIcon = "⬇"; // Arrow pointing down because depth is increasing (table falling)
            trendColorClass = "text-red";
            trendSub = "Water depth is increasing";
            slopeStr = "+" + slopeStr; 
        } else if (data.trend.direction === "recovering") {
            trendIcon = "⬆"; // Arrow pointing up because depth is decreasing (table rising)
            trendColorClass = "text-green";
            trendSub = "Water depth is decreasing";
        }

        document.getElementById('trend-val').innerText = slopeStr;
        document.getElementById('trend-val').className = `metric-primary ${trendColorClass}`;
        document.getElementById('trend-icon').innerText = trendIcon;
        document.getElementById('trend-icon').className = `metric-arrow ${trendColorClass}`;
        document.getElementById('trend-sub').innerText = trendSub;

        // 9. Update the Recharge box
        document.getElementById('recharge-val').innerText = data.recharge.recharge_mm;

        // 10. Update the Anomalies box
        document.getElementById('anomalies-val').innerText = data.anomalies.total;
        if (data.anomalies.total > 0) {
            document.getElementById('anomalies-val').className = "metric-primary text-red";
            document.getElementById('anomaly-icon').innerText = "⚠️";
            document.getElementById('anomaly-sub').innerText = "Suspicious sensor readings flagged";
        }

        // 11. Update the Overall Status box (and the new status card)
        let statusVal = document.getElementById('status-val');
        let statusCardVal = document.getElementById('status-card-val');
        
        statusVal.innerText = data.overall_status;
        statusCardVal.innerText = data.overall_status;
        
        let statusColorClass = "bg-gray";
        let statusTextClass = "text-unknown";
        if (data.overall_status === "Declining") { statusColorClass = "bg-red"; statusTextClass = "text-red"; }
        if (data.overall_status === "Recovering") { statusColorClass = "bg-green"; statusTextClass = "text-green"; }
        if (data.overall_status === "Stable") { statusColorClass = "bg-amber"; statusTextClass = "text-amber"; }
        
        statusVal.className = `status-badge ${statusColorClass}`;
        statusCardVal.className = `metric-primary ${statusTextClass}`;

        if (data.overall_status === "Declining") {
            document.getElementById('status-card-sub').innerText = "Attention needed";
        } else if (data.overall_status === "Recovering") {
            document.getElementById('status-card-sub').innerText = "Improving conditions";
        } else {
            document.getElementById('status-card-sub').innerText = "Within normal variance";
        }

        // 12. Update Interpretation Text
        let interpText = ``;
        if (data.overall_status === "Declining") {
            interpText += `<strong>⚠ Groundwater stress detected</strong><br><br>`;
            interpText += `This station shows a declining groundwater trend of ${slopeStr}. Water depth is increasing over time.<br><br>`;
        } else if (data.overall_status === "Recovering") {
            interpText += `<strong>✓ Groundwater recovery detected</strong><br><br>`;
            interpText += `This station shows a recovering groundwater trend of ${slopeStr}. Water depth is decreasing over time.<br><br>`;
        } else {
            interpText += `<strong>Groundwater levels are relatively stable</strong><br><br>`;
            interpText += `This station shows a stable trend of ${slopeStr}.<br><br>`;
        }

        if (data.anomalies.total > 0) {
            interpText += `${data.anomalies.total} anomalous readings have been flagged in the historical dataset. Review the hydrograph for sudden spikes.<br><br>`;
        }

        interpText += `──────────────────────────────────────────────────────────<br>`;
        interpText += `STATUS: <strong>${data.overall_status.toUpperCase()}</strong>`;

        document.getElementById('interpretation-text').innerHTML = interpText;

        // Fetch Metadata for Header and Footer
        let metaResponse = await fetch("http://127.0.0.1:8000/api/stations");
        let allStations = await metaResponse.json();
        let stationMeta = allStations.find(s => s.station_id === stationId);
        
        if (stationMeta) {
            document.getElementById('station-subtitle').innerHTML = `${stationMeta.state} &bull; ${stationMeta.station_id}`;
            document.getElementById('meta-id').innerText = stationMeta.station_id;
            document.getElementById('meta-state').innerText = stationMeta.state;
            document.getElementById('meta-district').innerText = stationMeta.district;
            document.getElementById('meta-formation').innerText = stationMeta.formation;
            document.getElementById('meta-sy').innerText = stationMeta.specific_yield;
            
            let d = new Date(stationMeta.last_refreshed);
            document.getElementById('meta-refreshed').innerText = d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });

            // Initialize Background Map
            let map = L.map('map', {
                zoomControl: false,
                scrollWheelZoom: false,
                dragging: false,
                doubleClickZoom: false,
                touchZoom: false
            }).setView([stationMeta.lat, stationMeta.lon], 12);

            L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                maxZoom: 19,
                attribution: '&copy; CARTO'
            }).addTo(map);

            // Add a subtle marker for context
            L.circleMarker([stationMeta.lat, stationMeta.lon], {
                radius: 12,
                fillColor: '#3b82f6',
                color: '#ffffff',
                weight: 2,
                fillOpacity: 0.5
            }).addTo(map);
        }

    } catch (error) {
        console.error("Failed to load analytics:", error);
    }
}

// TODO: 12. Call the loadAnalyticsData function to actually run it!
loadAnalyticsData();
