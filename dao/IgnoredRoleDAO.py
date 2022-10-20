from utils import DBUtils

__ignoredRolesSelectSql = """
    SELECT * FROM ignored_roles;
"""

__ignoredRolesDeleteByRoleSql = """
    DELETE FROM ignored_roles
    WHERE role_id = ?;
"""

__ignoredRoleInsertSql = """
    INSERT OR IGNORE INTO ignored_roles (
        role_id
    ) VALUES (
        ?
    );
"""


def getIgnoredRoles():
    try:
        dbConnection = DBUtils.getDBConnection()

        with dbConnection:
            dbCursor = dbConnection.execute(
                __ignoredRolesSelectSql)

            rows = dbCursor.fetchall()

            ignored_roles = []
            for row in rows:
                ignored_roles.append(int(row['role_id']))

            return ignored_roles

    except Exception as error:
        raise error

def deleteIgnoredRoleById(ignored_role_id: int):
    try:
        dbConnection = DBUtils.getDBConnection()

        with dbConnection:
            dbConnection.execute(
                __ignoredRolesDeleteByRoleSql, (ignored_role_id,))
            dbConnection.commit()

    except Exception as error:
        raise error

def insert(ignore_role_id: int):
    try:
        dbConnection = DBUtils.getDBConnection()

        with dbConnection:
            dbConnection.execute(
                __ignoredRoleInsertSql, (ignore_role_id,))
    except Exception as error:
        raise error