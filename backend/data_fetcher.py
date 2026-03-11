import requests
from datetime import datetime

class DataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://tennis-api-atp-wta-itf.p.rapidapi.com/tennis/v2"
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "tennis-api-atp-wta-itf.p.rapidapi.com"
        }

    def get_upcoming_matches(self):
        """
        Fetches matches for today.
        Note: Specific endpoint might vary based on Matchstat API version,
        but typically it's /matches or /schedule.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        url = f"{self.base_url}/matches"
        params = {"date": today}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return self._parse_matches(data)
        except Exception as e:
            print(f"Error fetching matches: {e}")
            return []

    def _parse_matches(self, data):
        """
        Simplifies the API response to a list of match dicts.
        """
        matches = []
        # Matchstat response structure usually has 'results' or 'data'
        results = data.get('results', []) or data.get('data', [])
        
        for item in results:
            # Basic mapping depending on actual API schema
            try:
                match_info = {
                    "player1": item.get('home_player', {}).get('name') or item.get('player1_name'),
                    "player2": item.get('away_player', {}).get('name') or item.get('player2_name'),
                    "surface": item.get('surface', 'Hard'),
                    "tournament": item.get('tournament_name', 'ATP Tour'),
                    "status": item.get('status', 'not_started')
                }
                if match_info["player1"] and match_info["player2"]:
                    matches.append(match_info)
            except:
                continue
        return matches

if __name__ == "__main__":
    # Test with the provided key
    fetcher = DataFetcher("ab7ee06161msh16b021a83ae7a8dp1c03dcjsn51074bf9408e")
    matches = fetcher.get_upcoming_matches()
    print(f"Found {len(matches)} matches for today.")
    for m in matches[:5]:
        print(f"{m['player1']} vs {m['player2']} ({m['surface']})")
