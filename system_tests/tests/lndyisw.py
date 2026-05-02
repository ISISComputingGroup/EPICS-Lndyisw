import unittest

from parameterized import parameterized
from utils.channel_access import ChannelAccess  # type: ignore
from utils.emulator_launcher import CommandLineEmulatorLauncher  # type: ignore
from utils.ioc_launcher import ProcServLauncher, get_default_ioc_dir  # type: ignore
from utils.test_modes import TestModes  # type: ignore
from utils.testing import get_running_lewis_and_ioc  # type: ignore

DEVICE_PREFIX = "LNDYISW_01"


IOCS = [
    {
        "name": DEVICE_PREFIX,
        "directory": get_default_ioc_dir("LNDYISW"),
        "macros": {"IPADDR": "127.0.0.1"},
        "ioc_launcher_class": ProcServLauncher,
        "emulator": "Lndyisw",
        "emulator_launcher_class": CommandLineEmulatorLauncher,
        "emulator_command_line": "cmd.exe /c responder.bat",
        "emulator_cwd_emulator_path": True,
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
        ## restart IOC and emulator
        self._ioc.__exit__(None, None, None)
        self._lewis.__exit__(None, None, None)
        self._lewis.__enter__()
        self._ioc.__enter__()

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

    @parameterized.expand(
        [
            ("_odds", "1,0,1,0,1,0,1,0"),
            ("_even", "0,1,0,1,0,1,0,1"),
            ("_all", "1,1,1,1,1,1,1,1"),
            ("_first_half", "1,1,1,1,0,0,0,0"),
            ("_second_half", "0,0,0,0,1,1,1,1"),
        ]
    )
    def test_status_split_properly(self, _, vals):
        self.ca.set_pv_value("STATUS:ALLSET", "0,0,0,0,0,0,0,0")
        self.ca.set_pv_value("STATUS:ALLSET", vals)
        check_outlet_status_calc(vals.split(","), self.ca)
        check_outlet_status_bi(vals.split(","), self.ca)

    def test_WHEN_curr_val_i_updates_THEN_correct_allset_update(self):
        allset = ["0", "0", "0", "0", "0", "0", "0", "0"]
        self.ca.set_pv_value("STATUS:ALLSET", ",".join(allset))
        for index in range(0, 8):
            # this is used to test against scalcout record string fields
            # which are named AA, BB, CC etc.
            field_part = chr(ord("A") + index)
            field = field_part * 2

            self.ca.set_pv_value("STATUS:CURRVAL.I", 10 * (index + 1) + 1)  # turn it on
            self.ca.assert_that_pv_is(f"STATUS:CURRVAL.{field}", "1")
            allset[index] = "1"
            self.ca.assert_that_pv_is("STATUS:ALLSET", ",".join(allset))

            self.ca.set_pv_value("STATUS:CURRVAL.I", 10 * (index + 1))  # turn it off
            self.ca.assert_that_pv_is(f"STATUS:CURRVAL.{field}", "0")
            allset[index] = "0"
            self.ca.assert_that_pv_is("STATUS:ALLSET", ",".join(allset))

        # we repeat above, but don't turn off outlets, so all eight should
        # be on by end
        for index in range(0, 8):
            # this is used to test against scalcout record string fields
            # which are named AA, BB, CC etc.
            field_part = chr(ord("A") + index)
            field = field_part * 2

            self.ca.assert_that_pv_is(f"STATUS:CURRVAL.{field}", "0")
            self.ca.set_pv_value("STATUS:CURRVAL.I", 10 * (index + 1) + 1)  # turn it on
            self.ca.assert_that_pv_is(f"STATUS:CURRVAL.{field}", "1")
            allset[index] = "1"
            self.ca.assert_that_pv_is("STATUS:ALLSET", ",".join(allset))

        allset = ["0", "0", "0", "0", "0", "0", "0", "0"]
        self.ca.set_pv_value("STATUS:ALLSET", ",".join(allset))

    def test_LNDYISW_ioc_WHEN_two_sets_THEN_both_work(self):
        self.ca.set_pv_value("STATUS:ALLSET", "0,0,0,0,0,0,0,0")

        self.ca.set_pv_value("OUTLET1:STATUS:SP", 1, sleep_after_set=0)
        self.ca.set_pv_value("OUTLET2:STATUS:SP", 1)

        self.ca.assert_that_pv_is("OUTLET1:STATUS", "ON")
        self.ca.assert_that_pv_is("OUTLET2:STATUS", "ON")

        self.ca.set_pv_value("OUTLET1:STATUS:SP", 0, sleep_after_set=0)
        self.ca.set_pv_value("OUTLET2:STATUS:SP", 0)

        self.ca.assert_that_pv_is("OUTLET1:STATUS", "OFF")
        self.ca.assert_that_pv_is("OUTLET2:STATUS", "OFF")


def check_outlet_status_calc(vals, ca):
    ca.assert_that_pv_is("OUTLET:STATUS1.B", float(vals[0]))
    ca.assert_that_pv_is("OUTLET:STATUS1.C", float(vals[1]))
    ca.assert_that_pv_is("OUTLET:STATUS1.D", float(vals[2]))
    ca.assert_that_pv_is("OUTLET:STATUS1.E", float(vals[3]))

    ca.assert_that_pv_is("OUTLET:STATUS2.F", float(vals[4]))
    ca.assert_that_pv_is("OUTLET:STATUS2.G", float(vals[5]))
    ca.assert_that_pv_is("OUTLET:STATUS2.H", float(vals[6]))
    ca.assert_that_pv_is("OUTLET:STATUS2.I", float(vals[7]))


def check_outlet_status_bi(vals, ca):
    status = ["OFF", "ON"]
    ca.assert_that_pv_is("OUTLET1:STATUS", status[int(vals[0])])
    ca.assert_that_pv_is("OUTLET2:STATUS", status[int(vals[1])])
    ca.assert_that_pv_is("OUTLET3:STATUS", status[int(vals[2])])
    ca.assert_that_pv_is("OUTLET4:STATUS", status[int(vals[3])])

    ca.assert_that_pv_is("OUTLET5:STATUS", status[int(vals[4])])
    ca.assert_that_pv_is("OUTLET6:STATUS", status[int(vals[5])])
    ca.assert_that_pv_is("OUTLET7:STATUS", status[int(vals[6])])
    ca.assert_that_pv_is("OUTLET8:STATUS", status[int(vals[7])])
