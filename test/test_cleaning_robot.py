from unittest import TestCase
from unittest.mock import Mock, patch, call

from mock import GPIO
from mock.ibs import IBS
from src.cleaning_robot import CleaningRobot


class TestCleaningRobot(TestCase):

    def test_initialize_robot_set_x_to_zero(self):
        system = CleaningRobot()
        system.initialize_robot()
        self.assertEqual(system.pos_x, 0)

    def test_initialize_robot_set_y_to_zero(self):
        system = CleaningRobot()
        system.initialize_robot()
        self.assertEqual(system.pos_y, 0)

    def test_initialize_robot_set_heading_to_n(self):
        system = CleaningRobot()
        system.initialize_robot()
        self.assertEqual(system.heading, 'N')