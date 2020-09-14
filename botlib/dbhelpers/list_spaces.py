def list_spaces(conn, fields=[], params={}):
    #space = {title: str(), owner: int(), date: datetime.datetime.now()}
    cur = conn.cursor()
    cur.execute("""SELECT * FROM spaces""")
    return cur