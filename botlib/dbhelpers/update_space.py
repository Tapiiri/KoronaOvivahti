def update_space(conn, space):
    #space = {title: str(), owner: int(), date: datetime.datetime.now()}
    cur = conn.cursor()
    cur.execute("""UPDATE spaces 
                    SET 
                        title=%(title)s,
                        handle=%(handle)s,
                        date=%(date)s
                    WHERE
                        id=%(id)s;""",
                    space
                )
    return cur.rowcount > 0