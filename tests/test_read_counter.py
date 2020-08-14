# -*- coding: utf-8 -*-

import unittest
from unittest.mock import Mock

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

    def test_zero_read(self):
        prodmon.part_count_entry = Mock()

        comm = Mock_Comm(
            {self.counter_entry['tag']: 0, self.counter_entry['Part_Type_Tag']: 0})

        # set non zero value so we know it is zeroed
        self.counter_entry['lastcount'] = 255

        prodmon.read_counter(self.counter_entry, comm)

        prodmon.part_count_entry.assert_not_called()
        assert self.counter_entry['lastcount'] == 0

    # def test_first_pass_through(mocker):
    #     mocker.patch('part_count_entry')

    #     counter_entry = get_counter_entry()

    #     comm = Mock_Comm(
    #         {counter_entry['tag']: 255, counter_entry['Part_Type_Tag']: 0})

    #     main.read_counter(counter_entry, comm)

    #     main.part_count_entry.assert_called_once()
    #     assert counter_entry['lastcount'] == 255

    # def test_multiple_entries(mocker):
    #     mocker.patch('part_count_entry')

    #     counter_entry = get_counter_entry()
    #     counter_entry['lastcount'] = 250

    #     comm = Mock_Comm(
    #         {counter_entry['tag']: 252, counter_entry['Part_Type_Tag']: 0})

    #     main.read_counter(counter_entry, comm)

    #     assert main.part_count_entry.call_count == 2
    #     assert counter_entry['lastcount'] == 252


if __name__ == '__main__':
    unittest.main()
