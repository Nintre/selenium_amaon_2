from clickhouse_driver import Client


def get_keywords(batch_size, n):
    # connect ClickHouse, No need add port
    client = Client(host='192.168.50.50', user='default', database='test')

    sql_select = 'select DISTINCT search_term from brand_analytics_search_terms_reports order by search_term limit {} offset {}'.format(batch_size, n)
    data_list = client.execute(sql_select)
    for i in range(len(data_list)):
        data_list[i] = (data_list[i][0])

    return data_list
