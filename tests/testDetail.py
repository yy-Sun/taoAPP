from taoAPP import detail
import unittest


class DetailTestCase(unittest.TestCase):
    """测试detail.py"""

    def test_str_price2int(self):
        """测试def _str_price2int(_original_price_str):"""
        price_str = '$32.7元'
        price_int = detail._str_price2int(price_str)
        self.assertEquals(price_int, 32)
