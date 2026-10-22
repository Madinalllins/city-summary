import unittest

from processing.preprocessing import needs_warm_clothes, is_expensive_rate


class TestPreprocessing(unittest.TestCase):

    def test_cold_weather(self):
        self.assertTrue(needs_warm_clothes(-5))

    def test_zero_temperature(self):
        self.assertFalse(needs_warm_clothes(0))

    def test_warm_weather(self):
        self.assertFalse(needs_warm_clothes(20))

    def test_expensive_rate(self):
        self.assertTrue(is_expensive_rate(110))

    def test_rate_at_threshold(self):
        self.assertFalse(is_expensive_rate(100))

    def test_normal_rate(self):
        self.assertFalse(is_expensive_rate(85))


if __name__ == "__main__":
    unittest.main()