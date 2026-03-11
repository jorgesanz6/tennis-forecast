from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from elo_system import EloSystem
from data_fetcher import DataFetcher

app = FastAPI(title="Tennis Forecast AI 2026")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

elo_manager = EloSystem(k_factor=28)
# Key provided by user
API_KEY = "ab7ee06161msh16b021a83ae7a8dp1c03dcjsn51074bf9408e"
fetcher = DataFetcher(API_KEY)

# Stats Cache
cached_matches = []

# --- Initial Ratings for PRO 2026 ---
# Basado en proyecciones y estado actual del tour en 2026
pro_players = {
    "Jannik Sinner": 2245,
    "Carlos Alcaraz": 2210,
    "Novak Djokovic": 2015, # Veterano pero top
    "Daniil Medvedev": 1980,
    "Alexander Zverev": 1960,
    "Holger Rune": 1920,
    "Ben Shelton": 1880,
    "Alex Michelsen": 1780, # Joven promesa confirmada
    "Casper Ruud": 1890,
    "Cameron Norrie": 1810,
    "Rinky Hijikata": 1720,
    "Grigor Dimitrov": 1840,
    "Rafael Nadal": 1600 # Modo leyenda / Inactivo / Ranking bajo
}

for name, rating in pro_players.items():
    elo_manager.ratings[name] = rating
    elo_manager.surface_ratings[name] = {
        "Pista Rápida": rating,
        "Tierra Batida": rating if name != "Rafael Nadal" else 2200, # Legacy on clay
        "Hierba": rating
    }

class MatchPrediction(BaseModel):
    player1: str
    player2: str
    prob1: float
    prob2: float
    elo1: float
    elo2: float
    recommended_winner: str
    surface: str
    tournament: str
    date: str

@app.get("/")
def read_root():
    return {"status": "online", "date": "2026-03-11", "event": "Indian Wells Masters"}

@app.get("/matches", response_model=List[MatchPrediction])
def get_matches():
    global cached_matches
    if not cached_matches:
        try:
            # We fetch for today (March 11, 2026)
            raw_matches = fetcher.get_upcoming_matches("2026-03-11")
            predictions = []
            for m in raw_matches:
                p1 = m["player1"]
                p2 = m["player2"]
                surf = m["surface"]
                
                r1 = elo_manager.get_rating(p1, surf)
                r2 = elo_manager.get_rating(p2, surf)
                
                prob1 = elo_manager.calculate_expected_score(r1, r2)
                prob2 = 1 - prob1
                
                predictions.append({
                    "player1": p1,
                    "player2": p2,
                    "prob1": round(prob1 * 100, 2),
                    "prob2": round(prob2 * 100, 2),
                    "elo1": round(r1, 0),
                    "elo2": round(r2, 0),
                    "recommended_winner": p1 if prob1 > prob2 else p2,
                    "surface": surf,
                    "tournament": m.get("tournament", "Indian Wells"),
                    "date": m.get("date", "2026-03-11")
                })
            cached_matches = predictions
        except Exception as e:
            print(f"Error sync: {e}")
            return []
    return cached_matches

@app.get("/rankings")
def get_rankings():
    # Excluimos a Nadal si queremos un ranking de "activos top" o lo dejamos al final
    active_rankings = {k: v for k, v in elo_manager.ratings.items() if k != "Rafael Nadal"}
    sorted_rankings = sorted(active_rankings.items(), key=lambda x: x[1], reverse=True)
    return [{"name": name, "elo": round(elo, 0)} for name, elo in sorted_rankings]

@app.get("/sync")
def force_sync():
    global cached_matches
    cached_matches = []
    return get_matches()
