from .get_user_id import get_user_id


def join_space(conn, space_id, tg_id):
    user_id = get_user_id(conn, tg_id).fetchone()[0]
    with conn.cursor() as cur:
        cur.execute("""           
        INSERT INTO doorevents (space_id, user_id, in_or_out) 
                        WITH events_sum AS (
            SELECT COALESCE(SUM(in_or_out),0)
            FROM doorevents 
            WHERE user_id = %(user_id)s
            AND space_id = %(space_id)s
        )     
                        SELECT %(space_id)s, %(user_id)s, 1 WHERE 0 IN (SELECT * FROM events_sum) """,
                    {
                        "space_id": space_id,
                        "user_id": user_id
                    }
                    )
        return cur.rowcount > 0
