from taoAPP.Mycommon23 import *
import time
from taoAPP.utils import driver

if __name__ == "__main__":

    time.sleep(1)
    print(' 进入关注店铺界面')
    time.sleep(1.5)

    all_shop_list = get_all_shops()
    print('共有店铺：', len(all_shop_list))
    time.sleep(1)

    # 这里的店铺是以第三个开始的
    print('开始对店铺进行第一论处理，先忽略前两个店铺')
    num = 3
    for shop in all_shop_list[2:]:
        print('取店铺名 并点击进入')
        print(get_shop_name(num))
        num += 1

        print('对店铺进行处理')
        hander_shop()
        print('返回')
        driver.keyevent(4)
        time.sleep(1)
    print('处理完毕当前店铺')
