import os
import sys
import setting
from clickhouse_driver import Client

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_keywords(batch_size, n):
    try:
        # connect ClickHouse, No need add port
        client = Client(host=setting.CLICKHOUSE['HOSTNAME'], user=setting.CLICKHOUSE['USERNAME'],
                        database=setting.CLICKHOUSE['DATABASE'])

        sql_select = "select DISTINCT search_term from brand_analytics_search_terms_reports where department_name='Amazon.com' order by search_term limit {} offset {}".format(
            batch_size, n)
        data_list = client.execute(sql_select)
        for i in range(len(data_list)):
            data_list[i] = (data_list[i][0])

        return data_list
    except Exception as e:
        print('get_keywords fun err or connect clickhouse err:', e)
