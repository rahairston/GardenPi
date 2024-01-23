# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`board` - Define ids for available pins
=================================================

See `CircuitPython:board` in CircuitPython for more details.

* Author(s): cefn
"""


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_Blinka.git"
__blinka__ = True


import sys

import adafruit_platformdetect.constants.boards as ap_board
from adafruit_blinka.agnostic import board_id, detector

# pylint: disable=wildcard-import,unused-wildcard-import,ungrouped-imports
# pylint: disable=import-outside-toplevel

if board_id == ap_board.RASPBERRY_PI_PICO:
    from adafruit_blinka.board.raspberrypi.pico import *

elif "sphinx" in sys.modules:
    pass

elif board_id is None:
    import platform
    import pkg_resources

    package = str(pkg_resources.get_distribution("adafruit_platformdetect")).split()
    raise NotImplementedError(
        f"""
        {package[0]} version {package[1]} was unable to identify the board and/or
        microcontroller running the {platform.system()} platform. Please be sure you
        have the latest packages by running:
        'pip3 install --upgrade adafruit-blinka adafruit-platformdetect'

        If you are running the latest package, your board may not yet be supported. Please
        open a New Issue on GitHub at https://github.com/adafruit/Adafruit_Blinka/issues and
        select New Board Request.
        """
    )

else:
    raise NotImplementedError(f"Board not supported {board_id}.")

if "SCL" in locals() and "SDA" in locals():

    def I2C():
        """The singleton I2C interface"""
        import busio

        return busio.I2C(SCL, SDA)


if "SCLK" in locals() and "MOSI" in locals() and "MISO" in locals():

    def SPI():
        """The singleton SPI interface"""
        import busio

        return busio.SPI(SCLK, MOSI, MISO)
