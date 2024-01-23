# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pins named after their chip name."""

import sys
from adafruit_platformdetect.constants import chips as ap_chip
from adafruit_blinka.agnostic import board_id, chip_id

# We intentionally are patching into this namespace so skip the wildcard check.
# pylint: disable=unused-wildcard-import,wildcard-import,ungrouped-imports

if chip_id == ap_chip.RP2040:
    from adafruit_blinka.microcontroller.rp2040.pin import *
elif "sphinx" in sys.modules:
    # pylint: disable=unused-import
    from adafruit_blinka.microcontroller.generic_micropython import Pin
elif chip_id == ap_chip.GENERIC_X86:
    print("WARNING: GENERIC_X86 is not fully supported. Some features may not work.")
    from adafruit_blinka.microcontroller.generic_micropython import Pin
elif chip_id is None:
    print(
        "WARNING: chip_id == None is not fully supported. Some features may not work."
    )
    from adafruit_blinka.microcontroller.generic_micropython import Pin
else:
    raise NotImplementedError("Microcontroller not supported: ", chip_id)
