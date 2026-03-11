import math

class EloSystem:
    def __init__(self, k_factor=32, initial_rating=1500):
        self.k_factor = k_factor
        self.initial_rating = initial_rating
        self.ratings = {}  # player_id -> rating
        self.surface_ratings = {} # player_id -> {surface -> rating}

    def get_rating(self, player_id, surface=None):
        if player_id not in self.ratings:
            self.ratings[player_id] = self.initial_rating
        
        if player_id not in self.surface_ratings:
            self.surface_ratings[player_id] = {"Pista Rápida": 1500, "Tierra Batida": 1500, "Hierba": 1500}
        
        if surface and surface in self.surface_ratings[player_id]:
            # Weight: 70% surface specific, 30% general (common approach)
            return 0.7 * self.surface_ratings[player_id][surface] + 0.3 * self.ratings[player_id]
        return self.ratings[player_id]

    def calculate_expected_score(self, rating_a, rating_b):
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

    def update_ratings(self, winner_id, loser_id, surface=None):
        # Update General Elo
        r_winner = self.get_rating(winner_id)
        r_loser = self.get_rating(loser_id)
        
        expected_winner = self.calculate_expected_score(r_winner, r_loser)
        
        # Winner gets points, loser loses points
        change = self.k_factor * (1 - expected_winner)
        self.ratings[winner_id] += change
        self.ratings[loser_id] -= change

        # Update Surface Elo
        if surface:
            rs_winner = self.surface_ratings[winner_id][surface]
            rs_loser = self.surface_ratings[loser_id][surface]
            
            expected_s_winner = self.calculate_expected_score(rs_winner, rs_loser)
            s_change = self.k_factor * (1 - expected_s_winner)
            
            self.surface_ratings[winner_id][surface] += s_change
            self.surface_ratings[loser_id][surface] -= s_change
        
        return change

# Example usage (Alcaraz vs Djokovic Wimbledon 2023)
# Alcaraz (2063) vs Djokovic (2120)
if __name__ == "__main__":
    system = EloSystem(k_factor=28) # Higher K for Pro
    system.ratings["Alcaraz"] = 2063
    system.ratings["Djokovic"] = 2120
    
    change = system.update_ratings("Alcaraz", "Djokovic")
    print(f"Alcaraz new rating: {system.get_rating('Alcaraz'):.2f} (Change: +{change:.2f})")
    print(f"Djokovic new rating: {system.get_rating('Djokovic'):.2f} (Change: -{change:.2f})")
