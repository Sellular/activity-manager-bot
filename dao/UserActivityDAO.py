from utils import DBUtils
from model.UserActivity import UserActivity

from datetime import datetime

__userActivitySelectByActiveSql = """
    SELECT * FROM user_activity
    WHERE is_active = ?;
"""

__userActivitySelectByMembersSql = """
    SELECT * FROM user_activity
    WHERE member_id = {0};
"""

__userActivityUpsertSql = """
    INSERT INTO user_activity (
        member_id,
        active_timestamp
    ) VALUES (
        ?,
        ?
    ) ON CONFLICT(member_id) DO
        UPDATE SET 
            active_timestamp = excluded.active_timestamp
    ;
"""

__userActivityInsertSql = """
    INSERT OR IGNORE INTO user_activity (
        member_id,
        active_timestamp
    ) VALUES (
        ?,
        ?
    );
"""

__userActivitySetActiveSql = """
    UPDATE user_activity
    SET 
        active_timestamp = ?,
        is_active = 1
    WHERE member_id = ?;
"""

__userActivitySetInactiveSql = """
    UPDATE user_activity
    SET is_active = 0
    WHERE member_id = ?;
"""

__userActivityDeleteSql = """
    DELETE FROM user_activity
    WHERE member_id = ?;
"""


def getUserActivityByActive(isActive: bool):
    try:
        dbConnection = DBUtils.getDBConnection()

        with dbConnection:
            dbCursor = dbConnection.execute(
                __userActivitySelectByActiveSql, (1 if isActive else 0,))

            rows = dbCursor.fetchall()

            activities = []
            for row in rows:
                activities.append(UserActivity(
                    row['member_id'],
                    datetime.fromisoformat(row['active_timestamp']),
                    row['is_active'] == 1
                ))

            return activities

    except Exception as error:
        raise error


def getUserActivityByMembers(member_id_list: list):
    try:
        dbConnection = DBUtils.getDBConnection()

        with dbConnection:
            sql = __userActivitySelectByMembersSql.format(
                ', '.join('?' for _ in member_id_list))
            dbCursor = dbConnection.execute(
                sql, member_id_list)

            rows = dbCursor.fetchall()

            activities = []
            for row in rows:
                activities.append(UserActivity(
                    row['member_id'],
                    datetime.fromisoformat(row['active_timestamp']),
                    row['is_active'] == 1
                ))

            return activities
    except Exception as error:
        raise error


def upsertMany(user_activity_list: list):
    try:
        dbConnection = DBUtils.getDBConnection()

        with dbConnection:
            dbConnection.executemany(
                __userActivityUpsertSql, user_activity_list)
    except Exception as error:
        raise error

def insertMany(user_activity_list: list):
    try:
        dbConnection = DBUtils.getDBConnection()

        with dbConnection:
            dbConnection.executemany(
                __userActivityInsertSql, user_activity_list)
    except Exception as error:
        raise error

def userActivitySetActive(memberID: int, activeTimestamp: datetime):
    try:
        dbConnection = DBUtils.getDBConnection()

        with dbConnection:
            dbConnection.execute(
                __userActivitySetActiveSql, (str(activeTimestamp), memberID))
    except Exception as error:
        raise error


def userActivitySetManyInactive(member_id_list: list):
    try:
        dbConnection = DBUtils.getDBConnection()

        with dbConnection:
            dbConnection.executemany(
                __userActivitySetInactiveSql, member_id_list)
    except Exception as error:
        raise error

def deleteUserActivityByMember(memberID: str):
    try:
        dbConnection = DBUtils.getDBConnection()

        with dbConnection:
            dbConnection.execute(
                __userActivityDeleteSql, (memberID,))
            dbConnection.commit()
    except Exception as error:
        raise error
