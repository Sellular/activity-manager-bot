import sqlite3

__userActivityTableSql = """
    CREATE TABLE IF NOT EXISTS user_activity (
        member_id           TEXT    NOT NULL    PRIMARY KEY,
        active_timestamp    TEXT    NOT NULL,
        is_active           INTEGER NOT NULL    DEFAULT 1
    );
"""

__channelMessageTableSql = """
    CREATE TABLE IF NOT EXISTS channel_messages (
        message_id      INTEGER NOT NULL,
        message_code    TEXT    NOT NULL    PRIMARY KEY
    );
"""

_ignoredRoleTableSql = """
    CREATE TABLE IF NOT EXISTS ignored_roles (
        role_id     INTEGER NOT NULL    PRIMARY KEY
    );
"""


def getDBConnection():
    dbConnection = None
    try:
        dbConnection = sqlite3.connect('pycord.db')
        dbConnection.row_factory = sqlite3.Row

        return dbConnection
    except (Exception) as error:
        if dbConnection:
            dbConnection.close()
        raise error


def checkTables():
    dbConnection = getDBConnection()

    try:
        dbCursor = dbConnection.cursor()
        tableCommands = (__userActivityTableSql, __channelMessageTableSql)

        for command in tableCommands:
            dbCursor.execute(command)

        dbConnection.commit()
        dbCursor.close()
    except (Exception) as error:
        raise error
    finally:
        if dbConnection:
            dbConnection.close()
