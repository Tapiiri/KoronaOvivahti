def with_conn(handler_callback):

    def with_conn_wrapper(update, context, *args, **kwargs):
        try:
            pool = context.bot_data["pool"]
            with pool.getconn() as conn:
                return handler_callback(update, context, conn)
        finally:
            pool.putconn(conn)

    return with_conn_wrapper