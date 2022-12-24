from pypresence import Presence
from yandex_music import Client
#import yandex_music
from config import *
import time
import os
import threading
import sys

import win32gui
import win32con
from SysTray import SysTrayIcon

def bye(sysTrayIcon):
    RPC.clear()
    sys.exit(1)

def hide(sysTrayIcon):
    RPC.clear()
    global RPCSTATUS
    RPCSTATUS = False

def show(sysTrayIcon):
    global RPCSTATUS
    RPCSTATUS = True
    mp = threading.Thread(target=music)
    mp.daemon = True
    mp.start()

TOKEN = token

client_id = discord_application

RPC = Presence(client_id=client_id)
RPC.connect()

client = Client(TOKEN).init()

def plus():
    if client.me.plus.has_plus: return "Плюс активирован!"
    else: return "Плюс не активирован"

def plusimg():
    if client.me.plus.has_plus: return "https://yastat.net/s3/plus/landing/2022/icons/rebrand/apple-touch-icon-180x180.png"
    else: return "https://assets.stickpng.com/images/5897a8c3cba9841eabab6156.png"

def music():
    while RPCSTATUS:
        try:
            queues = client.queues_list()
            last_queue = client.queue(queues[0].id)
            last_track_id = last_queue.get_current_track()
            last_track = last_track_id.fetch_track()
            artists = ', '.join(last_track.artists_name())
            title = last_track.title
            track_link = f"https://music.yandex.ru/album/{last_track['albums'][0]['id']}/track/{last_track['id']}/"
            image_link="https://" + last_track.cover_uri.replace("%%", "1000x1000")
            btns = [
                    { 
                "label": "Слушать Трек",
                "url": track_link
                    }
            ]

            RPC.update(
                details="Слушает: " + title,
                state="Исполнитель: " + artists,
                large_image=image_link,
                large_text="Че ты на меня наводишь свой грязный кусрсор?!??!?",
                buttons=btns,
                small_image=plusimg(),
                small_text=plus()
            )
        except:
            RPC.update(
            details='Поддерживаются только треки из плейлистов',
            state='Ну что мне поделать с яндексом',
            large_image='https://media.tenor.com/S7SLFLHTy-wAAAAC/uh-sorry.gif',
            large_text="Яндекс музыка не дает получить трек не из плейлиста xD",
            small_image=plusimg(),
            small_text=plus()
            )
    
        time.sleep(5)

def main():
    icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon_main.ico")
    hover_text = "Yandex Music RPC"
    menu_options = (("Show status", None, show), ("Hide status", None, hide))
    mp = threading.Thread(target=music)
    mp.daemon = True
    mp.start()
    SysTrayIcon(icon, hover_text, menu_options, on_quit=bye, default_menu_index=1)


if __name__ == "__main__":
    RPCSTATUS = True
    main()
