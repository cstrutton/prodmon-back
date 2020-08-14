# -*- coding: utf-8 -*-

import unittest
from unittest.mock import Mock, patch
from random import randint
import time


from .context import prodmon
from .pylogix_helpers import Mock_Comm, Response


class ReadCounterTestSuit(unittest.TestCase):
    """read_counter test cases."""

    def setUp(self):
        self.counter_entry = {
            # type = counter|value
            'type': 'counter',
            # tag is the PLC tag to read
            'tag': 'Tag.Counter',
            # Machine is written into the machine colum on the database
            'Machine': 'MachineName',
            # used internally
            'nextread': 0,
            'lastcount': 0,
            'lastread': 0,
            # how often to try to read the tag in seconds
            'frequency': .5,
            # database table to write to
            'table': 'dbTable',
            # tag containing what part type is currently running
            'Part_Type_Tag': 'Tag.PartType',
            # map values in above to a string to write in the part type db colum
            'Part_Type_Map': {'0': 'PartType0', '1': 'PartType1'}
        }

    @patch("prodmon.main.PLC")
    @patch("prodmon.main.read_counter")
    def test_polling_too_fast(self, mock_read_counter, mock_PLC):

        minimum_cycle = 1
        prodmon.loop([self.counter_entry], '0.0.0.0',
                     slot=0, minimum_cycle=minimum_cycle)
        pass1 = self.counter_entry['lastread']
        pass1time = time.time()
        time.sleep(minimum_cycle/2)
        prodmon.loop([self.counter_entry], '0.0.0.0',
                     slot=0, minimum_cycle=minimum_cycle)
        pass2 = self.counter_entry['lastread']
        pass2time = time.time()
        interval = pass2time-pass1time
        mock_read_counter.assert_called_once()

    @patch("prodmon.main.PLC")
    @patch("prodmon.main.read_counter")
    def test_polling(self, mock_read_counter, mock_PLC):

        minimum_cycle = 1
        prodmon.loop([self.counter_entry], '0.0.0.0',
                     slot=0, minimum_cycle=minimum_cycle)
        time.sleep(minimum_cycle/2)
        prodmon.loop([self.counter_entry], '0.0.0.0',
                     slot=0, minimum_cycle=minimum_cycle)
        time.sleep(minimum_cycle/2)
        prodmon.loop([self.counter_entry], '0.0.0.0',
                     slot=0, minimum_cycle=minimum_cycle)
        assert mock_read_counter.call_count == 2


if __name__ == '__main__':
    unittest.main()
