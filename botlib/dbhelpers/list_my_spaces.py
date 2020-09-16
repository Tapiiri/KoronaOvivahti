from .list_spaces import list_spaces
from .get_user_id import get_user_id

def list_my_spaces(conn, fields, tg_id):
    user_id = get_user_id(conn, tg_id).fetchone()[0]
    return list_spaces(conn, fields, params={"owner_id":user_id})

