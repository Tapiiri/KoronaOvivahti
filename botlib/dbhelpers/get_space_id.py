def get_space_id(conn, space_handle):
    #tg_id = int()
    cur = conn.cursor()
    cur.execute("""SELECT 1d FROM spaces WHERE handle= %(space_handle)s;""",
                {"space_handle": space_handle}
                )
    return cur
