# encoding = utf-8


class ChatRoom(object):

    def __init__(self, _name, _database=[], _member=[]):
        self._name = _name
        self._database = _database
        self._member = _member

    def __str__(self):
        return str(ChatRoom.data2dict(self))

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, value):
        self._database = value

    @property
    def member(self):
        return self._member

    @member.setter
    def member(self, value):
        self._member = value

    @staticmethod
    def data2dict(chat_room):
        return {
            "name": chat_room.name,
            "database": chat_room.database,
            "member": chat_room.member
        }


if __name__ == "__main__":
    pass
