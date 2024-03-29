from pylogix import PLC
import time
import os

tag_list = [
    {
        # type = counter|value
        'type': 'counter',
        # tag is the PLC tag to read
        'tag': 'Program:Production.ProductionData.DailyCounts.DailyTotal',
        # Machine is written into the machine colum on the database
        'Machine': '1617',
        # used internally
        'nextread': 0,
        'lastcount': 0,
        'lastread': 0,
        # how often to try to read the tag in seconds
        'frequency': .5,
        # database table to write to
        'table': 'GFxPRoduction',
        # tag containing what part type is currently running
        'Part_Type_Tag': 'Stn010.PartType',
        # map values in above to a string to write in the part type db colum
        'Part_Type_Map': {'0': '50-4865', '1': '50-5081'}
    }
]


tag_frequency_op30 = [
    {
        'type': 'counter',
        'tag': 'OP30_4_COUNT.SYSTEM[0].GOOD',
        'Machine': '1605',
        'nextread': 0,
        'lastcount': 0,
        'frequency': .5,
        'table': 'GFxPRoduction',
        'Part_Type_Tag': 'ROBOT_R30_4.O.DI37',
        'Part_Type_Map': {'False': '50-5081', 'True': '50-4865'},
    },
    {
        'type': 'counter',
        'tag': 'OP30_1_COUNT.SYSTEM[0].GOOD',
        'Machine': '1606',
        'frequency': .5,
        'nextread': 0,
        'lastcount': 0,
        'table': 'GFxPRoduction',
        'Part_Type_Tag': 'ROBOT_R30_1.O.DI37',
        'Part_Type_Map': {'False': '50-5081', 'True': '50-4865'},
    },
    {
        'type': 'counter',
        'tag': 'OP30_2_COUNT.SYSTEM[0].GOOD',
        'Machine': '1607',
        'frequency': .5,
        'nextread': 0,
        'lastcount': 0,
        'table': 'GFxPRoduction',
        'Part_Type_Tag': 'ROBOT_R30_2.O.DI37',
        'Part_Type_Map': {'False': '50-5081', 'True': '50-4865'},
    },
    {
        'type': 'counter',
        'tag': 'OP30_3_COUNT.SYSTEM[0].GOOD',
        'Machine': '1608',
        'frequency': .5,
        'nextread': 0,
        'lastcount': 0,
        'table': 'GFxPRoduction',
        'Part_Type_Tag': 'ROBOT_R30_3.O.DI37',
        'Part_Type_Map': {'False': '50-5081', 'True': '50-4865'},
    },
    {
        'type': 'value',
        'tag': 'OP30_3_COUNT.SYSTEM[0].GOOD',
        'nextread': 0,
        'frequency': 5,
        'table': 'DataTable',
        'name': 'random value'
    }
]


def loop(taglist, ip, slot=0, minimum_cycle=.5):
    with PLC() as comm:
        comm.IPAddress = ip
        comm.ProcessorSlot = slot

        for entry in taglist:

            # get current timestamp
            now = time.time()

            frequency = entry['frequency']

            # make sure we are not polling too fast
            if frequency < minimum_cycle:
                frequency = minimum_cycle

            # handle first pass through
            if entry['nextread'] == 0:
                entry['nextread'] = now

            if entry['nextread'] > now:
                continue  # too soon move on

            entry['lastread'] = now

            if entry['type'] == 'counter':
                with PLC() as comm:
                    comm.IPAddress = ip
                    comm.ProcessorSlot = slot
                    read_counter(entry, comm)

            if entry['type'] == 'value':
                with PLC() as comm:
                    comm.IPAddress = ip
                    comm.ProcessorSlot = slot
                    read_value(entry, comm)

            # set the next read timestamp
            entry['nextread'] += frequency


def read_value(value_entry, comm):
    print(time.time(), ':', comm.Read(entry['tag']))


def read_counter(counter_entry, comm):
    # read the tag
    part_count = comm.Read(counter_entry['tag'])
    if part_count.Status != 'Success':
        print('failed to read ', part_count)
        return

    part_type = comm.Read(counter_entry['Part_Type_Tag'])
    if part_type.Status != 'Success':
        print('failed to read ',  part_type)
        return

    if (part_count.Value == 0):
        counter_entry['lastcount'] = part_count.Value
        return  # machine count rolled over or is not running

    if (counter_entry['lastcount'] == 0):  # first time through...
        counter_entry['lastcount'] = part_count.Value - 1  # only count 1 part

    if part_count.Value > counter_entry['lastcount']:
        for entry in range(counter_entry['lastcount']+1, part_count.Value+1):
            part_count_entry(
                table=counter_entry['table'],
                timestamp=counter_entry['lastread'],
                count=entry,
                machine=counter_entry['Machine'],
                parttype=counter_entry['Part_Type_Map'][str(part_type.Value)]
            )
        counter_entry['lastcount'] = part_count.Value


def part_count_entry(table, timestamp, count, machine, parttype):
    print('{} made a {} ({})'.format(machine, parttype, count))

    # file_path = '/var/local/SQL/{}.sql'.format(
    #     str(int(timestamp)))
    file_path = './tempSQL/{}.sql'.format(
        str(int(timestamp)))

    with open(file_path, "a+") as file:
        sql = ('INSERT INTO {} '
               '(Machine, Part, PerpetualCount, Timestamp) '
               'VALUES ("{}", "{}" ,{} ,{});\n'.format(
                   table, machine, parttype, count, timestamp))
        file.write(sql)


if __name__ == "__main__":

    while True:
        loop(tag_list, ip='10.4.42.135', slot=3, minimum_cycle=.5)
