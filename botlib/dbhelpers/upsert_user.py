def upsert_user(conn, user):
    #user = {id: int(), handle: str(), name: str()}
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO users (id, handle, name) 
                        VALUES (%(id)s, %(handle)s, %(name)s)
                        ON CONFLICT (id) 
                        DO UPDATE
                        SET handle=%(handle)s, name=%(name)s;""",
                        user
                    )