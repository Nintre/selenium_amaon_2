from clickhouse_driver import Client


def save_clickhouse(item):
    try:
        # connect ClickHouse, No need add port
        client = Client(host='192.168.50.50', user='default', database='test')

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
