import os
import sys

import pymysql
import setting
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def save_data(item):
    db = pymysql.connect(host=setting.HOSTNAME, user=setting.USERNAME, password=setting.PASSWORD,
                         database=setting.DATABASE,
                         charset='utf8mb4', port=setting.PORT)
    try:
        cursor = db.cursor()
        # 删除为空和为0的键值对
        for k in list(item.keys()):
            if not item[k]:
                del item[k]
        # 取出keys为字段
        item_keys = ', '.join('`{}`'.format(k) for k in item.keys())
        # 取出values为插入的值
        item_values = ', '.join('"{}"'.format(k) for k in item.values())
        product_sql = "insert into `parse_product`({}) values({})".format(item_keys, item_values)
        cursor.execute(product_sql)
        db.commit()
    except Exception as e:
        print("product_sql insert err:", e)
        db.rollback()
