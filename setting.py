# 本地数据库
HOSTNAME = '127.0.0.1'
PORT = 3306
DATABASE = 'mysql'
USERNAME = "root"
PASSWORD = "hu306415"

# 5050数据库
# HOSTNAME = '192.168.50.50'
# PORT = 23306
# DATABASE = 'mysql'
# USERNAME = "root"
# PASSWORD = "root@123"

# 进程池的大小
PROCESS_POOL_SIZE = 1

# 一次处理的keywords大小
KEYWORDS_LIST_SIZE = 6

# 开始的url地址
BASE_URL = 'https://www.amazon.com'

# 邮编
POSTAL = "10001"

# webdriver.Chrome的地址
CHROME_WEBDRIVER_PATH = '/users/hutaiyi/downloads/chromedriver'

# chrome是否无头
HEADLESS = True

# 2022.02.17 10:44
# 1.将stars和rating初始化为0，而不是''字符串(解决插入数据库出错问题)
# 2.同时改变如果无sponsored默认是null而不是''字符串，同样的是price，best_seller_in
# 3.添加上传至github
# 4.添加rank以及将price和currency分开

