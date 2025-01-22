import requests

def fetch_movie_details(api_key, title):
    """Fetch movie details from OMDb API by title"""
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title.strip().lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            # Extract required fields
            return {
                "name": data.get("Title"),
                "director": data.get("Director"),
                "year": int(data.get("Year")),
                "poster": data.get("Poster"),
            }
        else:
            return {"error": data.get("Error", "Movie not found.")}
    else:
        return {"error": "Failed to fetch data from OMDb API."}
