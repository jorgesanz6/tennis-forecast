from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from elo_system import EloSystem

app = FastAPI(title="Tennis Forecast API")
elo_manager = EloSystem(k_factor=28)

# Initial Mock Data (Top players from article)
elo_manager.ratings["Jannik Sinner"] = 2176
elo_manager.ratings["Novak Djokovic"] = 2096
elo_manager.ratings["Carlos Alcaraz"] = 2003

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

@app.get("/")
def read_root():
    return {"status": "Tennis Forecast API is running"}

@app.post("/predict", response_model=MatchPrediction)
def predict_match(req: PredictionRequest):
    r1 = elo_manager.get_rating(req.player1, req.surface)
    r2 = elo_manager.get_rating(req.player2, req.surface)
    
    prob1 = elo_manager.calculate_expected_score(r1, r2)
    prob2 = 1 - prob1
    
    winner = req.player1 if prob1 > prob2 else req.player2
    
    return {
        "player1": req.player1,
        "player2": req.player2,
        "prob1": round(prob1 * 100, 2),
        "prob2": round(prob2 * 100, 2),
        "elo1": round(r1, 0),
        "elo2": round(r2, 0),
        "recommended_winner": winner
    }

@app.get("/rankings")
def get_rankings():
    sorted_rankings = sorted(elo_manager.ratings.items(), key=lambda x: x[1], reverse=True)
    return [{"name": name, "elo": round(elo, 0)} for name, elo in sorted_rankings]
