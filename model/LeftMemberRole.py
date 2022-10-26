from datetime import datetime

class LeftMemberRole:

    memberID = ""
    roleID = ""
    leftDate = datetime.now()

    def __init__(self, memberID: str, roleID: str, leftDate: datetime):
        self.memberID = memberID
        self.roleID = roleID
        self.leftDate = leftDate
