import os
import sys

from clickhouse_driver import Client
import setting

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def save_clickhouse(item):
    try:
        # connect ClickHouse, No need add port
        client = Client(host=setting.CLICKHOUSE['HOSTNAME'], user=setting.CLICKHOUSE['USERNAME'],
                        database=setting.CLICKHOUSE['DATABASE'])

        # 删除为空和为0的键值对
        for k in list(item.keys()):
            if not item[k]:
                del item[k]
        # 取出keys为字段
        item_keys = ', '.join('`{}`'.format(k) for k in item.keys())
        # 取出values为插入的值
        item_values = ', '.join("'{}'".format(k) for k in item.values())
        product_sql = "insert into `selenium_amazon_product_rank` ({}) values({})".format(item_keys, item_values)

        client.execute(product_sql)
    except Exception as e:
        print("product_sql insert err:", e)
