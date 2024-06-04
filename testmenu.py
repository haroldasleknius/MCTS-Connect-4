import unittest
import pygame
from button import Button
from menu import Menu

class TestCase(unittest.TestCase):
    #Before each test a menu object is created with two buttons 
    def setUp(self):
        pygame.init()
        self.menu = Menu(None)
        self.button_image = pygame.transform.scale(pygame.image.load("button.png"), (400,150))
        self.button1 = Button(437, 337, self.button_image, "First test button")
        self.button2 = Button(437, 537, self.button_image, "Second test button")
        self.menu.add_button(self.button1)
        self.menu.add_button(self.button2)

    def tearDown(self):
        pygame.quit()

    #Test add_button method to see if the objects were successfully added to the buttons list
    def test_add_button(self):
        self.assertIn(self.button1, self.menu.buttons)
        self.assertIn(self.button2, self.menu.buttons)

    #Test button_hover method to check that the correct button changes text colour
    def test_button_hover_inside(self):
        mouse_pos = (439,339)
        self.menu.button_hover(mouse_pos)
        self.assertEqual((0,0,0), self.menu.buttons[0].colour)
        self.assertNotEqual((0,0,0), self.menu.buttons[1].colour)
        mouse_pos = (439, 539)
        self.menu.button_hover(mouse_pos)
        self.assertEqual((0,0,0), self.menu.buttons[1].colour)
        self.assertNotEqual((0,0,0), self.menu.buttons[0].colour)

    #Test button_hover method to check that the colour successfully reverts to the base colour when outside the buttons area
    def test_button_hover_outside(self):
        mouse_pos = (439,339)
        self.menu.button_hover(mouse_pos)
        mouse_pos = (439, 539)
        self.menu.button_hover(mouse_pos)
        mouse_pos = (100,100)
        self.menu.button_hover(mouse_pos)
        self.assertEqual((255,255,255), self.menu.buttons[0].colour)
        self.assertEqual((255,255,255), self.menu.buttons[1].colour)

    #Test button_checks method to check that it returns the name of the button when inside
    def test_button_checks_inside(self):
        mouse_pos = (439, 339)
        name = self.menu.button_checks(mouse_pos)
        self.assertEqual(name, "First test button")
        mouse_pos = (439, 539)
        name = self.menu.button_checks(mouse_pos)
        self.assertEqual(name, "Second test button")

    #Test button_checks method to check that it returns None when outside the area of the buttons
    def test_button_checks_outside(self):
        mouse_pos = (100,100)
        name = self.menu.button_checks(mouse_pos)
        self.assertIsNone(name)

    #Test add_text method to check that text is correctly added into the array
    def test_add_text(self):
        self.assertEqual(len(self.menu.text), 0)
        self.menu.add_text("test", (100,100), 'Calibri', 60, (255,255,255))
        self.assertEqual(len(self.menu.text), 1)

if __name__ == '__main__':
    unittest.main()