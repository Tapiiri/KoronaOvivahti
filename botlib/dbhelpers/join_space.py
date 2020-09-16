from dbhelpers.get_user_id import get_user_id

def join_space(conn, space_id, tg_id):
    user_id = get_user_id(conn, tg_id).fetchone()[0]
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO doorevents (space_id, user_id, in_or_out) 
                        VALUES (%s, %s, %s)""",
                        [space_id, user_id, 1]
                    )