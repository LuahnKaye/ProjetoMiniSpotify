class User:
    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

    def to_dict(self):
        return {
            "email": self.email,
            "name": self.name,
            "password": self.password
        }


class Playlist:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.musics = []

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "musics": self.musics
        }


class Music:
    def __init__(self, name, artist):
        self.name = name
        self.artist = artist

    def to_dict(self):
        return {
            "name": self.name,
            "artist": self.artist
        }
