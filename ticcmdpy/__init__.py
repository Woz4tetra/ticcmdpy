# Uses ticcmd to send and receive data from the Tic over USB.
# Works with either Python 2 or Python 3.
#
# NOTE: The Tic's control mode must be "Serial / I2C / USB".

import yaml
import time
import subprocess


class TicT500:
    def __init__(self, device_number):
        self.device_number = device_number
        self.deg_per_step = 1.0

    def get_steps(self, degrees):
        return int(degrees * self.deg_per_step)

    def arm(self):
        counter = 0
        attempts = 2
        error = None
        for counter in range(attempts):
            try:
                self.status()
                break
            except RuntimeError as error:
                self.clear_driver_error()
        if counter == attempts - 1:
            raise error

        self.resume()

    def disarm(self):
        self.halt_and_hold()
        time.sleep(0.05)
        self.deenergize()

    def status(self):
        raw_status = TicT500._ticcmd('-s', '--full')
        if raw_status.startswith("Error:"):
            tic_list = TicT500._ticcmd('--list')
            raise RuntimeError("ticcmd returned an error: '%s'\n"
                               "list of Tic's:\n%s" % (raw_status, tic_list))
        return yaml.safe_load(raw_status)

    @staticmethod
    def _ticcmd(*args):
        return subprocess.check_output(['ticcmd'] + list(args))

    # Control commands

    def position(self, num):
        # Set target position in microsteps.
        self._ticcmd("-d", self.device_number, "--position", num)

    def position_relative(self, num):
        # Set target position relative to current pos.
        self._ticcmd("-d", self.device_number, "--position-relative", num)

    def velocity(self, num):
        # Set target velocity in microsteps / 10000 s.
        self._ticcmd("-d", self.device_number, "--velocity", num)

    def halt_and_set_position(self, num):
        # Set where the controller thinks it currently is.
        self._ticcmd("-d", self.device_number, "--halt-and-set-position", num)

    def halt_and_hold(self):
        # Abruptly stop the motor.
        self._ticcmd("-d", self.device_number, "--halt-and-hold")

    def home(self, dir):
        # Drive to limit switch; DIR is 'fwd' or 'rev'.
        self._ticcmd("-d", self.device_number, "--home", dir)

    def reset_command_timeout(self):
        # Clears the command timeout error.
        self._ticcmd("-d", self.device_number, "--reset-command-timeout")

    def deenergize(self):
        # Disable the motor driver.
        self._ticcmd("-d", self.device_number, "--deenergize")

    def energize(self):
        # Stop disabling the driver.
        self._ticcmd("-d", self.device_number, "--energize")

    def exit_safe_start(self):
        # Send the exit safe start command.
        self._ticcmd("-d", self.device_number, "--exit-safe-start")

    def resume(self):
        # Equivalent to --energize with --exit-safe-start.
        self._ticcmd("-d", self.device_number, "--resume")

    def enter_safe_start(self):
        # Send the enter safe start command.
        self._ticcmd("-d", self.device_number, "--enter-safe-start")

    def reset(self):
        # Make the controller forget its current state.
        self._ticcmd("-d", self.device_number, "--reset")

    def clear_driver_error(self):
        # Attempt to clear a motor driver error.
        self._ticcmd("-d", self.device_number, "--clear-driver-error")

    # Temporary settings

    def max_speed(self, num):
        # Set the speed limit.
        self._ticcmd("-d", self.device_number, "--max-speed", num)

    def starting_speed(self, num):
        # Set the starting speed.
        self._ticcmd("-d", self.device_number, "--starting-speed", num)

    def max_accel(self, num):
        # Set the acceleration limit.
        self._ticcmd("-d", self.device_number, "--max-accel", num)

    def max_decel(self, num):
        # Set the deceleration limit.
        self._ticcmd("-d", self.device_number, "--max-decel", num)

    def step_mode(self, mode):
        # Set step mode: full, half, 1, 2, 2_100p, 4, 8, 16, 32.
        assert mode in ["full", "half", "1", "2", "2_100p", "4", "8", "16", "32"], mode
        self._ticcmd("-d", self.device_number, "--step-mode", mode)

    def current(self, num):
        # Set the current limit in mA.
        self._ticcmd("-d", self.device_number, "--current", num)

    def decay(self, mode):
        # Set decay mode:
        # Tic T825/N825: mixed, slow, or fast
        # T834: slow, mixed25, mixed50, mixed75, or fast
        self._ticcmd("-d", self.device_number, "--decay", mode)

    # Permanent settings

    def restore_defaults(self):
        # Restore device's factory settings
        self._ticcmd("-d", self.device_number, "--restore-defaults")

    def settings(self, settings_path):
        # Load settings file into device.
        self._ticcmd("-d", self.device_number, "--settings", settings_path)

    def get_settings(self, output_path):
        # Read device settings and write to file.
        self._ticcmd("-d", self.device_number, "--get-settings", output_path)

