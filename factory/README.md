# Factory Pattern

Reference: https://realpython.com/factory-method-python/

## Steps

- The first step when you see complex conditional code(if/else if/else) in an application is to identify the common goal of each of the execution paths (or logical paths).

## Basic Implementation of Factory Method

The central idea in Factory Method is to provide a separate component with the responsibility to decide which concrete implementation should be used based on some specified parameter. That parameter in our example is the format.

- find common goal
- separate common goal in condition statements
- find parameters leading us to if/else if/else condition

The mechanics of Factory Method are always the same. A client (SongSerializer.serialize()) depends on a concrete implementation of an interface. It requests the implementation from a creator component (get_serializer()) using some sort of identifier (format).

```python
class SongSerializer:
    def serialize(self, song, format):
        serializer = get_serializer(format)
        return serializer(song)


def get_serializer(format):
    if format == 'JSON':
        return _serialize_to_json
    elif format == 'XML':
        return _serialize_to_xml
    else:
        raise ValueError(format)


def _serialize_to_json(song):
    payload = {
        'id': song.song_id,
        'title': song.title,
        'artist': song.artist
    }
    return json.dumps(payload)


def _serialize_to_xml(song):
    song_element = et.Element('song', attrib={'id': song.song_id})
    title = et.SubElement(song_element, 'title')
    title.text = song.title
    artist = et.SubElement(song_element, 'artist')
    artist.text = song.artist
    return et.tostring(song_element, encoding='unicode')
```

## Recognizing Opportunities to Use Factory Method

Factory Method should be used in every situation where an application (client, such as api) depends on an interface (product, such as http, database) to perform a task and there are multiple concrete implementations of that interface. You need to provide a parameter(such as post, get) that can identify the concrete implementation and use it in the creator to decide the concrete implementation.



```python
import json
import xml.etree.ElementTree as et

class JsonSerializer:
    def __init__(self):
        self._current_object = None

    def start_object(self, object_name, object_id):
        self._current_object = {
            'id': object_id
        }

    def add_property(self, name, value):
        self._current_object[name] = value

    def to_str(self):
        return json.dumps(self._current_object)


class XmlSerializer:
    def __init__(self):
        self._element = None

    def start_object(self, object_name, object_id):
        self._element = et.Element(object_name, attrib={'id': object_id})

    def add_property(self, name, value):
        prop = et.SubElement(self._element, name)
        prop.text = value

    def to_str(self):
        return et.tostring(self._element, encoding='unicode')

class ObjectSerializer:
    def serialize(self, serializable, format):
        serializer = factory.get_serializer(format)
        serializable.serialize(serializer)
        return serializer.to_str()

class SerializerFactory:
    def get_serializer(self, format):
        if format == 'JSON':
            return JsonSerializer()
        elif format == 'XML':
            return XmlSerializer()
        else:
            raise ValueError(format)


factory = SerializerFactory()

class SerializerFactory:

    def __init__(self):
        self._creators = {}

    def register_format(self, format, creator):
        self._creators[format] = creator

    def get_serializer(self, format):
        creator = self._creators.get(format)
        if not creator:
            raise ValueError(format)
        return creator()


factory = SerializerFactory()
factory.register_format('JSON', JsonSerializer)
factory.register_format('XML', XmlSerializer)
```

```python
# In songs.py

class Song:
    def __init__(self, song_id, title, artist):
        self.song_id = song_id
        self.title = title
        self.artist = artist

    def serialize(self, serializer):
        serializer.start_object('song', self.song_id)
        serializer.add_property('title', self.title)
        serializer.add_property('artist', self.artist)
```

implement

```python
>>> import songs
>>> import serializers
>>> song = songs.Song('1', 'Water of Love', 'Dire Straits')
>>> serializer = serializers.ObjectSerializer()

>>> serializer.serialize(song, 'JSON')
'{"id": "1", "title": "Water of Love", "artist": "Dire Straits"}'

>>> serializer.serialize(song, 'XML')
```

```python
# In music.py
import object_factory

# Omitting other implementation classes shown above

factory = object_factory.ObjectFactory()
factory.register_builder('SPOTIFY', SpotifyServiceBuilder())
factory.register_builder('PANDORA', PandoraServiceBuilder())
factory.register_builder('LOCAL', create_local_music_service)

class SpotifyService:
    def __init__(self, access_code):
        self._access_code = access_code

    def test_connection(self):
        print(f'Accessing Spotify with {self._access_code}')


class SpotifyServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, spotify_client_key, spotify_client_secret, **_ignored):
        if not self._instance:
            access_code = self.authorize(
                spotify_client_key, spotify_client_secret)
            self._instance = SpotifyService(access_code)
        return self._instance

    def authorize(self, key, secret):
        return 'SPOTIFY_ACCESS_CODE'

        class PandoraService:
            def __init__(self, consumer_key, consumer_secret):
                self._key = consumer_key
                self._secret = consumer_secret

            def test_connection(self):
                print(f'Accessing Pandora with {self._key} and {self._secret}')


class PandoraServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, pandora_client_key, pandora_client_secret, **_ignored):
        if not self._instance:
            consumer_key, consumer_secret = self.authorize(
                pandora_client_key, pandora_client_secret)
            self._instance = PandoraService(consumer_key, consumer_secret)
        return self._instance

    def authorize(self, key, secret):
        return 'PANDORA_CONSUMER_KEY', 'PANDORA_CONSUMER_SECRET'

        class LocalService:
            def __init__(self, location):
                self._location = location

            def test_connection(self):
                print(f'Accessing Local music at {self._location}')


def create_local_music_service(local_music_location, **_ignored):
    return LocalService(local_music_location)
```

```python
# In object_factory.py

class ObjectFactory:
    def __init__(self):
        self._builders = {}

    def register_builder(self, key, builder):
        self._builders[key] = builder

    def create(self, key, **kwargs):
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)
```

```python
# In program.py
import music

config = {
    'spotify_client_key': 'THE_SPOTIFY_CLIENT_KEY',
    'spotify_client_secret': 'THE_SPOTIFY_CLIENT_SECRET',
    'pandora_client_key': 'THE_PANDORA_CLIENT_KEY',
    'pandora_client_secret': 'THE_PANDORA_CLIENT_SECRET',
    'local_music_location': '/usr/data/music'
}

pandora = music.factory.create('PANDORA', **config)
pandora.test_connection()

spotify = music.factory.create('SPOTIFY', **config)
spotify.test_connection()

local = music.factory.create('LOCAL', **config)
local.test_connection()

pandora2 = music.services.get('PANDORA', **config)
print(f'id(pandora) == id(pandora2): {id(pandora) == id(pandora2)}')

spotify2 = music.services.get('SPOTIFY', **config)
print(f'id(spotify) == id(spotify2): {id(spotify) == id(spotify2)}')
```
