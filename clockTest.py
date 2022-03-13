import unittest
from clock import Clock


class ClockTest(unittest.TestCase):

    def setUp(self):
        try:
            self.clock = Clock()
        except NameError as e:
            raise NotImplementedError()


if __name__ == '__main__':
    unittest.main()
