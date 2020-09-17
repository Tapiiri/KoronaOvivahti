def upsert_user(conn, user):
    #user = {tg_id: int(), handle: str(), name: str()}
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO users (tg_id, handle, name) 
                        VALUES (%(tg_id)s, %(handle)s, %(name)s)
                        ON CONFLICT (tg_id) 
                        DO UPDATE
                        SET handle=%(handle)s, name=%(name)s;""",
                        user
                    )