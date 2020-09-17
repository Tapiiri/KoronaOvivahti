from psycopg2 import sql
from .get_space_id import get_space_id

def door_event_export(conn, space_handle, export_name):
    space_id = get_space_id(conn, space_handle).fetchone()[0]
    export_path = "/tmp/" + export_name
    cur = conn.cursor()
    cur.execute("""
        COPY (
            SELECT 
                user_id,
                users.handle,
                name,
                CASE WHEN in_or_out = 1 THEN 'In' ELSE 'Out' END AS InOrOut,
                created_at,
                spaces.title as Space
            FROM users, doorevents, spaces 
            WHERE 
                user_id = users.id  
                AND space_id = spaces.id
                AND space_id = %(space_id)s

            ) TO %(export_path)s DELIMITER ';' CSV HEADER
        """, {
            "space_id": space_id,
            "export_path": export_path
        }
    )
    return cur

    