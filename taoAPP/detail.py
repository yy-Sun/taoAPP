import time
from taoAPP.utils import *


def get_clickable_image(xpath):
    return get_elements_by_xpath(xpath)


def handle_images(wait, num, item, xpath):
    # 拼接xpath
    xpath = xpath + '[' + str(num + 1) + ']' + '/android.view.View'
    images = get_clickable_image(xpath)
    return images


def prepare_image():
    # 找到图片按钮，并点击  如果没有图片按钮就继续下一步
    btn_id = 'com.taobao.taobao:id/btn_customed_indicator_extra'
    btn_customed_indicator_extra = get_element_by_id(btn_id, time_out=8)
    if btn_customed_indicator_extra is not None:
        btn_customed_indicator_extra.click()

    # 找到图片的数量
    index_num_id = 'com.taobao.taobao:id/text_pic_index'
    index_num_text = get_text_by_id(index_num_id)
    return int(index_num_text[-1])


def get_images(img_id):
    imgs = []
    num = prepare_image()
    for i in range(num):
        # 点击图片，进入大图
        if i < 1:
            image_element = get_element_by_id(img_id)
            image_element.click()
            time.sleep(1)
        png_path = str(i) + '.png'
        get_file(png_path)
        imgs.append(png_path)
        # 返回，并右翻页
        if i < num - 1:
            swipe_left(300)
        time.sleep(0.5)
    driver.keyevent(4)
    return imgs


def _str_price2int(_original_price_str):
    index_start = 0
    index_end = 0
    start = True
    for i in range((len(_original_price_str))):
        if start:
            if i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                # i 是数字，作为开始
                index_start = i
                print(index_start)
                start = False
        else:
            if i not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                index_end = i
                print(index_end)
                break

    return int(_original_price_str[index_start:index_end])


def move_image_up(xpath):
    size = get_size_by_xpath(xpath, time_out=30, num=0)
    swipe_up(size['height'] - 160)


def move_params_up():
    up = 530
    swipe_up(up)


def get_params():
    print('开始寻找参数')
    params_xpath = '//android.widget.ListView/android.widget.LinearLayout'

    params_map = {}
    flag = True
    while flag:
        flag = False
        params_elements = get_elements_by_xpath(params_xpath, time_out=5)
        # 确定加载完毕
        for trying in range(5):
            if len(params_elements) < 4:
                params_elements = get_elements_by_xpath(params_xpath, time_out=5)
                continue
            break

        for i in range(len(params_elements), 0, -1):
            now_xpath = params_xpath + '[' + str(i) + ']' + '//android.widget.TextView'
            params_texts = get_texts_by_xpath(now_xpath)
            if len(params_texts) > 1 and params_texts[0] not in params_map:
                print(params_texts)
                params_map[params_texts[0]] = params_texts[1]
                print('插入一个参数,说明没有到底')
                flag = True
            elif params_texts[0] in params_map:
                break
        move_params_up()
    print('采集完毕所有参数')
    driver.keyevent(4)
    return params_map


def handle_detail(goods_time):
    print('搜素详情页内容', goods_time)
    # 将5张图片保存到本地，返回一个图片的url列表
    img_id = 'com.taobao.taobao:id/taodetail_gallery_image'

    img_path_list = get_images(img_id)
    print(img_path_list)

    price_xpath = '//android.widget.ListView/android.widget.FrameLayout[2]//android.widget.TextView'
    price_texts = get_texts_by_xpath(price_xpath)
    print(price_texts)
    # //android.widget.ListView/android.widget.FrameLayout[3]//android.widget.TextView
    frameLayout_xpath = '//android.widget.ListView/android.widget.FrameLayout'
    # 将图片上移图片的size - 50
    move_image_up(frameLayout_xpath)
    time.sleep(1)

    all_frameLayouts = get_elements_by_xpath(frameLayout_xpath)
    index = 2
    is_main_text = True
    is_send_goods = False
    is_params = False
    print('项目栏的数量：', len(all_frameLayouts))
    for frameLayou in all_frameLayouts[2:]:
        now_xpath = frameLayout_xpath + '[' + str(index) + ']' + '//android.widget.TextView'
        index += 1
        # 价格已经找到，现在遍历所有的项目栏，因为有的可能没有数据，所有我们将等待时间设置为5秒，找不到就说明没有，直接下一轮
        print('找出第', index - 1, '栏的text')
        texts = get_texts_by_xpath(now_xpath, 3)
        if is_main_text:
            print('寻找主题')
            if len(texts) > 0 and len(texts[0]) > 12:
                print('找到主题栏，结束本次循环，开始下一个')
                print('主题：', texts[0])
                is_main_text = False
                is_send_goods = True
                continue
            print('没有找到主题，继续寻找')
        if is_send_goods:
            if len(texts) > 0 and texts[0] == '发货':
                print('找到发货栏，结束本次循环，开始下一个')
                print(texts)
                is_send_goods = False
                is_params = True
                index += 2  # 发货栏离参数栏至少有两栏的距离
                continue
            print('没有找到发货栏，继续寻找')
        if is_params:
            if len(texts) > 0 and texts[0] == '参数':
                print('找到参数栏，点击并结束循环')
                get_elements_by_xpath(now_xpath)[0].click()
                print(get_params())
                break
        print('没有找到参数栏，继续寻找')

    driver.keyevent(4)
    print('退出详情页')
