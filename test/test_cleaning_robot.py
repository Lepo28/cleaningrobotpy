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

    def test_robot_status(self):
        system = CleaningRobot()

        system.pos_x = 0
        system.pos_y = 1
        system.heading = system.N

        status = system.robot_status()

        self.assertEqual(status, '(0,1,N)')

    @patch.object(IBS, 'get_charge_left')
    @patch.object(GPIO, 'output')
    def test_manage_cleaning_system_battery_greater_than_10_turn_off_recharge_led(self, mock_gpio: Mock, mock_ibs: Mock):
        mock_ibs.return_value = 11

        system = CleaningRobot()
        system.manage_cleaning_system()

        calls = [call(system.CLEANING_SYSTEM_PIN, True), call(system.RECHARGE_LED_PIN, False)]

        mock_gpio.assert_has_calls(calls, any_order=True)

        self.assertFalse(system.recharge_led_on)

    @patch.object(IBS, 'get_charge_left')
    @patch.object(GPIO, 'output')
    def test_manage_cleaning_system_battery_greater_than_10_turn_on_cleaning_system(self, mock_gpio: Mock, mock_ibs: Mock):
        mock_ibs.return_value = 11

        system = CleaningRobot()
        system.manage_cleaning_system()

        calls = [call(system.CLEANING_SYSTEM_PIN, True), call(system.RECHARGE_LED_PIN, False)]

        mock_gpio.assert_has_calls(calls, any_order=True)

        self.assertTrue(system.cleaning_system_on)