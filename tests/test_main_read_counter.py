# -*- coding: utf-8 -*-

import unittest
from unittest.mock import Mock
from random import randint

from .context import prodmon
from .pylogix_helpers import Mock_Comm, Response


class ReadCounterTestSuit(unittest.TestCase):
    """read_counter test cases."""

    def test_thoughts(self):
        self.assertIsNone(None)

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

    def test_first_pass_through(self):
        FIRST_COUNTER_VALUE = randint(1, 2500)
        prodmon.main.part_count_entry = Mock()

        comm = Mock_Comm(
            {self.counter_entry['tag']: FIRST_COUNTER_VALUE, self.counter_entry['Part_Type_Tag']: 0})

        prodmon.read_counter(self.counter_entry, comm)

        prodmon.main.part_count_entry.assert_called_once()
        assert self.counter_entry['lastcount'] == FIRST_COUNTER_VALUE

    def test_zero_read(self):
        prodmon.main.part_count_entry = Mock()

        comm = Mock_Comm(
            {self.counter_entry['tag']: 0, self.counter_entry['Part_Type_Tag']: 0})

        # set non zero value so we know it is zeroed
        self.counter_entry['lastcount'] = 255

        prodmon.read_counter(self.counter_entry, comm)

        prodmon.main.part_count_entry.assert_not_called()
        assert self.counter_entry['lastcount'] == 0

    def test_multiple_entries(self):
        prodmon.main.part_count_entry = Mock()

        self.counter_entry['lastcount'] = 250

        comm = Mock_Comm(
            {self.counter_entry['tag']: 252, self.counter_entry['Part_Type_Tag']: 0})

        prodmon.read_counter(self.counter_entry, comm)

        assert prodmon.main.part_count_entry.call_count == 2
        assert self.counter_entry['lastcount'] == 252


if __name__ == '__main__':
    unittest.main()
