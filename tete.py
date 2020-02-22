import time
from selenium import webdriver


'''
code : 学校代码，例如清华是10003
name : 你的名字
sfz : 身份证号码
zkz : 准考证号
'''


def chaxun(code, name, sfz, zkz):
    url = 'https://yz.chsi.com.cn/apply/cjcx/t/' + code + '.dhtml'
    options = webdriver.ChromeOptions()
    options.add_argument('-no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=options)
    browser.set_window_size(1600, 1200)
    try:
        browser.get(url)
        input_name = browser.find_element_by_xpath('//*[@name="yzwb_xm"]')
        input_name.send_keys(name)
        input_sfz = browser.find_element_by_xpath('//*[@name="yzwb_zjhm"]')
        input_sfz.send_keys(sfz)
        input_zkz = browser.find_element_by_xpath('//*[@name="yzwb_ksbh"]')
        input_zkz.send_keys(zkz)
        button = browser.find_element_by_xpath('//*[@type="button"]')
        button.click()
        time.sleep(3)
        res = browser.get_screenshot_as_file('result_' + name + '.png')

        try:
            result = browser.find_element_by_class_name('cjcx-noresult')
            if result.text == '请检查您报考的招生单位是否已开通初试成绩查询功能':
                return False
        except:
            print('截图！！')
            return True
    except:
        print('Error!')
    finally:
        browser.close()


if __name__ == '__main__':
    while 1:
        res = chaxun('10590', '---', '---', '---')
        # 填写你自己的 学校代码，姓名，身份证号码，准考证号
        if res:
            print('查询成功！！')
            break
        else:
            print('成绩尚未出')
        print(time.asctime(time.localtime(time.time())))
        time.sleep(350)
