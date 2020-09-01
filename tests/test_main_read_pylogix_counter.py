# -*- coding: utf-8 -*-

import unittest
from unittest.mock import Mock, patch, MagicMock
from random import randint

from .context import prodmon
from .pylogix_helpers import Response


class ReadPylogixCounterTestSuit(unittest.TestCase):
    """read_counter test cases."""

    def setUp(self):
        self.counter_entry = {
            # type = counter|value
            'type': 'pylogix_counter',
            # ip is the controller's ip address
            'ip': '10.4.42.135',
            # slot is the controller's slot
            'slot': 3,
            # tag is the PLC tag to read
            'tag': 'Program:Production.ProductionData.DailyCounts.DailyTotal',
            # tag containing what part type is currently running
            'Part_Type_Tag': 'Stn010.PartType',
            # map values in above to a string to write in the part type db colum
            'Part_Type_Map': {'0': '50-4865', '1': '50-5081'},
            # how often to try to read the tag in seconds
            'frequency': .5,
            # database table to write to
            'table': 'GFxPRoduction',
            # Machine is written into the machine colum in the database table
            'Machine': '1617',
            # used internally to track the readings
            'nextread': 0,      # timestamp of the next reading
            'lastcount': 0,     # last counter value
            'lastread': 0       # timestamp of the last read
        }

    @patch("prodmon.main.PLC")
    @patch("prodmon.main.part_count_entry")
    def test_first_pass_through(self, mock_part_count_entry, mock_PLC):

        FIRST_COUNTER_VALUE = randint(1, 2500)

        # mock_PLC.add(self.counter_entry['tag'], FIRST_COUNTER_VALUE)
        # mock_PLC.add(self.counter_entry['Part_Type_Tag'], 0)

        def mock_Read(tag):

            tag_dict = {
                self.counter_entry['tag']: FIRST_COUNTER_VALUE,
                self.counter_entry['Part_Type_Tag']: 0
            }

            print('Reading ', tag)
            if tag in tag_dict:
                print('returned ', tag_dict[tag])
                return Response(tag, Value=tag_dict[tag])
            else:
                print('returned Connection Failure')
                return Response(tag, Value=None, Status='Connection failure')

        mock_client = MagicMock()
        mock_client.Read.side_effect = mock_Read
        mock_client.__enter__.return_value = mock_client
        mock_PLC.return_value = mock_client

        prodmon.read_pylogix_counter(self.counter_entry)

        mock_part_count_entry.assert_called_once()
        assert self.counter_entry['lastcount'] == FIRST_COUNTER_VALUE

    @patch("prodmon.main.PLC")
    @patch("prodmon.main.part_count_entry")
    def test_zero_read(self, mock_part_count_entry, mock_PLC):

        def mock_Read(tag):

            tag_dict = {
                self.counter_entry['tag']: 0,
                self.counter_entry['Part_Type_Tag']: 0
            }

            print('Reading ', tag)
            if tag in tag_dict:
                print('returned ', tag_dict[tag])
                return Response(tag, Value=tag_dict[tag])
            else:
                print('returned Connection Failure')
                return Response(tag, Value=None, Status='Connection failure')

        mock_client = MagicMock()
        mock_client.Read.side_effect = mock_Read
        mock_client.__enter__.return_value = mock_client
        mock_PLC.return_value = mock_client

        # set non zero value so we know if it is zeroed
        self.counter_entry['lastcount'] = 255

        prodmon.read_pylogix_counter(self.counter_entry)

        mock_part_count_entry.assert_not_called()
        assert self.counter_entry['lastcount'] == 0

    @patch("prodmon.main.PLC")
    @patch("prodmon.main.part_count_entry")
    def test_multiple_entries(self, mock_part_count_entry, mock_PLC):

        def mock_Read(tag):

            tag_dict = {
                self.counter_entry['tag']: 252,
                self.counter_entry['Part_Type_Tag']: 0
            }

            print('Reading ', tag)
            if tag in tag_dict:
                print('returned ', tag_dict[tag])
                return Response(tag, Value=tag_dict[tag])
            else:
                print('returned Connection Failure')
                return Response(tag, Value=None, Status='Connection failure')

        mock_client = MagicMock()
        mock_client.Read.side_effect = mock_Read
        mock_client.__enter__.return_value = mock_client
        mock_PLC.return_value = mock_client

        self.counter_entry['lastcount'] = 250

        prodmon.read_pylogix_counter(self.counter_entry)

        assert mock_part_count_entry.call_count == 2
        assert self.counter_entry['lastcount'] == 252


if __name__ == '__main__':
    unittest.main()
