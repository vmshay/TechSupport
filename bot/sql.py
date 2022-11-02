def check_id(data):
    sql = f'select tg_id from user_table where tg_id ={data}'
    return sql


def check_approved(data):
    sql = f'select approved from user_table where tg_id ={data}'
    return sql


def send_ticket(data):
    sql = f"insert into tickets (client,category,cab,problem,status,t_date,t_new) values ('{data['tg_id']}'," \
        f"                                                                                '{data['Category']}'," \
        f"                                                                                '{data['cab']}'," \
        f"                                                                                '{data['problem']}'," \
        f"                                                                                '{data['status']}'," \
        f"                                                                                '{data['date']}'," \
        f"                                                                                '{data['t_new']}')"
    return sql


def get_name(data):
    sql = f"select name from users where tg_id = {data}"
    return sql
