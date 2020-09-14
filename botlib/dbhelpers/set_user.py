def set_user(conn, user):
    #user = {handle: str(), name: str()}
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO users (handle, name) 
                        VALUES (%(handle)s, %(name)s);""",
                        user
                    )