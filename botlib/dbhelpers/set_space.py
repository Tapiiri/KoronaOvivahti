def set_space(conn, space):
    #space = {title: str(), owner: int(), date: datetime.datetime.now()}
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO spaces 
                        (title, handle, owner_id, date) 
                        VALUES (
                            %(title)s,
                            %(handle)s,
                            %(owner_id)s,
                            %(date)s);""",
                        space
                    )