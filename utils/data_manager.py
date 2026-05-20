import json
import os

# Ensure the path works correctly across different operating systems
FILE_PATH = os.path.join("data", "users.json")

def load_data():
    "Reads user data from the JSON file"
    try:
        # Check if file exists to prevent FileNotFoundError on first run
        if not os.path.exists(FILE_PATH):
            return {}

        with open(FILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return {}

def save_favorite(user_id: str, movie_title: str):
    "Saves a favorite movie title for a specific user"
    try:
        data = load_data()

        # Initialize an empty list if the user is new
        if user_id not in data:
            data[user_id] = []

        # Prevent duplicate entries in the user's list
        if movie_title not in data[user_id]:
            data[user_id].append(movie_title)

        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        return True

    except Exception as e:
        print(f"Error saving to JSON file: {e}")
        return False

def get_favorites(user_id: str) -> list:
    "Returns the list of favorite movies for a given user"
    data = load_data()
    return data.get(user_id, [])

def remove_favorite(user_id: str, movie_title: str):
    "Removes a movie from the user's favorite list"
    try:
        data = load_data()

        if user_id in data:
            user_list = data[user_id]

            # Case-insensitive search for better user experience
            target_title = None
            for title in user_list:
                if title.lower() == movie_title.lower():
                    target_title = title
                    break

            # Remove the matched title and update the JSON file
            if target_title:
                user_list.remove(target_title)
                with open(FILE_PATH, "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4)
                return True

        return False
    except Exception as e:
        print(f"Error removing from JSON: {e}")
        return False

if __name__ == "__main__":
    # Test execution block
    print("Testing Data Manager...")
    test_user = "12345"
    save_favorite(test_user, "Interstellar")
    save_favorite(test_user, "Inception")

    favorites = get_favorites(test_user)
    print(f"Favorites for user {test_user}: {favorites}")