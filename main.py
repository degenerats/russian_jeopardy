import asyncio
import tornado.websocket
import tornado.escape
import tornado.ioloop
import tornado.locks
import tornado.web
import os.path
import uuid
import json
import random
import string
import datetime

from tornado.options import define, options, parse_command_line

import settings
from auth import AuthHandler

auth_handler = AuthHandler()

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


class RoomManager(object):
    def __init__(self):
        self.cond = tornado.locks.Condition()
        self.rooms = {}
        self.room_limit = settings.ROOM_LIMIT

    def _generate_room_key(self):
        chars = string.ascii_letters + string.digits
        random.seed(datetime.datetime.now().timestamp())
        return ''.join(random.choice(chars) for _ in range(settings.ROOM_KEY_LENGTH))

    def room_exists(self, room_id):
        return room_id in self.rooms

    def add_to_room(self, room_id, user_id, username):
        self.rooms[room_id]['users'][user_id] = {
            'username': username
        }

    def is_full(self, room_id):
        room = self.rooms[room_id]
        return len(room['users']) >= settings.ROOM_USER_LIMIT

    def belongs_to_room(self, room_id, user_id):
        room = self.rooms[room_id]
        return user_id in room['users']

    def get_messages(self, room_id):
        return self.rooms[room_id]['messages']

    def create_room(self, user_id=None):
        if len(self.rooms) >= self.room_limit:
            raise Exception('Превышено максимальное количество комнат')

        if user_id is None:
            user_id = auth_handler.create_token()
        room_key = self._generate_room_key()

        self.rooms[room_key] = {
            'messages': [],
            'author': user_id,
            'users': {}
        }
        self.cond.notify_all()
        return {
            'room_id': room_key,
            'user_id': user_id
        }


room_manager = RoomManager()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class CreateHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            data = room_manager.create_room()
        except Exception as e:
            self.write(json.dumps({'success': False, 'error': str(e)}))
        else:
            data['success'] = True
            self.write(json.dumps(data))
        self.finish()


class RoomHandler(tornado.web.RequestHandler):
    def get(self, room_id):
        if room_manager.room_exists(room_id):
            self.render("room.html", room_id=room_id)


class RoomJoinHandler(tornado.web.RequestHandler):
    def add_anonymous_to_room(self, username):
        self.user_id = auth_handler.create_token()
        room_manager.add_to_room(self.room_id, self.user_id, username)

    def get_username(self):
        username = self.request.arguments.get('username')
        if username and len(username) and username[0]:
            return username[0]
        return None

    def add_to_room(self):
        if room_manager.belongs_to_room(self.room_id, self.user_id):
            return self.success()
        else:
            username = self.get_username()
            if username:
                self.add_anonymous_to_room(username)
                return self.success()
            elif room_manager.is_full(self.room_id):
                return self.fail('room_is_full')
            else:
                return self.fail('username_required')

    def check_token(self):
        user_id = self.request.headers['Authentication']
        if user_id.startswith('Token ') and user_id[6:]:
            user_id = user_id[6:]
        else:
            user_id = None
        self.user_id = user_id

    def get(self, room_id):
        self.room_id = room_id
        self.check_token()

        if room_manager.room_exists(self.room_id):
            if room_manager.belongs_to_room(self.room_id, self.user_id):
                return self.success()
            else:
                return self.add_to_room()
        else:
            return self.fail('room_does_not_exists')

    def fail(self, error):
        self.write(json.dumps({'success': False, 'error_code': error}))
        self.finish()
        return

    def success(self):
        self.write(json.dumps({
            'success': True,
            'user_id': self.user_id,
            'messages': room_manager.get_messages(self.room_id)
        }))
        self.finish()
        return


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = {}

    def get_token(self):
        token = self.request.arguments.get('token')
        if token and len(token) and token[0]:
            return token[0]
        return None

    def open(self, room_id):
        self.token = self.get_token()
        self.room_id = room_id
        if self.token in ChatSocketHandler.waiters:
            ChatSocketHandler.waiters[self.token].append(self)
        else:
            ChatSocketHandler.waiters[self.token] = [self]

    # def on_close(self):
    #     ChatSocketHandler.waiters[self.token]
    #     ChatSocketHandler.waiters.remove(self)
    #
    # @classmethod
    # def addMessage(cls, chat):
    #     cls.cache.append(chat)
    #     if len(cls.cache) > cls.cache_size:
    #         cls.cache = cls.cache[-cls.cache_size:]
    #
    # @classmethod
    # def send_updates(cls, chat):
    #     for waiter in cls.waiters:
    #         try:
    #             waiter.write_message(chat)
    #         except:
    #             pass
    #
    # def on_message(self, message):
    #     parsed = tornado.escape.json_decode(message)
    #     chat = {
    #         "id": str(uuid.uuid4()),
    #         "body": parsed["body"],
    #     }
    #     chat["html"] = tornado.escape.to_basestring(
    #         self.render_string("message.html", message=chat))
    #
    #     ChatSocketHandler.addMessage(chat)
    #     ChatSocketHandler.send_updates(chat)


def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/create", CreateHandler),
            (r"/room/(\w+)", RoomHandler),
            (r"/room/(\w+)/join", RoomJoinHandler),
            (r"/room/(\w+)/connect", ChatSocketHandler),
        ],
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
        debug=options.debug,
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
