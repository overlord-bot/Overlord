from enum import Enum

class CMD(Enum):

    # getting enums require unique values so ONLY THE LAST DIGIT of each enum 
    # represents their actual value (number of arguments needed).
    ADD = 12
    REMOVE = 22
    SCHEDULE = 11
    PRINT = 10
    FULFILLMENT = 20
    DEGREE = 21
    FIND = 31
    DETAILS = 41

    TEST = 30
    IMPORT = 40

    TAG = 101 # tags all responses with given id

    NONE = 50

    def get(string:str):
        try:
            enum = CMD[string.upper()]  
        except Exception as e:
            enum = CMD.NONE
        return enum

class Command():

    def __init__(self, command:str):
        self.command = CMD.get(command)
        self.arguments = []
        self.data_store = None

    """ True means valid command, the last digit of the enum value
        represents the number of arguments required
    """
    def valid(self) -> bool:
        return self.command.value % 10 <= len(self.arguments)

    def __len__(self):
        return len(self.arguments) + 1

    def __repr__(self):
        return f"{', '.join([str(self.command)] + self.arguments)}"

    def __eq__(self, other):
        if not isinstance(other, Command):
            return False
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))