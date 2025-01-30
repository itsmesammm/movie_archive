import requests

def fetch_movie_details(api_key, title):
    """Fetch movie details from OMDb API by title"""
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title.strip().lower()}"

    try:
        response = requests.get(url)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        if data.get('Error'): # check for OMDb error
            raise ValueError(data['Error'])


        return {
                "name": data.get("Title"),
                "director": data.get("Director"),
                "year": int(data.get("Year")),
                "poster": data.get("Poster"),
            }

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error fetching movie data: {e}")  # More general error message
    except ValueError as e:  # Re-raise the ValueError from API
        raise