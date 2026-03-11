document.addEventListener('DOMContentLoaded', () => {
    console.log('Tennis Forecast AI Initialized');

    // Smooth scroll and active link highlighting
    const navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            document.querySelector(targetId).scrollIntoView({
                behavior: 'smooth'
            });

            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });

    const matchList = document.getElementById('matchList');
    const heroMatchContainer = document.getElementById('hero-match-container');
    const rankingTableBody = document.querySelector('#rankingTable tbody');

    async function fetchData() {
        try {
            // Fetch Matches
            const matchRes = await fetch('http://localhost:8888/matches');
            const matches = await matchRes.json();

            if (matches && matches.length > 0) {
                renderHeroMatch(matches[0]);
                renderMatchList(matches.slice(1));
            } else {
                renderEmptyMatches();
            }

            // Fetch Rankings
            const rankRes = await fetch('http://localhost:8888/rankings');
            const rankings = await rankRes.json();
            renderRankings(rankings);

        } catch (error) {
            console.error('Data fetch error:', error);
            renderErrorUi();
        }
    }

    function renderHeroMatch(match) {
        heroMatchContainer.innerHTML = `
            <div class="prediction-card premium">
                <div class="player-container">
                    <div class="player">
                        <div class="player-rank">#1 ELO</div>
                        <div class="player-name">${match.player1}</div>
                        <div class="player-elo">ELO: ${match.elo1}</div>
                    </div>
                    <div class="vs">VS</div>
                    <div class="player">
                        <div class="player-rank">#2 ELO</div>
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
            </div>
        `;
    }

    function renderMatchList(matches) {
        matchList.innerHTML = '';
        if (matches.length === 0) {
            matchList.innerHTML = '<p style="text-align:center; opacity:0.5;">No hay más partidos programados hoy.</p>';
            return;
        }

        matches.forEach((match, index) => {
            const card = document.createElement('div');
            card.className = 'prediction-card';
            card.style.padding = '1.5rem';
            card.style.marginBottom = '1rem';
            card.style.animation = `fadeInUp 0.5s ease-out forwards`;
            card.style.animationDelay = `${index * 0.1}s`;
            card.style.opacity = '0';

            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div>
                        <div style="font-weight: 700;">${match.player1}</div>
                        <div style="font-size: 0.8rem; color: var(--text-secondary);">ELO: ${match.elo1}</div>
                    </div>
                    <div class="vs" style="font-size: 1rem;">VS</div>
                    <div style="text-align: right;">
                        <div style="font-weight: 700;">${match.player2}</div>
                        <div style="font-size: 0.8rem; color: var(--text-secondary);">ELO: ${match.elo2}</div>
                    </div>
                </div>
                <div class="probability-meter" style="margin-bottom: 0;">
                    <div class="bar" style="height: 6px;">
                        <div class="fill" style="width: ${match.prob1}%; height: 6px;"></div>
                    </div>
                    <div class="labels" style="font-size: 0.7rem;">
                        <span>${match.prob1}%</span>
                        <span>${match.prob2}%</span>
                    </div>
                </div>
            `;
            matchList.appendChild(card);
        });
    }

    function renderRankings(rankings) {
        rankingTableBody.innerHTML = '';
        rankings.forEach((player, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td style="color: var(--accent); font-weight: 800;">${index + 1}</td>
                <td style="font-weight: 700;">${player.name}</td>
                <td>${player.elo}</td>
                <td style="color: #00ff88;">Stable ↑</td>
            `;
            rankingTableBody.appendChild(row);
        });
    }

    function renderEmptyMatches() {
        heroMatchContainer.innerHTML = '<div class="prediction-card premium"><p style="text-align:center;">No hay partidos cargados. Prueba reiniciando el backend.</p></div>';
        matchList.innerHTML = '';
    }

    function renderErrorUi() {
        heroMatchContainer.innerHTML = '<div class="prediction-card premium"><p style="text-align:center; color:#ff4b2b;">Error de conexión con el backend.</p></div>';
    }

    fetchData();
});
