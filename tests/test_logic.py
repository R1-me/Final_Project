import unittest
from utils.media_classes import Movie
from utils.data_manager import save_favorite, get_favorites, remove_favorite

class TestMovieBotLogic(unittest.TestCase):

    def test_movie_object_creation(self):
        "Verifies that the Movie class properly initializes its properties"
        test_movie = Movie(
            title="The Matrix",
            rating=8.7,
            overview="Hackers learn the truth about reality.",
            genres=["Sci-Fi", "Action"],
            release_year="1999",
            duration=136,
            poster_url="https://image.tmdb.org/t/p/w500/path.jpg",
            cast="Keanu Reeves, Laurence Fishburne"
        )

        self.assertEqual(test_movie.title, "The Matrix")
        self.assertEqual(test_movie.release_year, "1999")
        self.assertEqual(test_movie.duration, 136)
        self.assertEqual(test_movie.cast, "Keanu Reeves, Laurence Fishburne")

    def test_data_manager_saving(self):
        "Ensures that saving functionality correctly writes to the data source"
        test_user_id = "test_user_999"
        test_movie_title = "Inception"

        save_result = save_favorite(test_user_id, test_movie_title)
        self.assertTrue(save_result)

        favorites = get_favorites(test_user_id)
        self.assertIn(test_movie_title, favorites)

    def test_remove_favorite(self):
        "Ensures the removal functionality correctly deletes a record"
        test_user_id = "test_user_remove"
        movie_title = "Interstellar"

        #Initialize the state
        save_favorite(test_user_id, movie_title)

        #Execute removal
        remove_favorite(test_user_id, movie_title)

        #Assert the state was correctly modified
        self.assertNotIn(movie_title, get_favorites(test_user_id))

if __name__ == "__main__":
    unittest.main()