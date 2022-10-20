from datetime import datetime, timezone


class UserActivity:

    memberID = 0
    activeTimestamp = datetime.now(timezone.utc)
    isActive = True

    def __init__(self, memberID: int, activeTimestamp: datetime, isActive: bool):
        self.memberID = memberID
        self.activeTimestamp = activeTimestamp
        self.isActive = isActive
