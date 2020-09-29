import sys
import unittest

sys.path.append("..")  # Adds higher directory to python modules path.


class Test(unittest.TestCase):
    def test_add(self) -> None:
        self.assertEqual(3 + 4, 7)


if __name__ == "__main__":
    unittest.main()
