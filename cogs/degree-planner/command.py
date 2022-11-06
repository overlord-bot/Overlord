from enum import Enum

class CMD(Enum):
    ADD = 1
    REMOVE = 2
    SCHEDULE = 3
    PRINT = 4
    FULFILLMENT = 5
    DEGREE = 6
    FIND = 7

    TEST = 10
    IMPORT = 11

    NONE = 100

    def get(string:str):
        try:
            enum = CMD[string.upper()]  
        except Exception as e:
            enum = CMD.NONE
        return enum

class Command():

    def __init__(self, command:str):
        self.command = CMD.get(command)
        if self.command == CMD.NONE:
            print("error creating command: command not found")
        self.arguments = []
        self.data_store = None

    def __len__(self):
        return len(self.arguments) + 1

    def __repr__(self):
        return f"{'+'.join([str(self.command)] + self.arguments)}"

    def __eq__(self, other):
        if not isinstance(other, Command):
            return False
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))