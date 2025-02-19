import unittest
from mintcheck import grade_card

class TestMintCheck(unittest.TestCase):
    def test_synthetic_card_centered(self):
        image_path = r"C:\Users\dlaev\mintcheck\data\synthetic_card_centered.jpg"
        result = grade_card(image_path)
        self.assertIsNotNone(result)
        self.assertGreaterEqual(result["Centering"], 0.8)
        self.assertGreaterEqual(result["Corners"], 0.9)
        self.assertGreaterEqual(result["Edges"], 0.9)
        self.assertGreaterEqual(result["Surface"], 0.9)
        self.assertGreaterEqual(result["Grade"], 8.0)

    def test_synthetic_card_offset1(self):
        image_path = r"C:\Users\dlaev\mintcheck\data\synthetic_card_offset1.jpg"
        result = grade_card(image_path)
        self.assertIsNotNone(result)
        self.assertLess(result["Centering"], 0.8)

    def test_synthetic_card_offset2(self):
        image_path = r"C:\Users\dlaev\mintcheck\data\synthetic_card_offset2.jpg"
        result = grade_card(image_path)
        self.assertIsNotNone(result)
        self.assertLess(result["Centering"], 0.8)

if __name__ == "__main__":
    unittest.main()
