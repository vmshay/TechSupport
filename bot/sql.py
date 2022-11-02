def check_id(data):
    sql = f'select tg_id from user_table where tg_id ={data}'
    return sql


def check_approved(data):
    sql = f'select approved from user_table where tg_id ={data}'
    return sql
