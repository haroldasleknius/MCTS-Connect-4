import unittest
import pygame
from button import Button

class TestCase(unittest.TestCase):
    #Before each test, a button is created 
    def setUp(self):
        pygame.init()
        self.button_image = pygame.image.load("button.png")
        self.button_image = pygame.transform.scale(self.button_image, (400, 150))
        self.button = Button(437, 437, self.button_image, "Test Button")

    def tearDown(self):
        pygame.quit()

    #Tests positioncheck method to see if it returns True when the mouse_pos coordinates are within the button area
    def test_positioncheck_true(self):
        mouse_pos = (439, 439)
        self.assertTrue(self.button.positioncheck(mouse_pos))

    #Tests positioncheck method to see if it returns False when mouse_pos coordinates are outside of the button area
    def test_positioncheck_false(self):
        mouse_pos = (0, 0)
        self.assertFalse(self.button.positioncheck(mouse_pos))

    #Tests hover method to see if it correctly changes the text colour when the mouse_pos is within the button area
    def test_hover_inside(self):
        mouse_pos = (437, 437)
        self.button.hover(mouse_pos)
        self.assertEqual(self.button.colour, (0,0,0))

    #Tests hover method to see if it correctly changes the text colour when the mouse_pos is outside the button area
    def test_hover_outside(self):
        mouse_pos = (0, 0)
        self.button.hover(mouse_pos)
        self.assertEqual(self.button.colour, (255,255,255))


if __name__ == '__main__':
    unittest.main()
