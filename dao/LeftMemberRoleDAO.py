from utils import DBUtils
from model import LeftMemberRole

__leftMemberRoleSelectByMemberSql = """
    SELECT * FROM left_members
    WHERE member_id = ?;
"""

__leftMemberRoleInsertSql = """
    INSERT OR IGNORE INTO left_members (
        member_id,
        role_id,
        left_date
    ) VALUES (
        ?,
        ?,
        ?
    )
"""

__leftMemberRoleDeleteByMemberSql = """
    DELETE FROM left_members
    WHERE member_id = ?;
"""

def getLeftMemberRolesByMember(memberID: str):
    try:
        dbConnection = DBUtils.getDBConnection()

        with dbConnection:
            dbCursor = dbConnection.execute(
                __leftMemberRoleSelectByMemberSql, (memberID,))
            
            rows = dbCursor.fetchall()

            roles = []
            for row in rows:
                roles.append(LeftMemberRole(
                    row['member_id'],
                    row['role_id'],
                    row['left_date']
                ))

            return roles
    except (Exception) as error:
        raise error


def insertMany(role_member_list: list):
    try:
        dbConnection = DBUtils.getDBConnection()

        with dbConnection:
            dbConnection.executemany(
                __leftMemberRoleInsertSql, role_member_list)
            dbConnection.commit()
    except (Exception) as error:
        raise error


def deleteLeftMemberRolesByMember(memberID: str):
    try:
        dbConnection = DBUtils.getDBConnection()

        with dbConnection:
            dbConnection.execute(
                __leftMemberRoleDeleteByMemberSql, (memberID,))
            dbConnection.commit()
    except (Exception) as error:
        raise error