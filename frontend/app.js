document.addEventListener('DOMContentLoaded', () => {
    console.log('Tennis Forecast AI Initialized');

    // Smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    const matchList = document.getElementById('matchList');
    const heroCard = document.querySelector('#match-of-the-day .prediction-card');

    async function fetchMatches() {
        try {
            // Tentamos conectar con el backend local
            const response = await fetch('http://localhost:8000/matches');
            if (!response.ok) throw new Error('Backend not responding');
            const matches = await response.json();

            if (matches && matches.length > 0) {
                renderMatches(matches);
                updateHero(matches[0]);
            } else {
                renderEmpty();
            }
        } catch (error) {
            console.error('Error fetching matches:', error);
            renderError();
        }
    }

    function updateHero(match) {
        heroCard.innerHTML = `
            <div class="player-container">
                <div class="player">
                    <div class="player-rank">#1 PROB</div>
                    <div class="player-name">${match.player1}</div>
                    <div class="player-elo">ELO: ${match.elo1}</div>
                </div>
                <div class="vs">VS</div>
                <div class="player">
                    <div class="player-rank">#2 PROB</div>
                    <div class="player-name">${match.player2}</div>
                    <div class="player-elo">ELO: ${match.elo2}</div>
                </div>
            </div>
            <div class="probability-meter">
                <div class="bar">
                    <div class="fill" style="width: ${match.prob1}%;"></div>
                </div>
                <div class="labels">
                    <span>${match.prob1}% - ${match.player1}</span>
                    <span>${match.prob2}% - ${match.player2}</span>
                </div>
            </div>
            <div class="prediction-badge">Victoria Recomendada: ${match.recommended_winner}</div>
        `;
    }

    function renderMatches(matches) {
        matchList.innerHTML = '';
        matches.slice(1).forEach((match, index) => {
            const card = document.createElement('div');
            card.className = 'prediction-card small';
            card.style.cssText = `
                background: var(--card-bg);
                border: 1px solid var(--glass-border);
                border-radius: 16px;
                padding: 1.5rem;
                margin-bottom: 1rem;
                animation: fadeInUp 0.5s ease-out forwards;
                animation-delay: ${index * 0.1}s;
                opacity: 0;
            `;

            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div>
                        <div style="font-weight: 700;">${match.player1}</div>
                        <div style="font-size: 0.8rem; color: var(--text-secondary);">ELO: ${match.elo1}</div>
                    </div>
                    <div style="font-weight: 800; opacity: 0.3;">VS</div>
                    <div style="text-align: right;">
                        <div style="font-weight: 700;">${match.player2}</div>
                        <div style="font-size: 0.8rem; color: var(--text-secondary);">ELO: ${match.elo2}</div>
                    </div>
                </div>
                <div class="probability-meter">
                    <div class="bar" style="height: 6px; background: rgba(255,255,255,0.05); border-radius: 3px; overflow: hidden;">
                        <div class="fill" style="width: ${match.prob1}%; height: 100%; background: var(--gradient);"></div>
                    </div>
                    <div class="labels" style="display: flex; justify-content: space-between; font-size: 0.75rem; margin-top: 5px; font-weight: 600;">
                        <span>${match.prob1}%</span>
                        <span>${match.prob2}%</span>
                    </div>
                </div>
            `;
            matchList.appendChild(card);
        });
    }

    function renderEmpty() {
        matchList.innerHTML = '<p style="text-align:center; color: var(--text-secondary);">No hay partidos programados para hoy.</p>';
    }

    function renderError() {
        matchList.innerHTML = '<p style="text-align:center; color: #ff4b2b;">Inicia el backend (uvicorn main:app) para ver datos reales.</p>';
    }

    fetchMatches();
});
