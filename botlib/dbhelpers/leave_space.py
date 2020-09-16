from dbhelpers.get_user_id import get_user_id

def leave_space(conn, space_id, tg_id):
    user_id = get_user_id(conn, tg_id).fetchone()[0]
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO doorevents (space_id, user_id, in_or_out) 
                        VALUES (%(space_id)s, %(user_id)s, %(in_or_out)s) IF (
                            SELECT SUM(in_or_out) 
                            FROM doorevents 
                            WHERE user_id = %(user_id)s
                            AND space_id = %(space_id)s
                        )""",
                        [space_id, user_id, -1]
                    )