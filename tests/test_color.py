


import unittest
from suou import RGBColor, chalk
from suou.color import OKLCHColor

class TestColor(unittest.TestCase):
    def setUp(self) -> None:
        ...
    def tearDown(self) -> None:
        ...
    
    def test_chalk_colors(self):
        strg = "The quick brown fox jumps over the lazy dog"
        
        self.assertEqual(f'\x1b[31m{strg}\x1b[39m', chalk.red(strg))
        self.assertEqual(f'\x1b[32m{strg}\x1b[39m', chalk.green(strg))
        self.assertEqual(f'\x1b[34m{strg}\x1b[39m', chalk.blue(strg))
        self.assertEqual(f'\x1b[36m{strg}\x1b[39m', chalk.cyan(strg))
        self.assertEqual(f'\x1b[33m{strg}\x1b[39m', chalk.yellow(strg))
        self.assertEqual(f'\x1b[35m{strg}\x1b[39m', chalk.purple(strg))

    def test_chalk_bold(self):
        strg = "The quick brown fox jumps over the lazy dog"
        self.assertEqual(f'\x1b[1m{strg}\x1b[22m', chalk.bold(strg))
        self.assertEqual(f'\x1b[2m{strg}\x1b[22m', chalk.faint(strg))
        self.assertEqual(f'\x1b[1m\x1b[33m{strg}\x1b[39m\x1b[22m', chalk.bold.yellow(strg))

    def test_oklch_to_rgb(self):
        self.assertEqual(OKLCHColor(0.628, 0.2577, 29.23).to_rgb(), RGBColor(255, 0, 0))
        self.assertEqual(OKLCHColor(0.7653, 0.1306, 194.77).to_rgb(), RGBColor(0, 204, 204))
        self.assertEqual(OKLCHColor(0.5931, 0., 0.).to_rgb(), RGBColor(126, 126, 126))