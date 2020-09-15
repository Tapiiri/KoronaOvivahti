from psycopg2 import sql

def list_spaces(conn, fields=[], params={}):
    #space = {title: str(), owner: int(), date: datetime.datetime.now()}
    cur = conn.cursor()
    
    fields_string = "("
    for val in fields:
        fields_string += f"{val},"
    fields_string = fields_string[:-1]
    fields_string += ")"

    params_string = " "
    for key in params:
        param = "{}='{}',".format(key, params[key])
        params_string += param
    params_string = params_string[:-1]
    
    cur.execute(
        sql.SQL("""
            SELECT {} FROM spaces {};
            """.format(
                fields and fields_string or "*",
                params and "WHERE " + params_string
                or ""
            ))
    )
    return cur