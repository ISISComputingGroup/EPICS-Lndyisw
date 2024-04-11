import unittest
import subprocess

from utils.channel_access import ChannelAccess
from utils.ioc_launcher import get_default_ioc_dir
from utils.test_modes import TestModes
from utils.testing import get_running_lewis_and_ioc, skip_if_recsim
from utils.emulator_launcher import CommandLineEmulatorLauncher

DEVICE_PREFIX = "LNDYISW_01"


IOCS = [
    {
        "name": DEVICE_PREFIX,
        "directory": get_default_ioc_dir("LNDYISW"),
        "macros": {
            "IPADDR": "127.0.0.1"
        },
        "emulator": "Lndyisw",
        "emulator_launcher_class": CommandLineEmulatorLauncher,
        "emulator_command_line": "responder.bat",
    },
]


TEST_MODES = [TestModes.DEVSIM]


class LndyiswTests(unittest.TestCase):
    """
    Tests for the Lndyisw IOC.
    """
    def setUp(self):
        self._lewis, self._ioc = get_running_lewis_and_ioc("Lndyisw", DEVICE_PREFIX)
        self.ca = ChannelAccess(device_prefix=DEVICE_PREFIX)
        
    def test_LNDYISW_ioc_returns_expected_name(self):
        expected_value = "LYNDY"
        self.ca.assert_that_pv_is("NAME", expected_value)
 
    def test_LNDYISW_ioc_sets_new_name(self):
        old_value = "LYNDY"
        new_value = "ChangedName"
        self.ca.assert_that_pv_is("NAME", old_value)
        
        # Set to new value and check
        self.ca.set_pv_value("NAME:SP", new_value)
        self.ca.assert_that_pv_is_not("NAME", old_value)
        self.ca.assert_that_pv_is("NAME", new_value)
        
        # Set to old value and check
        self.ca.set_pv_value("NAME:SP", old_value)
        self.ca.assert_that_pv_is_not("NAME", new_value)
        self.ca.assert_that_pv_is("NAME", old_value)

    def test_LNDYISW_ioc_returns_expected_location(self):
        expected_value = "CHILTON-DIDCOT"
        self.ca.assert_that_pv_is("LOCATION", expected_value)
 
    def test_LNDYISW_ioc_sets_new_location(self):
        old_value = "CHILTON-DIDCOT"
        new_value = "ChangedName"
        self.ca.assert_that_pv_is("LOCATION", old_value)
        
        # Set to new value and check
        self.ca.set_pv_value("LOCATION:SP", new_value)
        self.ca.assert_that_pv_is_not("LOCATION", old_value)
        self.ca.assert_that_pv_is("LOCATION", new_value)
        
        # Set to old value and check
        self.ca.set_pv_value("LOCATION:SP", old_value)
        self.ca.assert_that_pv_is_not("LOCATION", new_value)
        self.ca.assert_that_pv_is("LOCATION", old_value)
        
    #def test_that_fails(self):
    #    self.fail("You haven't implemented any tests!")
