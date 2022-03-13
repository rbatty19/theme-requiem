from pickle import TRUE
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from lib import config_yml
from glom import glom
import matplotlib.pyplot as plt
import numpy as np
import time
import datetime
import os


def login(drive, alias, username, passwd):
    drive.implicitly_wait(400)
    input = drive.find_element_by_xpath("//input[@id='resolving_input']")
    input.send_keys(alias)
    input.send_keys(Keys.ENTER)

    input = drive.find_element_by_xpath("//input[@name='username']")
    input.send_keys(username)

    input = drive.find_element_by_xpath("//input[@name='password']")
    input.send_keys(passwd)

    input.send_keys(Keys.ENTER)
    drive.implicitly_wait(300)


def handle_chart(sample_dict, keys_to_chart):
    for count, key in enumerate(keys_to_chart, start=1):
        fig = plt.figure(figsize=(20, 10))
        plt.bar(
            x=list(range(len(sample_dict.get(key)))),
            height=sample_dict.get(key), label=key,
            width=0.4
        )
        min_in_array = min(sample_dict.get(key))-2
        max_in_array = max(sample_dict.get(key))+2
        t1 = np.arange(min_in_array, max_in_array, 1)
        #plt.yticks(np.arange(min(sample_dict.get(key)), max(sample_dict.get(key)), 1))
        plt.yticks(range(min_in_array, max_in_array, 1))
        for bar_count, bar_value in enumerate(sample_dict.get(key), start=0):
            plt.text(bar_count, bar_value+0.2,
                     str(bar_value), ha='center', fontsize=12)

        plt.ylim([min_in_array, max_in_array])
        plt.xlabel('Iteration')
        plt.ylabel('AWS SQS Process')
        plt.legend(loc='upper left')
        plt.grid(True)
        plt.title('SQS Message Queu')
        fig.savefig(f"temp/{key}.png")
        # plt.show()


def custom_aws_sqs_queu(driver):
    # wait the page loading ...
    # time.sleep(metric['sleep'] if ('sleep' in metric) else 100)
    driver.implicitly_wait(400)
    # to identify the table column
    l = driver.find_elements_by_xpath(
        "//*[@class= 'awsui-table-container']/table")[0]
    col_header = l.find_element_by_xpath(
        "//th[@data-awsui-column-id='messagesAvailable']//span")
    col_header.click()
    col_header.click()
    driver.implicitly_wait(400)
    screenshot_filename = f'{savedir}AWS - {metric["name"]}.png'
    refresh_button = l.find_element_by_xpath(
        "//awsui-button[@id='refresh-button']")
    testdict = {}
    for iteration_monitor in range(1, 30):
        for row in range(1, 11):
            rows = l.find_elements(
                By.XPATH, "//body//tbody//tr[" + str(row) + "]")
            for row_data in rows:
                col = row_data.find_elements(By.TAG_NAME, "td")
                keyname = f'{col[1].text}'
                if not keyname in testdict:
                    testdict[keyname] = []
                testdict[keyname].append(int(col[4].text))
        refresh_button.click()
        time.sleep(2)

    print(testdict)
    handle_chart(testdict, [
        'ceb-board-load-license-oracle-sync',
        'ceb-board-users-sync'
    ])


options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1480,1480")
# driver = webdriver.Chrome()


# grafana panel url
# url =
# create the image path
basedir = "screenshots"
now = datetime.datetime.now()
savedir = (
    basedir + "/" + str(now.year) + "/" + str(now.month) +
    "/" + str(now.day) + "/"
)
if not os.path.exists(savedir):
    os.makedirs(savedir)

urls_arr = [
    {
        "url": "https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/ceb-license-migration?tab=monitoring",
        "name": "Licenses Migration Lambda",
        "login": (
            config_yml.env['aws_ec_alias'],
            config_yml.env['aws_ec_username'],
            config_yml.env['aws_ec_password']
        ),
        "is_screenshot": True
    },
    {
        "url": "https://urlzs.com/fr2by",
        "name": "Lambda - Invocations - Sum",
        "login": (
            config_yml.env['aws_ec_alias'],
            config_yml.env['aws_ec_username'],
            config_yml.env['aws_ec_password']
        ),
        "is_screenshot": True
    },
    {
        "url": "https://urlzs.com/Uv1ve",
        "name": "Lambda - Duration - p99",
        "login": (
            config_yml.env['aws_ec_alias'],
            config_yml.env['aws_ec_username'],
            config_yml.env['aws_ec_password']
        ),
        "is_screenshot": True
    },
    {
        "url": "https://urlzs.com/ppRdX",
        "name": "SQS - Msgs Received - Sum",
        "login": (
            config_yml.env['aws_ec_alias'],
            config_yml.env['aws_ec_username'],
            config_yml.env['aws_ec_password']
        ),
        "is_screenshot": True
    },
    {
        "url": "https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards:name=CEB-Board-DailyDevSupport",
        "name": "CEB-Board-DailyDevSupport",
        "login": (
            config_yml.env['aws_ec_alias'],
            config_yml.env['aws_ec_username'],
            config_yml.env['aws_ec_password']
        ),
        "is_screenshot": True
    },
    {
        "url": "https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logEventViewer:group=/aws/lambda/ceb-load-license-dashboard;filter=%22cd_process_license_type:%20'LICENSE_ERROR%22;start=PT6H",
        "name": "Process License Error",
        "login": (
            config_yml.env['aws_ec_alias'],
            config_yml.env['aws_ec_username'],
            config_yml.env['aws_ec_password']
        ),
        "is_screenshot": True
    },
    {
        "url": "https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logEventViewer:group=/aws/lambda/ceb-load-license-dashboard;filter=%22code:%20'pkg_board_implementation_api.send_email_notification%22;start=P2D",
        "name": "Finish Events",
        "login": (
            config_yml.env['aws_ec_alias'],
            config_yml.env['aws_ec_username'],
            config_yml.env['aws_ec_password']
        ),
        "is_screenshot": True
    },
    {
        "url": "https://us-east-1.console.aws.amazon.com/sqs/v2/home?region=us-east-1#/queues",
        "name": "SQS - CEB Account",
        "login": (
            config_yml.env['aws_ceb_alias'],
            config_yml.env['aws_ceb_username'],
            config_yml.env['aws_ceb_password']
        ),
        "is_custom": True,
    },
]

urls_arr1 = [
    {
        "url": "https://us-east-1.console.aws.amazon.com/sqs/v2/home?region=us-east-1#/queues",
        "name": "SQS - CEB Account",
        "login": (
            config_yml.env['aws_ceb_alias'],
            config_yml.env['aws_ceb_username'],
            config_yml.env['aws_ceb_password']
        ),
        "is_custom": True,
        "custom": lambda driver: custom_aws_sqs_queu(driver)
    },
]


for metric in urls_arr1:
    try:
        print('---------------------')
        print(metric['name']+':')
        print('---------------------')
        driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=options)
        driver.get(metric['url'])
        # LOGIN CONFIG
        alias, username, password = metric['login']
        metric_name = metric['name']
        login(driver, username=username, alias=alias, passwd=password)

        if (glom(metric, 'is_screenshot', default=False)):
            # wait the page loading ...
            time.sleep(metric['sleep'] if ('sleep' in metric) else 100)
            # save images

            screenshot_filename = f'{savedir}AWS - {metric_name}.png'
            driver.get_screenshot_as_file(screenshot_filename)
        if (glom(metric, 'is_custom', default=False)):
            print('it pass')
            pass

    finally:
        driver.close()
        driver.quit()
