import os
import re
import sys
from pymysql.converters import escape_string
import save_mysql
import save_clickhouse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def parse_title(driver, asin):
    title = ''
    try:
        title = driver.find_element_by_xpath('//div[@data-asin="{}"]//span[@class="a-size-medium a-color-base a-text-normal" or @class="a-size-base-plus a-color-base a-text-normal"]'.format(asin)).get_attribute('textContent')
    except Exception as e:
        print("parse_title err:", e)
    return title


def parse_image(driver, asin):
    image = ''
    try:
        image = driver.find_element_by_xpath('//div[@data-asin="{}"]//img[@class="s-image"]'.format(asin)).get_attribute('src')
    except Exception as e:
        print("parse_image err:", e)
    return image


def parse_stars(driver, asin):
    stars = 0
    try:
        stars = driver.find_element_by_xpath('//div[@data-asin="{}"]//span[@class="a-icon-alt"]'.format(asin))
        if stars is not None:
            stars = stars.get_attribute('textContent')
            stars = re.findall('(.*?) out of 5 stars', stars)[0]
            stars = float(stars)

    except Exception as e:
        # print("parse_stars err:", e)
        pass
    return stars


def parse_ratings(driver, asin):
    ratings = 0
    try:
        ratings = driver.find_element_by_xpath('//div[@data-asin="{}"]//span[@class="a-size-base s-underline-text"]'.format(asin))
        if ratings is not None:
            ratings = ratings.get_attribute('textContent')
            ratings = ratings.replace(',', '')
            ratings = int(ratings)
    except Exception as e:
        # print("parse_ratings err:", e)
        pass
    return ratings


def parse_price(driver, asin):
    price = 0
    currency = ''
    try:
        price_origin = driver.find_element_by_xpath('//div[@data-asin="{}"]//div[@class="a-row a-size-base a-color-base"]//span[@class="a-offscreen"]'.format(asin)).get_attribute('textContent')
        # price_origin = '$4.34'
        currency = re.findall('[^0-9.-]', price_origin)[0]
        price = price_origin.replace(currency, '')
        price = float(price)
    except Exception as e:
        # print("parse_price err:", e)
        pass
    return price, currency


def parse_sponsored(driver, asin):
    sponsored = ''
    try:
        sponsored = driver.find_element_by_xpath('//div[@data-asin="{}"]//span[@class="s-label-popover-hover"]//span[@class="a-color-base"]'.format(asin)).get_attribute('textContent')
    except Exception as e:
        pass
    return sponsored


def parse_best_seller_in(driver, asin):
    best_seller_in = ''
    try:
        best_seller_in = driver.find_element_by_xpath('//div[@data-asin="{}"]//span[@id="{}-best-seller-supplementary"]'.format(asin, asin)).get_attribute('textContent').replace('in ', '')
    except Exception as e:
        pass
    return best_seller_in


def get_product_list(driver, keywords):
    product_list = driver.find_elements_by_xpath('//div[@class="s-main-slot s-result-list s-search-results sg-row"]/div[@data-asin]')
    # print(len(product_list))
    asin_list = []
    for asin in product_list:
        asin = asin.get_attribute('data-asin')
        if asin != '':
            asin_list.append(asin)
    # print(asin_list)
    # print(len(asin_list))
    rank = 1
    for i in range(len(asin_list)):
        item = get_dict_item(keywords, asin_list[i], driver)
        if item['sponsored'] == '':
            item['rank'] = rank
            rank += 1
        else:
            item['rank'] = 0
        print(item)

        # 存入5050 mysql下的parse_product表
        # save_mysql.save_data(item)

        # 存入clickhouse
        save_clickhouse.save_clickhouse(item)


def get_dict_item(keywords, asin, driver):
    item = {}
    item['keywords'] = keywords
    item['asin'] = asin

    title = parse_title(driver, asin)
    item['title'] = escape_string(title)

    image = parse_image(driver, asin)
    item['image'] = escape_string(image)

    stars = parse_stars(driver, asin)
    item['stars'] = stars

    ratings = parse_ratings(driver, asin)
    item['ratings'] = ratings

    price, currency = parse_price(driver, asin)
    item['price'] = price
    item['currency'] = currency

    sponsored = parse_sponsored(driver, asin)
    item['sponsored'] = sponsored

    best_seller_in = parse_best_seller_in(driver, asin)
    item['best_seller_in'] = escape_string(best_seller_in)
    return item


# def get_tuple_item(keywords, asin, driver):
#     title = parse_title(driver, asin)
#
#     image = parse_image(driver, asin)
#
#     stars = parse_stars(driver, asin)
#
#     ratings = parse_ratings(driver, asin)
#
#     price = parse_price(driver, asin)
#
#     sponsored = parse_sponsored(driver, asin)
#
#     best_seller_in = parse_best_seller_in(driver, asin)
#
#     item = (keywords, asin, title, image, stars, ratings, price, sponsored, best_seller_in)
#     return item
