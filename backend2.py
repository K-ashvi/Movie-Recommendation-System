from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend's URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hardcoded TMDB API Key
TMDB_API_KEY = "api_key"

class MovieInput(BaseModel):
    movie1: str
    movie2: str
    movie3: str
    movie4: str

def get_movie_id(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]['id']
    return None

# Endpoint to handle movie recommendations
@app.post("/recommendations")
async def get_recommendations(movies: MovieInput):
    movie_ids = []
    
    # Get movie IDs for each movie title
    for movie in [movies.movie1, movies.movie2, movies.movie3, movies.movie4]:
        movie_id = get_movie_id(movie)
        if movie_id:
            movie_ids.append(movie_id)
        else:
            raise HTTPException(status_code=404, detail=f"Movie '{movie}' not found")

    recommendations = []

    # Fetch recommendations for each movie ID
    for movie_id in movie_ids:
        rec_url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={TMDB_API_KEY}"
        response = requests.get(rec_url)
        if response.status_code == 200:
            data = response.json()
            recommendations.extend([rec['title'] for rec in data['results'][:5]])  # Top 5 recommendations
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching recommendations")

    # Remove duplicate recommendations
    recommendations = list(set(recommendations))
    
    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendations found")
    
    return {"recommendations": recommendations}
