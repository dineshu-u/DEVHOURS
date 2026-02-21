/* ============================================================
   Flow Guardian X — UIC Live Intelligence Module
   All API calls target http://localhost:8080/api/v1
   Refresh cycle: 1500ms (< 2s requirement)
   ============================================================ */

const API = 'http://localhost:8080/api/v1';
const REFRESH_MS = 1500;

// ── Sector map (display label → API edge)
const SECTORS = [
    { label: 'A → B', id: 'A-B' },
    { label: 'B → C', id: 'B-C' },
    { label: 'A → D', id: 'A-D' },
    { label: 'D → C', id: 'D-C' },
    { label: 'B → D', id: 'B-D' },
    { label: 'D → A', id: 'D-A' }, // overflow placeholder
];

// ── Init Chart.js Radar
const radarCtx = document.getElementById('radarChart').getContext('2d');
const radarChart = new Chart(radarCtx, {
    type: 'radar',
    data: {
        labels: ['α Delay', 'β Emission', 'γ Risk', 'Throughput', 'Resilience', 'Equity'],
        datasets: [{
            label: 'System Balance',
            data: [0.6, 0.2, 0.2, 0.7, 0.8, 0.55],
            backgroundColor: 'rgba(56, 189, 248, 0.12)',
            borderColor: '#38bdf8',
            borderWidth: 2,
            pointBackgroundColor: '#38bdf8',
            pointRadius: 4,
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
            r: {
                min: 0, max: 1,
                ticks: { display: false, stepSize: 0.25 },
                grid: { color: 'rgba(255,255,255,0.06)' },
                angleLines: { color: 'rgba(255,255,255,0.06)' },
                pointLabels: {
                    color: '#94a3b8',
                    font: { size: 10, family: 'Outfit' }
                }
            }
        }
    }
});

// ── Build heatmap cells on load
function buildHeatmap() {
    const grid = document.getElementById('heatmapGrid');
    grid.innerHTML = '';
    SECTORS.forEach(s => {
        const cell = document.createElement('div');
        cell.className = 'hm-cell stable';
        cell.id = `hm-${s.id}`;
        cell.innerHTML = `<span class="cell-label">${s.label}</span>Stable`;
        grid.appendChild(cell);
    });
}

// ── Map API regime string → CSS class + display text
function regimeClass(r) {
    if (!r) return { cls: 'stable', label: 'Stable' };
    const lower = r.toLowerCase();
    if (lower.includes('unstable') || lower.includes('gridlock') || lower.includes('collapse'))
        return { cls: 'unstable', label: r };
    if (lower.includes('meta') || lower.includes('high'))
        return { cls: 'meta', label: r };
    return { cls: 'stable', label: r };
}

// ── Ticker updates
function updateTicker(heatmap) {
    const mapping = { 'A-B': 'tick-ab', 'B-C': 'tick-bc', 'A-D': 'tick-ad', 'D-C': 'tick-dc' };
    heatmap.forEach(item => {
        const sector = item.sector ? item.sector.replace('→', '-').replace(' ', '').replace(' ', '') : '';
        const tickId = mapping[sector] || null;
        if (tickId) {
            const el = document.getElementById(tickId);
            if (el) el.textContent = item.regime || 'Stable';
        }
    });
    document.getElementById('tick-time').textContent = new Date().toLocaleTimeString();
}

// ── Main UIC refresh loop
let lastPollStart = Date.now();

async function refreshUIC() {
    lastPollStart = Date.now();
    try {
        const res = await fetch(`${API}/uic-stream`, { cache: 'no-store' });
        const data = await res.json();

        const lagMs = Date.now() - lastPollStart;
        document.getElementById('lag-ms').textContent = `${lagMs}ms`;

        // Update Radar
        const { alpha_delay: a, beta_emission: b, gamma_risk: g } = data.radar;
        radarChart.data.datasets[0].data = [
            a, b, g,
            parseFloat((1 - b).toFixed(2)),
            parseFloat((1 - g).toFixed(2)),
            parseFloat(((a + b + g) / 3).toFixed(2))
        ];
        radarChart.update('none');
        document.getElementById('alpha-val').textContent = a.toFixed(2);
        document.getElementById('beta-val').textContent = b.toFixed(2);
        document.getElementById('gamma-val').textContent = g.toFixed(2);

        // Update Heatmap
        data.heatmap.forEach(item => {
            const sectorKey = item.sector;
            const cell = document.getElementById(`hm-${sectorKey}`);
            if (cell) {
                const { cls, label } = regimeClass(item.regime);
                cell.className = `hm-cell ${cls}`;
                cell.innerHTML = `<span class="cell-label">${sectorKey.replace('-', ' → ')}</span>${label}`;
            }
        });

        updateTicker(data.heatmap);

    } catch (e) {
        document.getElementById('lag-ms').textContent = 'ERR';
        document.getElementById('sys-status').textContent = 'API OFFLINE';
    }
}

// ── Prediction
async function runPrediction() {
    const payload = {
        vehicle_count: parseInt(document.getElementById('p-vehicles').value),
        avg_speed_kmph: parseFloat(document.getElementById('p-speed').value),
        road_capacity: parseInt(document.getElementById('p-capacity').value),
        rainfall_intensity: parseFloat(document.getElementById('p-rain').value),
        accident_flag: document.getElementById('p-accident').checked,
        violation_vehicle_count: 0
    };

    const btn = document.querySelector('.btn-predict');
    btn.textContent = '⏳ Predicting...';

    try {
        const res = await fetch(`${API}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const d = await res.json();

        document.getElementById('res-delay').textContent = `${d.predicted_delay_minutes} mins`;
        document.getElementById('res-conf').textContent = `${d.confidence_percentage}%`;
        document.getElementById('res-regime').textContent = d.congestion_regime;
        document.getElementById('res-risk').textContent = d.bottleneck_risk_score;
        document.getElementById('res-severity').textContent = d.severity_level;
        document.getElementById('res-emit').textContent = `${d.emission_load_g_per_km} g/km`;

        // Color code severity
        const sev = document.getElementById('res-severity');
        sev.style.color = d.severity_level === 'HIGH' ? 'var(--red)' :
            d.severity_level === 'MEDIUM' ? 'var(--yellow)' : 'var(--green)';
    } catch (e) {
        document.getElementById('res-delay').textContent = 'API Error';
    } finally {
        btn.textContent = '▶ Run Prediction';
    }
}

// ── Route Optimizer
async function runRoute() {
    const start = document.getElementById('r-start').value;
    const end = document.getElementById('r-end').value;
    const isEmerg = document.getElementById('r-emergency').checked;

    const btn = document.querySelector('.btn-route');
    btn.textContent = '⏳ Routing...';

    try {
        const res = await fetch(`${API}/route?start=${start}&end=${end}&is_emergency=${isEmerg}`);
        const d = await res.json();

        document.getElementById('res-route').textContent = d.recommended_route || `${start} → ${end}`;
        document.getElementById('res-cost').textContent = d.total_optimization_cost ?? '—';
        document.getElementById('res-priority').textContent = d.priority_mode || 'NORMAL';

        const prio = document.getElementById('res-priority');
        prio.style.color = d.priority_mode === 'EMERGENCY' ? 'var(--red)' : 'var(--green)';
    } catch (e) {
        document.getElementById('res-route').textContent = 'API Error';
    } finally {
        btn.textContent = '🔍 Find Best Route';
    }
}

// ── Chaos Trigger
async function triggerChaos() {
    const from = document.getElementById('c-from').value;
    const to = document.getElementById('c-to').value;

    const btn = document.getElementById('chaosBtn');
    btn.textContent = '💥 TRIGGERING...';
    btn.disabled = true;
    document.body.classList.add('shaking');
    setTimeout(() => document.body.classList.remove('shaking'), 700);

    try {
        const res = await fetch(`${API}/trigger-grid-collapse`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ intersection_node: from, target_edge: [from, to] })
        });
        const d = await res.json();

        const resultEl = document.getElementById('chaosResult');
        resultEl.style.display = 'flex';
        resultEl.style.flexDirection = 'column';

        document.getElementById('c-segment').textContent = d.affected_segment || `${from} → ${to}`;
        document.getElementById('c-ripple').textContent =
            d.impact_analysis?.predicted_ripple_delay !== undefined
                ? `${d.impact_analysis.predicted_ripple_delay} mins`
                : '∞ (Critical)';
        document.getElementById('c-status').textContent = d.impact_analysis?.sector_status || 'UNSTABLE';
        document.getElementById('c-action').textContent = d.action || 'GLOBAL_MINIMUM_REROUTE_EXECUTING';

        // Force heatmap to show that sector as unstable
        const cell = document.getElementById(`hm-${from}-${to}`);
        if (cell) {
            cell.className = 'hm-cell unstable';
            cell.innerHTML = `<span class="cell-label">${from} → ${to}</span>☠ COLLAPSED`;
        }

        // Override card border
        document.querySelector('.card-chaos').style.borderColor = 'rgba(248,113,113,0.6)';
        document.querySelector('.card-chaos').style.boxShadow = '0 0 40px rgba(248,113,113,0.15)';

    } catch (e) {
        if (e.message.includes('404')) {
            alert(`Edge ${from}→${to} not found in the network. Try A→B, B→C, A→D, D→C, or B→D.`);
        } else {
            alert('API Error: ' + e.message);
        }
    } finally {
        btn.textContent = '💥 TRIGGER GRID COLLAPSE';
        btn.disabled = false;
    }
}

// ── Restore Network
async function restoreGrid() {
    document.getElementById('chaosResult').style.display = 'none';
    document.querySelector('.card-chaos').style.borderColor = '';
    document.querySelector('.card-chaos').style.boxShadow = '';
    // Note: A proper restore would call a POST /restore-grid endpoint.
    // For now, refreshing UIC stream will reflect live server state.
    refreshUIC();
}

// ── Emergency
async function triggerEmergency() {
    const intId = document.getElementById('e-id').value || 'Int-01';
    const btn = document.querySelector('.btn-emergency');
    btn.textContent = '⏳ Activating...';

    try {
        const res = await fetch(`${API}/emergency?intersection_id=${encodeURIComponent(intId)}`, {
            method: 'POST'
        });
        const d = await res.json();

        document.getElementById('emg-status').textContent = d.status || 'ACTIVE';
        document.getElementById('emg-actions').textContent = (d.actions || []).join(', ');
        document.getElementById('emg-priority').textContent = d.priority_level || 'MAXIMUM';

        document.getElementById('emg-status').style.color = 'var(--red)';
        document.getElementById('emg-priority').style.color = 'var(--red)';
    } catch (e) {
        document.getElementById('emg-status').textContent = 'Error';
    } finally {
        btn.textContent = '🚑 ACTIVATE GREEN WAVE';
    }
}

// ── Bootstrap
buildHeatmap();
refreshUIC(); // Initial load
setInterval(refreshUIC, REFRESH_MS); // Live loop

// Auto-run first prediction on load
window.addEventListener('load', () => {
    setTimeout(runPrediction, 800);
});
