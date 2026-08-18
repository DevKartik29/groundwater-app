// Helper function to format depth consistently across the frontend
function formatDepth(depth) {
    if (depth === null || depth === undefined) return "N/A";
    return Number(depth).toFixed(2);
}
