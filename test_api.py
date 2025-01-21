from api_utils import fetch_movie_details

API_KEY = "2849e462"

if __name__ == "__main__":
    movie_title = input("Enter a movie title: ")
    details = fetch_movie_details(API_KEY, movie_title)
    print(details)
