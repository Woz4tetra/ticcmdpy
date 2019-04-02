# ticcmdpy
A python interface for ticcmd. This library is to be used with the [Tic T500](https://www.pololu.com/product/3134/resources).

Here's an example of a basic interface on pololu's website:
```python
# Uses ticcmd to send and receive data from the Tic over USB.
# Works with either Python 2 or Python 3.
#
# NOTE: The Tic's control mode must be "Serial / I2C / USB".
 
import subprocess
import yaml
 
def ticcmd(*args):
  return subprocess.check_output(['ticcmd'] + list(args))
 
status = yaml.load(ticcmd('-s', '--full'))
 
position = status['Current position']
print("Current position is {}.".format(position))
 
new_target = -200 if position > 0 else 200
print("Setting target position to {}.".format(new_target))
ticcmd('--exit-safe-start', '--position', str(new_target))
```

This library wraps most of the options listed in the ticcmd help menu and adds some nice helpers.

Example usage:

```python
import time
from pprint import pprint
from ticcmdpy import TicT500

ticpy = TicT500()

ticpy.arm()  # energize, exit safe start, and check status
 
ticpy.velocity(360000000)  # set velocity
time.sleep(3)  # wait for 3 seconds
ticpy.velocity(0)  # decelerate motor
time.sleep(0.5)

ticpy.halt_and_set_position(0)  # reset current position to zero
ticpy.position(10000)  # move to tick number 10000
time.sleep(3)
ticpy.position(0)  # move back to tick 0


pprint(ticpy.status())

ticpy.disarm()  # halt and hold, then de-energize
```