from sqlalchemy import create_engine
from sqlalchemy.sql import text
import os
from dotenv import load_dotenv
import requests

load_dotenv()

USER = 'avnadmin'
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = 16947
DATABASE = 'defaultdb'
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API')


def get_connection():
    return create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")


def get_manual(id: int):
    engine = get_connection()
    query = text(
        '''
            SELECT *
            FROM Manuals
            WHERE id = :id
        '''
    )
    with engine.connect() as connection:
        result = connection.execute(query, {'id': id})
        data = tuple(result.fetchone())
        return data


def get_yt_videos(query: str):
    MAX_RESULTS = 3  # thala for a reason!
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults={MAX_RESULTS}&key={YOUTUBE_API_KEY}'
    response = requests.get(url)
    data = response.json()

    videos = []
    for item in data.get('items', []):
        id = item['id']['videoId']
        title = item['snippet']['title']
        url = f"https://www.youtube.com/embed/{id}"
        videos.append({'title': title, 'url': url})
    return videos


if __name__ == '__main__':
    try:
        engine = get_connection()
        print('Success')
    except Exception as e:
        print('Not', e)
