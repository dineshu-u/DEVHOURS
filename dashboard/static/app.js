async function simulateReroute() {
    const routeDisplay = document.getElementById('route-display');
    routeDisplay.innerText = "Recalculating...";
    
    // In a real app, this would fetch from /api/v1/route
    setTimeout(() => {
        routeDisplay.innerText = "A -> D -> C (Optimized for Emission)";
    }, 1000);
}

async function triggerEmergency() {
    const status = document.getElementById('emergency-status');
    status.innerHTML = '<span class="dot" style="background: #ef4444; box-shadow: 0 0 10px #ef4444;"></span> Active';
    
    // In a real app, this would POST to /api/v1/emergency
    alert("Emergency Vehicle Detected. Clearing Path & Activating Green Wave.");
}

// Mock update loop
setInterval(() => {
    const delayVal = document.getElementById('delay-val');
    const riskProgress = document.getElementById('risk-progress');
    
    const randomDelay = (Math.random() * 20 + 5).toFixed(1);
    delayVal.innerText = `${randomDelay} mins`;
    
    const randomRisk = Math.random() * 100;
    riskProgress.style.width = `${randomRisk}%`;
}, 3000);
