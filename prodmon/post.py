import glob
import os
import yaml
from time import sleep

import mysql.connector


def executesql():

    dbconfig = post_config['dbconfig']
    sqldir = post_config['sqldir']

    cnx = mysql.connector.connect(**dbconfig)
    cursor = cnx.cursor()

    for filepath in glob.iglob(sqldir+'*.sql'):
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                sql = line.strip()
                cursor.execute(sql)
                print(sql)
        cnx.commit()
        os.remove(filepath)

    cursor.close()
    cnx.close()


if __name__ == '__main__':

    with open(r'configs/example-config.yml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    post_config = config['post']

    while True:
        executesql()
        sleep(2)
