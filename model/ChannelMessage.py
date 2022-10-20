
class ChannelMessage:

    messageID = 0
    messageCode = ''

    def __init__(self, messageID: int, messageCode: str):
        self.messageID = messageID
        self.messageCode = messageCode