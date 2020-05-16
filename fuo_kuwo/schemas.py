from marshmallow import Schema, fields, post_load, EXCLUDE


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE


Schema = BaseSchema


class KuwoSongSchema(Schema):
    identifier = fields.Int(data_key='rid', required=True)
    duration = fields.Int(data_key='duration', required=True)
    title = fields.Str(data_key='name', required=True)
    artist = fields.Str(data_key='artist', required=True)
    artistid = fields.Int(data_key='artistid', required=True)
    album = fields.Str(data_key='album', required=False)
    albumid = fields.Int(data_key='albumid', required=False)
    albumpic = fields.Str(data_key='albumpic', required=False)
    lossless = fields.Bool(data_key='hasLossless', required=False)
    hasmv = fields.Int(data_key='hasmv', required=False)

    @post_load
    def create_model(self, data, **kwargs):
        artists = [KuwoArtistModel(identifier=data.get('artistid'), name=data.get('artist'))] \
            if data.get('artistid') else []
        album = KuwoAlbumModel(identifier=data.get('albumid'), name=data.get('album'),
                               cover=data.get('albumpic', '')) if data.get('albumid') else None
        return KuwoSongModel(identifier=data.get('identifier'),
                             duration=data.get('duration') * 1000,
                             title=data.get('title'),
                             artists=artists,
                             album=album,
                             lossless=data.get('lossless', False),
                             hasmv=data.get('hasmv', 0))


class KuwoAlbumSchema(Schema):
    identifier = fields.Int(data_key='albumid', required=True)
    name = fields.Str(data_key='album', required=True)
    cover = fields.Str(data_key='pic', required=False)
    artist = fields.Str(data_key='artist', required=True)
    artistid = fields.Int(data_key='artistid', required=True)
    albuminfo = fields.Str(data_key='albuminfo', required=False)

    @post_load
    def create_model(self, data, **kwargs):
        return KuwoAlbumModel(identifier=data.get('identifier'), name=data.get('name'),
                              artists=[KuwoArtistModel(identifier=data.get('artistid'), name=data.get('artist'))],
                              desc=data.get('albuminfo', ''))


from .models import KuwoSongModel, KuwoArtistModel, KuwoAlbumModel
