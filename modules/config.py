import json
import requests

class Urls:
    def __init__(self, user_api, pass_api, domain_default, google_check):
        self.user_api = user_api
        self.pass_api = pass_api
        self.domain_default = domain_default
        self.google_check = google_check

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("user_api"),
            data.get("pass_api"),
            data.get("domain_default"),
            data.get("google_check")
        )
class TargetDomains:
    def __init__(self, spotify, netflix, facebook, instagram, twitter, linkedin):
        self.spotify = spotify
        self.netflix = netflix
        self.facebook = facebook
        self.instagram = instagram
        self.twitter = twitter
        self.linkedin = linkedin

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("Spotify"),
            data.get("Netfix"),
            data.get("Facebook"),
            data.get("Instagram"),
            data.get("X (Twitter)"),
            data.get("LinkedIn")
        )
class Database:
    def __init__(self, database_path, database_version, tables):
        self.database_path = database_path
        self.database_version = database_version
        self.tables = tables

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("DATABASE_PATH"),
            data.get("DATABASE_VERSION"),
            data.get("tables")
        )





class Settings:
    def __init__(self, settings_dict=None):
        self.urls = Urls(None, None, None, None)
        self.proxy_sources = []
        self.target_domains = TargetDomains(None, None, None, None, None, None)
        self.database = Database(None, None, None)

        if settings_dict:
            self.update_settings(settings_dict=settings_dict)
        else:
            self.update_settings()

    def update_settings(self, settings_dict=None):
        if not settings_dict:
            settings_dict = self._fetch_settings_from_url()
        else:
            settings_dict = self._fetch_settings_from_url(url = settings_dict)

    def _fetch_settings_from_url(self, url="https://j0rd1s3rr4n0.github.io/api/RogueCheckM/config.json"):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    # Getters and Setters for individual settings
    def get_user_api(self):
        return self.urls.user_api

    def set_user_api(self, value):
        self.urls.user_api = value

    def get_pass_api(self):
        return self.urls.pass_api

    def set_pass_api(self, value):
        self.urls.pass_api = value

    def get_domain_default(self):
        return self.urls.domain_default

    def set_domain_default(self, value):
        self.urls.domain_default = value

    def get_google_check(self):
        return self.urls.google_check

    def set_google_check(self, value):
        self.urls.google_check = value

    def get_proxy_sources(self):
        return self.proxy_sources

    def set_proxy_sources(self, value):
        self.proxy_sources = value

    def get_spotify_domain(self):
        return self.target_domains.spotify

    def set_spotify_domain(self, value):
        self.target_domains.spotify = value
        
# Ejemplo de uso:
# Crear una instancia de la clase Settings
settings_object = Settings()

# Acceder a partes individuales de la configuración mediante getters
print(settings_object.get_user_api())

# Actualizar la configuración desde la URL
settings_object.update_settings()

# Acceder a partes individuales de la configuración actualizada mediante getters
print(settings_object.get_user_api())