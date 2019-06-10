from celery import Celery
import time
from flask_socketio import SocketIO
import json
import pandas as pd
import requests
from moviepy.editor import TextClip, CompositeVideoClip, VideoFileClip
import os

# vid_path = '/home/sunny/Projects/flask_celery_socketio/demo/templates/static/assets/videos/sample.mp4'

root = os.path.dirname(os.path.abspath(__file__))
vid_path = os.path.join(root, 'templates', 'static', 'assets', 'videos', 'sample.mp4')
store_path = os.path.join(root, 'downloads', 'videos')

# store_path = '/home/sunny/Projects/flask_celery_socketio/demo/downloads/videos'
request_url = 'http://localhost:5000'

celery=Celery('demo',broker='amqp://admin:mypass@rabbit:5672')

socketio = SocketIO(message_queue='amqp://admin:mypass@rabbit:5672/')

def construct_subclip(index, my_text, video, id):
    ukulele = video
    w,h = moviesize = ukulele.size
    txt = TextClip(my_text, font='Amiri-regular', color='white',fontsize=24)
    txt_col = txt.on_color(size=(ukulele.w + txt.w,txt.h+10), color=(0,0,0), pos=(6,'center'), col_opacity=0.6)
    txt_mov = txt_col.set_pos( lambda t: (max(w/30,int(w-0.5*w*t)), max(5*h/6,int(100*t))) )
    result = CompositeVideoClip([video, txt_mov])
    os.makedirs(store_path + "/session" + str(id), exist_ok=True)
    url = store_path + "/session" + str(id) + "/sample_edited"+ str(index) +".mp4" # Overlay text on video
    result.subclip(0, 10).write_videofile(url) # Many options...
    view_url = request_url + "/videos/" + "/session" + str(id) + "/sample_edited"+ str(index) +".mp4"
    return view_url

def generate_final_video(index, clip1, clip2):
    final_clip = concatenate_videoclips([clip2, clip1], method='compose')
    final_clip.write_videofile("my_concatenation" + str(index) + ".mp4")


def send_message(event, namespace, room, message):
    print(message)
    socketio.emit(event,{'msg':message},namespace=namespace,room=room)

@celery.task
def long_task(n, path, session):
    room=session
    namespace='/long_task'

    pframe = pd.read_csv(path)
    video = VideoFileClip(vid_path).subclip(50,60)
    arr = []
    for i, v in enumerate(list(pframe['name'])):
        h = {'id': ('session' + str(i)), 'name': v, 'url': '','video_generated': False, 'video_sent': False, 'url_enabled': False}
        arr.append(h)
    send_message('msg', namespace, room, json.dumps(arr))

    for i, v in enumerate(arr):
        url = construct_subclip(i, v['name'], video, room)
        v['url'] = url
        v['video_generated'] = True
        v['url_enabled'] = True
        send_message('msg', namespace, room, json.dumps(arr))

