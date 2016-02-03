import cx_Oracle
import ConfigParser
import string, os, sys
import time

def main():

    # read config
    cf = ConfigParser.ConfigParser() 
    cf.read("conn.conf")
    srvname     = cf.get("db", "srvname")
    username    = cf.get("db", "username")
    userpwd     = cf.get("db", "userpwd")
    foldername  = cf.get("path", "foldername")

    # create dir
    if not os.path.exists(foldername):
        os.mkdir(foldername)    

    t1 = time.time()
    conn = cx_Oracle.connect(username, userpwd, srvname)
    cursor = conn.cursor()  
    cursor.execute (" select * from user_tables ")

    tables = cursor.fetchall()                                  # get all user tables
    for table in tables:
        tablename = table[0]
        try:
            cursor.execute (" select * from " + tablename)          # get one table data
            rows = cursor.fetchall()
            fp = open(".\\" + foldername + "\\" + tablename + ".csv", 'w')
            for row in rows:                           
                a = ",".join("\"" + str(v) + "\"" for v in row)
                fp.writelines(a + '\n')
            print("get " + tablename.ljust(40) + " success, " + str(len(rows)) + " rows.")
            fp.close()
        except:
            print("get " + tablename.ljust(40) + " fail .")
            # raise
    cursor.close()  
    conn.close()
    
    t2 = time.time()
    print("table cost: {} s.").format(t2 - t1)

if __name__ == '__main__':
       main()

