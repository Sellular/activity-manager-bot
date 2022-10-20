from utils import DBUtils
from model import ChannelMessage

__channelMessageSelectByCodeSql = """
    SELECT * FROM channel_messages
    WHERE message_code = ?;
"""

__channelMessageDeleteByCodeSql = """
    DELETE FROM channel_messages
    WHERE message_code = ?;
"""

__channelMessageUpdateSql = """
    UPDATE channel_messages
    SET message_id = ?
    WHERE message_code = ?;
"""

__channelMessageInsert = """
    INSERT OR IGNORE INTO channel_messages (
        message_id,
        message_code
    ) VALUES (
        ?,
        ?
    );
"""

def getChannelMessageByCode(messageCode: str):
    try:
        dbConnection = DBUtils.getDBConnection()

        with dbConnection:
            dbCursor = dbConnection.execute(
                __channelMessageSelectByCodeSql, (messageCode,))
            
            row = dbCursor.fetchone()

            role = None
            if row:
                role = ChannelMessage(
                    row['message_id'],
                    row['message_code']
                )
            return role
    except (Exception) as error:
        raise error

def insert(messageID: int, messageCode: str):
    try:
        dbConnection = DBUtils.getDBConnection()

        with dbConnection:
            dbConnection.execute(
                __channelMessageInsert, (messageID, messageCode))
            dbConnection.commit()
    except (Exception) as error:
        raise error

def deleteChannelMessageByCode(messageCode: str):
    try:
        dbConnection = DBUtils.getDBConnection()

        with dbConnection:
            dbConnection.execute(
                __channelMessageDeleteByCodeSql, (messageCode,))
            dbConnection.commit()
    except (Exception) as error:
        raise error

def updateChannelMessage(messageID: int, messageCode: str):
    try:
        dbConnection = DBUtils.getDBConnection()

        with dbConnection:
            dbConnection.execute(
                __channelMessageUpdateSql, (messageID, messageCode))
            dbConnection.commit()
    except (Exception) as error:
        raise error