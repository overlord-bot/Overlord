from enum import Enum

class Permission(Enum):
    CMD_ADD = 12
    CMD_REMOVE = 22
    CMD_SCHEDULE = 11
    CMD_PRINT = 10
    CMD_FULFILLMENT = 20
    CMD_DEGREE = 21
    CMD_FIND = 31

    CMD_TEST = 30
    CMD_IMPORT = 40

# one permissions object per user

class Permissions():

    def __init__(self):
        # stores {server/server+channel:permissions granted}
        self.__permissions = dict()