from unittest import TestCase
from unittest.mock import Mock, patch, call

from mock import GPIO
from mock.ibs import IBS
from src.cleaning_robot import CleaningRobot, CleaningRobotError


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

    @patch.object(IBS, 'get_charge_left')
    @patch.object(GPIO, 'output')
    def test_manage_cleaning_system_battery_lower_equal_than_10_turn_on_recharge_led(self, mock_gpio: Mock, mock_ibs: Mock):
        mock_ibs.return_value = 9

        system = CleaningRobot()
        system.manage_cleaning_system()

        calls = [call(system.CLEANING_SYSTEM_PIN, False), call(system.RECHARGE_LED_PIN, True)]

        mock_gpio.assert_has_calls(calls, any_order=True)

        self.assertTrue(system.recharge_led_on)

    @patch.object(IBS, 'get_charge_left')
    @patch.object(GPIO, 'output')
    def test_manage_cleaning_system_battery_lower_equal_than_10_turn_off_cleaning_system(self, mock_gpio: Mock, mock_ibs: Mock):
        mock_ibs.return_value = 9

        system = CleaningRobot()
        system.cleaning_system_on = True
        system.manage_cleaning_system()

        calls = [call(system.CLEANING_SYSTEM_PIN, False), call(system.RECHARGE_LED_PIN, True)]

        mock_gpio.assert_has_calls(calls, any_order=True)

        self.assertFalse(system.cleaning_system_on)

    @patch.object(CleaningRobot, 'activate_wheel_motor')
    def test_execute_command_move_forward(self, mock_wheel_motor: Mock):
        system = CleaningRobot()

        system.pos_x = 0
        system.pos_y = 0
        system.heading = system.N

        new_status = system.execute_command(system.FORWARD)

        mock_wheel_motor.assert_called()

        self.assertEqual(new_status, '(0,1,N)')

    @patch.object(CleaningRobot, 'activate_rotation_motor')
    def test_execute_command_move_right(self, mock_rotation_motor: Mock):
        system = CleaningRobot()

        system.pos_x = 0
        system.pos_y = 0
        system.heading = system.N

        new_status = system.execute_command(system.RIGHT)

        mock_rotation_motor.assert_called_with(system.RIGHT)

        self.assertEqual(new_status, '(0,0,E)')

    @patch.object(CleaningRobot, 'activate_rotation_motor')
    def test_execute_command_move_left(self, mock_rotation_motor: Mock):
        system = CleaningRobot()

        system.pos_x = 0
        system.pos_y = 0
        system.heading = system.N

        new_status = system.execute_command(system.LEFT)

        mock_rotation_motor.assert_called_with(system.LEFT)

        self.assertEqual(new_status, '(0,0,W)')

    def test_execute_command_invalid_command(self):
        system = CleaningRobot()

        system.pos_x = 0
        system.pos_y = 0
        system.heading = system.N

        self.assertRaises(CleaningRobotError, system.execute_command, 'a')

    @patch.object(GPIO, 'input')
    def test_obstacle_found_true(self, mock_infrared: Mock):
        system = CleaningRobot()
        mock_infrared.return_value = True
        self.assertTrue(system.obstacle_found())

    @patch.object(GPIO, 'input')
    def test_obstacle_found_false(self, mock_infrared: Mock):
        system = CleaningRobot()
        mock_infrared.return_value = False
        self.assertFalse(system.obstacle_found())

    @patch.object(CleaningRobot, 'activate_wheel_motor')
    @patch.object(GPIO, 'input')
    def test_execute_command_move_obstacle_detected(self, mock_infrared: Mock, mock_wheel_motor: Mock):
        system = CleaningRobot()
        mock_infrared.return_value = True

        system.pos_x = 0
        system.pos_y = 0
        system.heading = system.N

        new_status = system.execute_command(system.FORWARD)

        mock_wheel_motor.assert_not_called()

        self.assertEqual(new_status, '(0,0,N)(0,1)')