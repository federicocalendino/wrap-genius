from datetime import datetime
from typing import Dict, List

from .album import Album
from .artist import Artist
from .media import Media
from .stats import Stats


def lazy_property(prop):
    @property
    def wrapper(*args):
        self = args[0]
        if not self._fully_loaded_:
            data = self.api.get_song_data(self.id)
            self.__init_extra_data__(data)
            self._fully_loaded_ = True
        return prop(self)

    return wrapper


class Song:
    _fully_loaded_: bool = False

    def __init__(self, api, data):
        self.api = api

        self.id: int = data["id"]
        self.title: str = data["title"]
        self.title_with_featured: str = data["title_with_featured"]
        self.url: str = data["url"]
        self.api_path: str = data["api_path"]
        self.full_title: str = data["full_title"]
        self.path: str = data["path"]
        self.primary_artist: 'Artist' = Artist(self.api, data["primary_artist"])

        self.annotation_count: int = data.get("annotation_count", 0)
        self.header_image_thumbnail_url: str = data.get("header_image_thumbnail_url")
        self.header_image_url: str = data.get("header_image_url")
        self.lyrics_owner_id: int = data.get("lyrics_owner_id", 0)
        self.lyrics_state: str = data.get("lyrics_state")
        self.pyongs_count: int = data.get("pyongs_count", 0)
        self.song_art_image_thumbnail_url: str = data.get("song_art_image_thumbnail_url")
        self.song_art_image_url: str = data.get("song_art_image_url")

        self.__init_extra_data__(data)

    def __init_extra_data__(self, data):
        self.__apple_music_id: str = data.get("apple_music_id")
        self.__apple_music_player_url: str = data.get("apple_music_player_url")
        self.__description: str = data.get("description")
        self.__embed_content: str = data.get("embed_content")
        self.__featured_video: bool = data.get("featured_video", False)
        self.__lyrics_marked_complete_by: str = data.get("lyrics_marked_complete_by")
        self.__lyrics_placeholder_reason: str = data.get("lyrics_placeholder_reason")
        self.__recording_location: str = data.get("recording_location")
        self.__release_date_for_display: str = data.get("release_date_for_display")

        release_date = data.get("release_date")

        if release_date:
            self.__release_date: datetime = datetime.strptime(release_date, "%Y-%m-%d")
        else:
            self.__release_date = None

        self.__stats: Stats = Stats(self.api, data["stats"])
        self.__album: Album = Album(self.api, data.get("album")) if data.get("album") else None

        self.__media: Dict[str, Media] = dict(map(
            lambda m: (m["provider"], Media(self.api, m)),
            data.get("media", [])
        ))

        self.__featured_artists: List['Artist'] = list(map(
            lambda fa: Artist(self.api, fa),
            data.get("featured_artists", [])
        ))
        self.__producer_artists: List['Artist'] = list(map(
            lambda pa: Artist(self.api, pa),
            data.get("producer_artists", [])
        ))
        self.__writer_artists: List['Artist'] = list(map(
            lambda wa: Artist(self.api, wa),
            data.get("writer_artists", [])
        ))

        for relationship in data.get("song_relationships", []):
            type_ = relationship["type"]
            songs = list(map(
                lambda rs: Song(self.api, rs),
                relationship.get("songs", [])
            ))

            if type_ == "samples":
                self.__samples: List['Song'] = songs
            elif type_ == "sampled_in":
                self.__sampled_in: List['Song'] = songs
            elif type_ == "interpolates":
                self.__interpolates: List['Song'] = songs
            elif type_ == "interpolated_by":
                self.__interpolated_by: List['Song'] = songs
            elif type_ == "cover_of":
                self.__cover_of: List['Song'] = songs
            elif type_ == "covered_by":
                self.__covered_by: List['Song'] = songs
            elif type_ == "remix_of":
                self.__remix_of: List['Song'] = songs
            elif type_ == "remixed_by":
                self.__remixed_by: List['Song'] = songs
            elif type_ == "live_version_of":
                self.__live_version_of: List['Song'] = songs
            elif type_ == "performed_live_as":
                self.__performed_live_as: List['Song'] = songs

    @lazy_property
    def apple_music_id(self) -> str:
        return self.__apple_music_id

    @lazy_property
    def apple_music_player_url(self) -> str:
        return self.__apple_music_player_url

    @lazy_property
    def description(self) -> str:
        return self.__description

    @lazy_property
    def embed_content(self) -> str:
        return self.__embed_content

    @lazy_property
    def featured_video(self) -> bool:
        return self.__featured_video

    @lazy_property
    def lyrics_marked_complete_by(self) -> str:
        return self.__lyrics_marked_complete_by

    @lazy_property
    def lyrics_placeholder_reason(self) -> str:
        return self.__lyrics_placeholder_reason

    @lazy_property
    def recording_location(self) -> str:
        return self.__recording_location

    @lazy_property
    def release_date(self) -> datetime:
        return self.__release_date

    @lazy_property
    def release_date_for_display(self) -> str:
        return self.__release_date_for_display

    @lazy_property
    def stats(self) -> 'Stats':
        return self.__stats

    @lazy_property
    def album(self) -> 'Album':
        return self.__album

    @lazy_property
    def media(self) -> Dict[str, Media]:
        return self.__media

    @lazy_property
    def featured_artists(self) -> List['Artist']:
        return self.__featured_artists

    @lazy_property
    def producer_artists(self) -> List['Artist']:
        return self.__producer_artists

    @lazy_property
    def writer_artists(self) -> List['Artist']:
        return self.__writer_artists

    @lazy_property
    def samples(self) -> List['Song']:
        return self.__samples

    @lazy_property
    def sampled_in(self) -> List['Song']:
        return self.__sampled_in

    @lazy_property
    def interpolates(self) -> List['Song']:
        return self.__interpolates

    @lazy_property
    def interpolated_by(self) -> List['Song']:
        return self.__interpolated_by

    @lazy_property
    def cover_of(self) -> List['Song']:
        return self.__cover_of

    @lazy_property
    def covered_by(self) -> List['Song']:
        return self.__covered_by

    @lazy_property
    def remix_of(self) -> List['Song']:
        return self.__remix_of

    @lazy_property
    def remixed_by(self) -> List['Song']:
        return self.__remixed_by

    @lazy_property
    def live_version_of(self) -> List['Song']:
        return self.__live_version_of

    @lazy_property
    def performed_live_as(self) -> List['Song']:
        return self.__performed_live_as

    def __repr__(self):
        return f"{self.title} ({self.id})"
