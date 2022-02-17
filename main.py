import multiprocessing
import os
import sys
import time

from selenium.webdriver.support.select import Select

import control
import get_search_item
import parse_product
import setting

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

url = setting.BASE_URL
postal = setting.POSTAL
batch_size = setting.KEYWORDS_LIST_SIZE
pool_size = setting.PROCESS_POOL_SIZE

# 15
# data_list = ['phone', 'book', 'computer', 'tree', 'cat', 'dog', 'food', 'basketball', 'fishing', 'golf', 'hunting', 'gift',
#                  'bag', 'football', 'ping pang']


def main():
    n = 0
    while True:
        data_list = get_search_item.get_keywords(batch_size, n)
        if len(data_list) == 0:
            print("爬取结束")
            break
        print('大小为{},值为{}'.format(len(data_list), data_list))
        n += batch_size

        queue = multiprocessing.Manager().Queue()
        for keyword in data_list:
            queue.put(keyword)

        # print('queue 开始大小 %d' % queue.qsize())

        # 异步进程池(非阻塞)
        pool = multiprocessing.Pool(pool_size)
        for index in range(queue.qsize()):
            pool.apply_async(process_one, args=(queue,))
            # time.sleep(1)
        pool.close()
        pool.join()
        queue.join()


def process_one(in_queue):
    driver = control.get_driver()
    driver.get(url)
    control.change_address(driver, postal)
    while in_queue.empty() is not True:
        if driver.find_element_by_id('nav-search-label-id').get_attribute('textContent') != 'All':
            print("all click select err")
            Select(driver.find_element_by_id('searchDropdownBox')).select_by_visible_text('All Departments')

        keywords = in_queue.get()
        # print(keywords)
        control.search_keywords(driver, keywords)

        parse_product.get_product_list(driver, keywords)

        # time.sleep(5)
        # driver.close()

        in_queue.task_done()


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print((end - start))
