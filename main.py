import os
import random
import vk_api

from vk_api import VkUpload
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from create_image import make_image_file, make_image_web
from database_utils import database, add_photos, clear_photos, ignor, change_name, change_audio
from config import TOKEN, GROUP_ID

try:
    TOKEN = os.environ['ACCESS_TOKEN']
    GROUP_ID = os.environ['GROUP_ID']
except KeyError:
    pass

vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)
upload = VkUpload(vk_session)
vk = vk_session.get_api()


def main():
    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:

            print(event.message)

            msg_rec = event.message.text
            from_id = str(event.message['from_id'])
            if msg_rec.startswith("!photo") or msg_rec.startswith("!фото"):
                try_func(
                    add_photos(event),
                    event
                )
            elif msg_rec.startswith("!clear") or msg_rec.startswith("!оч"):
                try_func(
                    clear_photos(event),
                    event
                )
            elif msg_rec.startswith("!ignor") or msg_rec.startswith("!игнор"):
                try_func(
                    ignor(event),
                    event
                )
            elif msg_rec.startswith("!name") or msg_rec.startswith("!имя"):
                try_func(
                    change_name(event),
                    event
                )
            elif msg_rec.startswith("!audio") or msg_rec.startswith("!аудио"):
                try_func(
                    change_audio(event),
                    event
                )
            elif from_id in database and not database[from_id].get("ignor", False):
                attachments = []

                audio = database[from_id].get("audio", None)
                images_lst = database[from_id].get("images", [])
                links_lst = database[from_id].get("links", [])

                if audio:
                    attachments.append(audio)
                if links_lst or images_lst:
                    if images_lst:
                        image = random.choice(images_lst)
                        make_image_file(msg_rec, image)
                    if links_lst:
                        image = random.choice(links_lst)
                        make_image_web(msg_rec, image)
                    photo = upload.photo_messages(photos=f"temp_images/tmp.jpg")[0]
                    attachments.append(
                        f"photo{photo['owner_id']}_{photo['id']}"
                    )
                if attachments:
                    vk.messages.send(
                        random_id=get_random_id(),
                        attachment=attachments,
                        chat_id=event.chat_id,
                    )


def report_bug(event, error):
    vk.messages.send(
        random_id=get_random_id(),
        message=f"Произошла ошибка {error}",
        chat_id=event.chat_id,
    )


def try_func(func, event):
    try:
        func
    except Exception as e:
        report_bug(event, e)


if __name__ == "__main__":
    main()
