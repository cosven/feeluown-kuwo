import logging

import requests
from requests.cookies import RequestsCookieJar
from .DES import base64_encrypt


logger = logging.getLogger(__name__)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class KuwoApi(object, metaclass=Singleton):
    API_BASE: str = 'http://www.kuwo.cn/api/www'
    HTTP_HOST: str = 'http://kuwo.cn'
    MOBI_HOST: str = 'http://mobi.kuwo.cn'
    M_HOST: str = 'http://m.kuwo.cn'
    SEARCH_HOST: str = 'http://search.kuwo.cn'
    token: str
    cookie: RequestsCookieJar

    FORMATS_RATES = {
        'shq': 2000000,
        'hq': 320000,
        'sq': 192000,
        'lq': 128000
    }

    FORMATS_BRS = {
        'shq': '2000kflac',
        'hq': '320kmp3',
        'sq': '192kmp3',
        'lq': '128kmp3'
    }

    FORMATS = {
        'shq': 'AL',
        'hq': 'MP3H',
        'sq': 'MP3192',
        'lq': 'MP3128'
    }

    def __init__(self):
        self.timeout = 30
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Referer': 'http://kuwo.cn',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/81.0.4044.138 Safari/537.36',
            'Host': 'kuwo.cn',
        }
        self.mobi_headers = {'User-Agent': 'okhttp/3.10.0'}
        self.get_cookie_token()
        self.headers['csrf'] = self.token

    def get_cookie_token(self):
        token_uri = KuwoApi.HTTP_HOST + '/search/list?key=hello'
        with requests.Session() as session:
            response = session.get(token_uri, headers=self.headers)
            token = response.cookies.get('kw_token')
            self.token = token
            self.cookie = response.cookies

    def search(self, keyword: str, limit=20, page=1):
        uri = KuwoApi.API_BASE + f'/search/searchMusicBykeyWord?key={keyword}&pn={page}&rn={limit}'
        with requests.Session() as session:
            response = session.get(uri, cookies=self.cookie, headers=self.headers)
            data = response.json()
            return data

    def search_album(self, keyword: str, limit=20, page=1):
        uri = KuwoApi.API_BASE + f'/search/searchAlbumBykeyWord?key={keyword}&pn={page}&rn={limit}'
        with requests.Session() as session:
            response = session.get(uri, cookies=self.cookie, headers=self.headers)
            data = response.json()
            return data

    def search_artist(self, keyword: str, limit=20, page=1):
        uri = KuwoApi.API_BASE + f'/search/searchArtistBykeyWord?key={keyword}&pn={page}&rn={limit}'
        with requests.Session() as session:
            response = session.get(uri, cookies=self.cookie, headers=self.headers)
            data = response.json()
            return data

    def search_playlist(self, keyword: str, limit=20, page=1):
        uri = KuwoApi.API_BASE + f'/search/searchPlayListBykeyWord?key={keyword}&pn={page}&rn={limit}'
        with requests.Session() as session:
            response = session.get(uri, cookies=self.cookie, headers=self.headers)
            data = response.json()
            return data

    def get_song_detail(self, rid: int) -> dict:
        """
        获取歌曲信息
        :param int rid: musicrid
        :return dict 歌曲信息
        """
        uri = KuwoApi.API_BASE + f'/music/musicInfo?mid={rid}'
        with requests.Session() as session:
            response = session.get(uri, cookies=self.cookie, headers=self.headers)
            data = response.json()
            return data

    def get_song_url(self, rid: int):
        uri = KuwoApi.HTTP_HOST + f'/url?format=mp3&rid={rid}&response=url&type=convert_url3&br=128kmp3&from=web&t' \
                                  '=1589364222048'
        with requests.Session() as session:
            response = session.get(uri, cookies=self.cookie, headers=self.headers)
            data = response.json()
            return data

    def get_song_url_mobi(self, rid, quality):
        if quality == 'shq':
            logger.info(f'Querying lossless: {rid} ({quality})')
            formats = 'ape|flac|mp3|aac'
        else:
            logger.info(f'Querying best mp3: {rid} ({quality})')
            formats = 'mp3|aac'
        payload = f'corp=kuwo&p2p=1&type=convert_url2&sig=0&format={formats}&rid={rid}'
        uri = KuwoApi.MOBI_HOST + '/mobi.s?f=kuwo&q=' + base64_encrypt(payload)
        with requests.Session() as session:
            response = session.get(uri, headers=self.mobi_headers)
            return response.text

    def get_album_info(self, aid: int, limit=20, page=1):
        uri = KuwoApi.API_BASE + f'/album/albumInfo?albumId={aid}&pn={page}&rn={limit}'
        with requests.Session() as session:
            response = session.get(uri, cookies=self.cookie, headers=self.headers)
            data = response.json()
            return data

    def get_artist_info(self, aid: int, limit=20, page=1):
        uri = KuwoApi.API_BASE + f'/artist/artist?artistid={aid}&pn={page}&rn={limit}'
        with requests.Session() as session:
            response = session.get(uri, cookies=self.cookie, headers=self.headers)
            data = response.json()
            return data

    def get_playlist_info(self, pid: int, limit=20, page=1):
        uri = KuwoApi.API_BASE + f'/playlist/playListInfo?pid={pid}&pn={page}&rn={limit}'
        with requests.Session() as session:
            response = session.get(uri, cookies=self.cookie, headers=self.headers)
            data = response.json()
            return data

    def get_artist_songs(self, aid: int, limit=20, page=1):
        uri = KuwoApi.API_BASE + f'/artist/artistMusic?artistid={aid}&pn={page}&rn={limit}'
        with requests.Session() as session:
            response = session.get(uri, cookies=self.cookie, headers=self.headers)
            data = response.json()
            return data

    def get_artist_albums(self, aid: int, limit=20, page=1):
        uri = KuwoApi.API_BASE + f'/artist/artistAlbum?artistid={aid}&pn={page}&rn={limit}'
        with requests.Session() as session:
            response = session.get(uri, cookies=self.cookie, headers=self.headers)
            data = response.json()
            return data

    def get_song_mv(self, rid: int):
        uri = KuwoApi.HTTP_HOST + f'/url?rid={rid}&response=url&format=mp4%7Cmkv&type=convert_url&t=1589586895402'
        with requests.Session() as session:
            response = session.get(uri, cookies=self.cookie, headers=self.headers)
            return response.text

    def get_song_lyrics(self, rid: int):
        uri = KuwoApi.M_HOST + f'/newh5/singles/songinfoandlrc?musicId={rid}'
        with requests.Session() as session:
            response = session.get(uri, cookies=self.cookie, headers=self.headers)
            return response.json()
