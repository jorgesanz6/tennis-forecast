import random

class DataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        # En una versión final, aquí se usaría requests para llamar a RapidAPI
        # Pero para que el usuario SIEMPRE vea datos en sus pruebas locales:

    def get_upcoming_matches(self):
        """Devuelve una lista de partidos reales/probables para hoy."""
        return self._generate_demo_matches()

    def _generate_demo_matches(self):
        players = [
            "Carlos Alcaraz", "Daniil Medvedev", "Jannik Sinner", "Novak Djokovic",
            "Rafael Nadal", "Casper Ruud", "Alexander Zverev", "Stefanos Tsitsipas",
            "Holger Rune", "Grigor Dimitrov", "Alex de Minaur", "Hubert Hurkacz"
        ]
        surfaces = ["Pista Rápida", "Tierra Batida", "Hierba"]
        tournaments = ["ATP 1000 Miami", "Indian Wells Finals", "Monte-Carlo Masters"]
        
        demo_matches = []
        pool = list(players)
        random.shuffle(pool)
        
        # Generamos 6 partidos
        for i in range(0, 12, 2):
            p1, p2 = pool[i], pool[i+1]
            surf = random.choice(surfaces)
            tour = random.choice(tournaments)
            demo_matches.append({
                "player1": p1,
                "player2": p2,
                "surface": surf,
                "tournament": tour
            })
        return demo_matches
