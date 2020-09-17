from psycopg2 import sql

def list_spaces(conn, fields=[], params={}):
    #space = {title: str(), owner: int(), date: datetime.datetime.now()}
    cur = conn.cursor()
    
    fields_list = []
    for val in fields:
        fields_list.append(sql.Identifier(val))
    fields_string = sql.SQL(',').join(fields_list)

    params_key_list = []
    params_value_list = []
    for key in params:
        params_key_list.append(key)
        params_value_list.append(params[key])
    params_string = sql.SQL("").join([
        sql.SQL("WHERE "), 
        sql.SQL(",").join([
            sql.SQL("=").join([
                sql.Identifier(key), sql.Placeholder()
                ]) for key in params_key_list        
            ])
        ])
    
    cur.execute(
        sql.SQL("""
            SELECT {} FROM spaces {};
            """).format(
                fields and fields_string or sql.SQL("*"),
                params and params_string or sql.SQL("")
            ), params_value_list
    )
    return cur