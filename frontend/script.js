let currentLang = 'en';

const TRANSLATIONS = {
    en: {
        road_clear: "CLEAR ✅",
        road_blocked: "BLOCKED ❌",
        access_good: "GOOD",
        access_limited: "LIMITED ⚠️",
        access_fair: "FAIR",
        syncing: "Syncing Situational Data...",
        no_action: "Waiting for agent decision..."
    },
    hi: {
        road_clear: "स्पष्ट ✅",
        road_blocked: "अवरुद्ध ❌",
        access_good: "अच्छा",
        access_limited: "सीमित ⚠️",
        access_fair: "ठीक है",
        syncing: "स्थितिजन्य डेटा सिंक हो रहा है...",
        no_action: "एजेंट निर्णय की प्रतीक्षा की जा रही है..."
    }
};

function changeLang() {
    currentLang = document.getElementById('lang-select').value;
    updateStats();
}

async function updateStats() {
    try {
        const res = await fetch('/state');
        if (!res.ok) throw new Error("Sync failure");
        const state = await res.json();
        const t = TRANSLATIONS[currentLang] || TRANSLATIONS['en'];

        // Header & Meta
        document.getElementById('ui-region-name').innerText = state.region;
        document.getElementById('ui-coords').innerText = `${state.lat.toFixed(4)}, ${state.lon.toFixed(4)}`;
        document.getElementById('ui-last-updated').innerText = `Last Updated: ${state.last_updated_str}`;
        
        // Weather Banner
        document.getElementById('ui-rain-val').innerText = state.rainfall;
        document.getElementById('ui-forecast-val').innerText = state.forecast.toUpperCase();
        document.getElementById('ui-terrain-val').innerText = state.terrain.toUpperCase();
        document.getElementById('ui-severity-val').innerText = (state.severity * 100).toFixed(0) + "%";
        
        // Infrastructure
        document.getElementById('ui-road-val').innerText = state.road_blocked ? t.road_blocked : t.road_clear;
        document.getElementById('ui-road-val').className = "val-text " + (state.road_blocked ? 'color-danger' : 'color-success');
        document.getElementById('ui-traffic-val').innerText = state.traffic;
        document.getElementById('ui-rescue-val').innerText = state.rescue_access.toUpperCase();
        document.getElementById('ui-alt-val').innerText = state.altitude;

        // Resources
        document.getElementById('ui-boats-v').innerText = state.resources.boats;
        document.getElementById('ui-med-v').innerText = state.resources.ambulances;
        document.getElementById('ui-kits-v').innerText = state.resources.food_kits;

        // Action & Feedback
        if (state.last_action) {
            document.getElementById('ui-insight').innerHTML = `
                <b>Decision:</b> ${state.last_action.decision.toUpperCase()}<br>
                <b>Method:</b> ${state.last_action.method || 'Standard'}<br>
                <b>Reasoning:</b> ${state.last_action.reasoning}
            `;
            const fb = state.last_action.feedback || [];
            document.getElementById('ui-feedback').innerText = fb.length > 0 ? fb[fb.length - 1] : "Decision verified.";
        } else {
            document.getElementById('ui-insight').innerText = t.no_action;
        }

        // Impact Panel
        document.getElementById('ui-pop-val').innerText = state.population.toLocaleString();
        document.getElementById('ui-cas-val').innerText = state.casualties;
        document.getElementById('ui-sens-val').innerText = state.time_sensitivity;
        
        const score = state.last_action ? (state.last_action.score || "--") : "--";
        document.getElementById('ui-score-val').innerText = score;

    } catch (e) {
        console.error("DR-OpenEnv Error", e);
    }
}

async function resetEnv() {
    await fetch('/reset');
    updateStats();
}

// Initial Load
setInterval(updateStats, 2000);
updateStats();
