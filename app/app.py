from flask import Flask, render_template, request
from database import get_manual, get_yt_videos


app = Flask(__name__)


@app.route('/<id>/home')
def home(id):
    # fetch manual'data for id
    manual = get_manual(id)
    ID = manual[0]
    TITLE = manual[1]
    METADATA = manual[2]
    LINK = manual[3]

    mp = {'id': ID, 'title': TITLE, 'meta': METADATA, 'link': LINK}

    # fetch youtube videos for id's metadata
    videos = get_yt_videos(mp['meta'])

    return render_template('index.html', manual=mp, videos=videos)


@app.route('/<id>/chat')
def chat(id):
    pass


if __name__ == '__main__':
    app.run(debug=True)
