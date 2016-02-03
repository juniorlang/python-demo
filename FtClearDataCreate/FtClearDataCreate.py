# -*- coding: cp936 -*-
import cx_Oracle
import ConfigParser
import string, os, sys

'''
/*******************************
*��֤�����ĳɽ���ϸ���ļ��ṹ V4.1��
*******************************/
//added by czw 20121210
tagFtFieldInfo bzjtrddatatxt[]={
    {1,   "", "date",             "����",           'D', 10, 0, 0},   // yyyy-mm-dd
    {2,   "", "account",          "�ʽ��˻�",       'C', 18, 0, 0},
    {3,   "", "matchno",          "�ɽ���ˮ��",     'C',  8, 0, 0},
    {4,   "", "instrumentid",     "��Լ����",       'C',  6, 0, 0},
    {5,   "", "direction",        "������־",       'C',  1, 0, 0},   // B-S
    {6,   "", "matchqty",         "�ɽ���",         'N', 10, 0, 0},   // ��λ����
    {7,   "", "matchprice",       "�ɽ���",         'N', 15, 3, 0},
    {8,   "", "matchamt",         "�ɽ����",       'N', 15, 3, 0},
    {9,   "", "matchtime",        "�ɽ�ʱ��",       'N',  8, 0, 0},   // hh:mm:ss
    {10,  "", "offsetflag",       "��ƽ��־",       'C',  1, 0, 0},   // O����-Lƽ��
    {11,  "", "hedgeflag",        "Ͷ���ױ���־",   'C',  1, 0, 0},   // SͶ��-H�ױ�
    {12,  "", "tdcloseactual",    "����ƽ��ӯ��",   'N', 15, 3, 0},
    {13,  "", "totalcloseactual", "���ƽ��ӯ��",   'N', 15, 3, 0},
    {14,  "", "fee",              "������",         'N', 15, 3, 0},
    {15,  "", "rpttranscode",     "���ױ���",       'C', 12, 0, 0},
    {16,  "", "market",           "�г�",           'C',  1, 0, 0},
    {17,  "", "memberflag",       "�Ƿ�Ϊ���׻�Ա", 'C',  1, 0, 0},   // Y-N
    {18,  "", "rptno",            "������",         'C', 12, 0, 0},
    {19,  "", "tradeoperid",      "ϯλ��",         'C', 15, 0, 0},
    {20,  "", "moneytype",        "��������",       'C',  3, 0, 0},   // USD CNY HKD
    {21,  "", "matchdate",        "�ɽ�����",       'D', 10, 0, 0}
};
'''

def main():

    cf = ConfigParser.ConfigParser() 
    cf.read("conn.conf")
    srvname = cf.get("db", "srvname")
    username = cf.get("db", "username")
    userpwd = cf.get("db", "userpwd")

    conn = cx_Oracle.connect(username, userpwd, srvname)
    cursor = conn.cursor()  
    cursor.execute (
                 " select to_char(to_date(trddate, 'YYYYMMDD') , 'yyyy-mm-dd') trddate_s,   " +
                 "        fundacct, matchsno, stkcode, " +
                 "        case when BSFLAG = '1U' or BSFLAG = '1X' then 'B' else 'S' end as BUYORSELL,  " +
                 "        matchqty,  matchprice, matchamt, matchtime, " +
                 "        case when BSFLAG = '1U' or BSFLAG = '1W' then 'O' else 'L' end as openorclose,  " +
                 "        case when hedgeflag = '0' then 'S' else 'H' end as hedgeflag,   " +
                 "        0.00 as closeprofit,   " +
                 "        0.00 as closeprofit_d,   " +
                 "        fee, secuid,   " +
                 "        'J' as market,   " +
                 "        'N' as memberflag,   " +
                 "        (select jysorderid from orderrec o where o.ordersno = a.ordersno) as jysorderid,  " +
                 "        mainseat   " +
                 " from match a where market = 'F' and matchamt > 0  ")

    fp = open("trddata.txt", 'w')
    rows = cursor.fetchall()
    for row in rows:
        a = "@".join(str(v) for v in row)
        print a
        fp.writelines(a + '\n')
    print("generate success.")
    fp.close()

    cursor.close ()  
    conn.close ()  

if __name__ == '__main__':
       main()

