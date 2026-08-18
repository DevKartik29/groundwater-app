# Manual End-to-End Test Checklist

This checklist verifies the critical functionality of the Groundwater App from an end-user perspective. It should be run manually before deployment.

## 1. The Map Page (`index.html`)

- [ ] **Load rendering:** Open `index.html`. Does the map load centered on India with exactly 30 circle markers?
- [ ] **Status coloring:** Do the markers display distinct colors based on their pre-computed status (e.g., red for Declining, blue for Recovering, grey/green for Stable)?
- [ ] **Legend visibility:** Is the status legend visible and accurate to the colors on the map?
- [ ] **Popups:** Click a marker (e.g., Ludhiana). Does a popup appear showing the station name, ID, and its specific trend value?
- [ ] **Navigation:** Click the "View Details" link inside a popup. Does it correctly navigate to `station.html?id=STATION_ID`?

## 2. The Station Page (`station.html`)

- [ ] **Data Fetching:** Navigate to `station.html?id=RJ-001`. Do the dashboard boxes display the correct numbers from the API (Trend, Recharge, Anomaly Count)?
- [ ] **Format Consistency:** Do all depth numbers utilize the `formatDepth()` utility (e.g., formatted to 2 decimal places with "m bgl" where appropriate)?
- [ ] **Chart Rendering:** Does the historical hydrograph render 3 years of data points?
- [ ] **Y-Axis Inversion:** Look at the chart's Y-axis. Is it correctly reversed? (Higher numbers = deeper water = lower on the chart).
- [ ] **Visuals/Faults:** Are anomalous points (spikes/stuck readings) visually distinct (e.g., colored red) from normal readings?

## 3. Resilience and Edge Cases

- [ ] **Invalid Station ID:** Manually type `station.html?id=FAKE-99` in the URL bar. Does the UI display a graceful "Station not found" error instead of a blank page or unhandled exception?
- [ ] **Missing ID Parameter:** Manually type `station.html` (with no `?id=`) in the URL bar. Does it display an expected missing ID prompt/message?
- [ ] **Backend Down:** Stop the Uvicorn server in your terminal. Refresh the frontend. Does it show a connection error or loading state failure rather than silently breaking?

## 4. API Integrity Verification (Post-Generation)

- [ ] **Data Completeness:** Hit `/api/stations`. Are exactly 30 stations returned?
- [ ] **Nulls and Negatives:** Verify no `null` values exist for critical fields (`water_level_m_bgl`, `ts`) and no depth values are negative (`< 0`).
- [ ] **Recharge Sanity:** Review the calculated recharge. While the synthetic sine-wave generator produces out-of-range values (>25% of rainfall) for sandy regions, verify the math executes correctly without throwing errors.
- [ ] **Endpoint Contracts:** Hit `/api/stations/search?state=Punjab`. Does it correctly filter and return only Punjab stations?
