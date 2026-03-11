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

    const upcomingMatches = [
        { p1: "Carlos Alcaraz", p2: "Daniil Medvedev", p1Elo: 2003, p2Elo: 1985, prob1: 54, surface: "Hard" },
        { p1: "Rafa Nadal", p2: "Casper Ruud", p1Elo: 2150, p2Elo: 1910, prob1: 78, surface: "Clay" },
        { p1: "Alexander Zverev", p2: "Stefanos Tsitsipas", p1Elo: 1940, p2Elo: 1925, prob1: 51, surface: "Hard" }
    ];

    const matchList = document.getElementById('matchList');

    upcomingMatches.forEach((match, index) => {
        const card = document.createElement('div');
        card.className = 'prediction-card small';
        card.style.animationDelay = `${index * 0.2}s`;

        card.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 1.5rem; background: rgba(255,255,255,0.03); border-radius: 16px; margin-bottom: 1rem; border: 1px solid rgba(255,255,255,0.05);">
                <div style="text-align: left;">
                    <div style="font-weight: 700;">${match.p1}</div>
                    <div style="font-size: 0.8rem; color: #a0a0a8;">ELO: ${match.p1Elo}</div>
                </div>
                <div style="font-weight: 800; opacity: 0.3;">VS</div>
                <div style="text-align: right;">
                    <div style="font-weight: 700;">${match.p2}</div>
                    <div style="font-size: 0.8rem; color: #a0a0a8;">ELO: ${match.p2Elo}</div>
                </div>
            </div>
            <div class="probability-meter">
                <div class="bar" style="height: 6px;">
                    <div class="fill" style="width: ${match.prob1}%; height: 6px;"></div>
                </div>
                <div class="labels" style="font-size: 0.8rem;">
                    <span>${match.prob1}%</span>
                    <span>${100 - match.prob1}%</span>
                </div>
            </div>
        `;

        matchList.appendChild(card);
    });
});
