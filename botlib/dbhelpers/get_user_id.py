def get_user_id(conn, tg_id):
    #tg_id = int()
    cur = conn.cursor()
    cur.execute("""SELECT (id) FROM users WHERE tg_id = %(tg_id)s;""",
                    {"tg_id": tg_id}
                )
    return cur