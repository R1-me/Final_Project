# Base class for media objects ENC
class Media:
    def __init__(self, title: str, rating: float, overview: str, genres: list, poster_url: str = "", cast: str = ""):
        self.title = title
        self.rating = rating
        self.overview = overview
        self.genres = genres
        self.poster_url = poster_url
        self.cast = cast

    def get_info(self):
        return f"Title: {self.title}, Rating: {self.rating}"

# Movie class inherits from Media and adds specific attributes POL
class Movie(Media):
    def __init__(self, title: str, rating: float, overview: str, genres: list, release_year: str, duration: int, poster_url: str = "", cast: str = ""):
        super().__init__(title, rating, overview, genres, poster_url, cast)
        self.release_year = release_year
        self.duration = duration


#Overriding the base method for specific string formatting
    def get_info(self):
        genres_str = ", ".join(self.genres)
        return (
            f"🎬 *{self.title}*\n\n"
            f"⭐ Rating: {self.rating}/10\n"
            f"🎭 Genre: {genres_str}\n"
            f"📅 Release Year: {self.release_year}\n"
            f"⏳ Duration: {self.duration} min\n"
            f"👥 Cast: {self.cast}\n\n"
            f"Description:\n{self.overview}"
        )

# Series class inheriting from Media
class Series(Media):
    def __init__(self, title: str, rating: float, overview: str, genres: list, seasons: int, release_year: str, poster_url: str = "", cast: str = ""):
        super().__init__(title, rating, overview, genres, poster_url, cast)
        self.seasons = seasons
        self.release_year = release_year

    def get_info(self):
        genres_str = ", ".join(self.genres)
        return (
            f"📺 *{self.title}*\n\n"
            f"⭐ Rating: {self.rating}/10\n"
            f"🎭 Genre: {genres_str}\n"
            f"📅 Release Year: {self.release_year}\n"
            f"🎞 Seasons: {self.seasons}\n"
            f"👥 Cast: {self.cast}\n\n"
            f"Description:\n{self.overview}"
        )