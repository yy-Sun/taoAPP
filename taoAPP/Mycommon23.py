from taoAPP.detail import handle_images, handle_detail
from taoAPP.utils import *
import time

shop_xpath = '//android.support.v7.widget.RecyclerView/android.widget.FrameLayout'


def get_all_shops():
    # 找到我的淘宝
    mytaobao_xpath = '//android.widget.FrameLayout[@content-desc="我的淘宝"]'
    mytaobao_ele = get_element_by_xpath(mytaobao_xpath, time_out=5, limit=1)
    # 点击
    mytaobao_ele.click()

    # 找到关注店铺
    my_attention_xpath = '//android.widget.LinearLayout[@content-desc="关注店铺"]'
    my_attention_element = get_element_by_xpath(my_attention_xpath, time_out=5, limit=1)
    print('点击关注店铺')
    my_attention_element.click()

    print('找到所有店铺')
    return get_elements_by_xpath(shop_xpath, time_out=8, limit=9)


def into_now_goods():
    """进入到新品界面"""
    new_shops_xpath = '//android.view.View[@content-desc="新品"]'
    new_shops_element = get_element_by_xpath(new_shops_xpath, time_out=5, limit=1)
    print('点击进入新品')
    new_shops_element.click()

    print('等待新品界面加载')
    time.sleep(1)


def get_all_goods():
    all_goods_xpath = '//android.widget.FrameLayout[@content-desc="WVUCWebView"]/android.' \
                      'view.View/android.webkit.WebView/android.view.View/android.view.View/android.view.View'
    return get_elements_by_xpath(all_goods_xpath, time_out=10, limit=7)[3:-3]


def get_childele_from_new_good(num):
    num += 3
    # //android.widget.FrameLayout[@content-desc="WVUCWebView"]/android.view.View/android.webkit.WebView/android.view.View/android.view.View/android.view.View[4]/android.view.View[1]
    xpath = '//android.widget.FrameLayout[@content-desc="WVUCWebView"]/android.view.View/' \
            'android.webkit.WebView/android.view.View/android.view.View/android.view.View' + '[' + str(
        num) + ']' + '/android.view.View'

    return get_elements_by_xpath(xpath, time_out=5, limit=1)


def get_good_time(num, num2):
    # 拼接xpath字符串 num 需要从1开始
    num += 3  # 从第四个开始
    num2 += 1  # 从第一个开始
    xpath = '//android.widget.FrameLayout[@content-desc="WVUCWebView"]/android.view.View/' \
            'android.webkit.WebView/android.view.View/android.view.View/android.view.View' + '[' + str(
        num) + ']' + '/android.view.View' + "[" + str(num2) + "]" + "/android.view.View"
    return get_text_by_xpath(xpath)


def get_imageElements(num, num2):
    # 拼接xpath字符串 num 需要从1开始
    num += 3
    num2 += 1
    xpath = '//android.widget.FrameLayout[@content-desc="WVUCWebView"]/android.view.View/' \
            'android.webkit.WebView/android.view.View/android.view.View/android.view.View' + '[' + str(
        num) + ']' + '/android.view.View'  "[" + str(num2) + "]" + "/android.view.View"
    image_element = get_elements_by_xpath(xpath, time_out=5, limit=2)
    return {xpath: image_element}


def swipe_to_next(webelement, driver):
    """每次存储完毕一栏的新品，都要下翻一栏
    这里要根据当前元素的位置参数进行调整"""
    local = webelement.size
    h = local['height']
    driver.swipe(345, 980, 355, 980 - h, 880)


def first_swipe(webelement):
    local = webelement.location_in_view
    if local['y'] > 320:
        swipe_up(local['y'] - 320)


def hander_shop():
    print(' 进入新品界面')
    into_now_goods()

    all_goods = get_all_goods()
    print(' 找到所有的新品栏', len(all_goods))

    num = 1
    goods_time = ''
    for goods in all_goods:
        print('对每个新品栏，找到子节点的个数，即是否包含日期')
        print(str(num + 3) + '--> 当前新品栏num')

        child_eles = get_childele_from_new_good(num)
        images_map = {}
        if len(child_eles) > 1:
            print('包含日期，对日期更新')
            goods_time = get_good_time(num, 0)
            images_map = get_imageElements(num, 1)
        else:
            images_map = get_imageElements(num, 0)

        xpath = list(images_map)[0]
        images = images_map.get(xpath)

        if len(images) >= 3:  # 是大图
            print('对新品栏距离进行微调')
            first_swipe(goods)
            print('进入新品栏')
            images[0].click()
            handle_detail(goods_time)

        else:  # 不是大图
            flog = True
            for i in range(len(images)):
                if flog:
                    first_swipe(goods)
                    flog = False  # 只调整一次
                # imgs = handle_images(i, goods_time, xpath)  # 得到可点击的图片？应该不需要
                images[i].click()
                handle_detail(goods_time)
        print('获取完毕1栏，准备滑动到下下一栏')
        time.sleep(0.8)
        swipe_to_next(goods)
        num += 1


def get_shop_name(num):
    new_xpath = shop_xpath + '[' + str(
        num) + ']/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout'
    FrameLayouts = get_elements_by_xpath(new_xpath, limit=1)
    for i in range(len(FrameLayouts)):
        if i == 0:
            continue  # 第一个不需要操作
        shop_name_xpath = new_xpath + '[' + str(i + 1) + ']/android.widget.FrameLayout/android.view.View'
        shop_name_str = get_desc_content_by_xpath(shop_name_xpath, time_out=5)
        if shop_name_str == '':
            print('当前的FrameLayout不是真的，继续下一个')
            continue

        # 走到这一步，说明已经找到店铺名，点击进入店铺，并结束循环
        FrameLayouts[i].click()
        return shop_name_str
