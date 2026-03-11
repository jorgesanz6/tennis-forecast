from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from elo_system import EloSystem

from data_fetcher import DataFetcher
import os

app = FastAPI(title="Tennis Forecast API")
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Tennis Forecast API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

elo_manager = EloSystem(k_factor=28)
# Use the user provided key or an environment variable
API_KEY = "ab7ee06161msh16b021a83ae7a8dp1c03dcjsn51074bf9408e"
fetcher = DataFetcher(API_KEY)

# Initial Mock Data (Top players from article)
elo_manager.ratings["Jannik Sinner"] = 2176
elo_manager.ratings["Novak Djokovic"] = 2096
elo_manager.ratings["Carlos Alcaraz"] = 2003

# Cache for today's matches
cached_matches = []

class PredictionRequest(BaseModel):
    player1: str
    player2: str
    surface: Optional[str] = "Hard"

class MatchPrediction(BaseModel):
    player1: str
    player2: str
    prob1: float
    prob2: float
    elo1: float
    elo2: float
    recommended_winner: str
    surface: str
    tournament: Optional[str] = ""

@app.get("/")
def read_root():
    return {"status": "Tennis Forecast API is running"}

@app.get("/sync")
def sync_matches():
    global cached_matches
    matches = fetcher.get_upcoming_matches()
    predictions = []
    
    for m in matches:
        r1 = elo_manager.get_rating(m["player1"], m["surface"])
        r2 = elo_manager.get_rating(m["player2"], m["surface"])
        
        prob1 = elo_manager.calculate_expected_score(r1, r2)
        prob2 = 1 - prob1
        
        predictions.append({
            "player1": m["player1"],
            "player2": m["player2"],
            "prob1": round(prob1 * 100, 2),
            "prob2": round(prob2 * 100, 2),
            "elo1": round(r1, 0),
            "elo2": round(r2, 0),
            "recommended_winner": m["player1"] if prob1 > prob2 else m["player2"],
            "surface": m["surface"],
            "tournament": m["tournament"]
        })
    
    cached_matches = predictions
    return {"msg": f"Synced {len(predictions)} matches", "count": len(predictions)}

@app.get("/matches")
def get_matches():
    if not cached_matches:
        return sync_matches()
    return cached_matches

@app.post("/predict", response_model=MatchPrediction)
# ... rest of the code remains similar but using MatchPrediction structure

@app.get("/rankings")
def get_rankings():
    sorted_rankings = sorted(elo_manager.ratings.items(), key=lambda x: x[1], reverse=True)
    return [{"name": name, "elo": round(elo, 0)} for name, elo in sorted_rankings]
