import sqlite3


def checkCurator(userId):
    conn = sqlite3.connect('sqlite_db.sqlite', check_same_thread=False)
    cursor = conn.cursor()
    sql_select_query = '''SELECT * FROM curators WHERE id = ?'''
    cursor.execute(sql_select_query, (userId,))
    result = cursor.fetchone()
    return result is not None


def getNextProblem(userId):
    conn = sqlite3.connect('sqlite_db.sqlite', check_same_thread=False)
    cursor = conn.cursor()
    sql_select_query = '''SELECT *
                            FROM problems
                           WHERE curator_id is null
                              or curator_id = ?
                           ORDER BY id'''
    cursor.execute(sql_select_query, (userId,))
    problem = cursor.fetchone()
    if problem is None:
        return None

    req = "UPDATE problems SET curator_id = ? WHERE id = ?"
    cursor.execute(req, (userId, problem[0]))
    conn.commit()
    return problem


def getCurrentProblem(userId):
    conn = sqlite3.connect('sqlite_db.sqlite', check_same_thread=False)
    cursor = conn.cursor()
    sql_select_query = '''SELECT *
                            FROM problems
                           WHERE curator_id = ?
                           ORDER BY id'''
    cursor.execute(sql_select_query, (userId,))
    return cursor.fetchone()


def delCurrentProblem(problemId):
    conn = sqlite3.connect('sqlite_db.sqlite', check_same_thread=False)
    cursor = conn.cursor()
    req = "DELETE FROM problems WHERE id = ?"
    cursor.execute(req, (problemId,))
    conn.commit()
