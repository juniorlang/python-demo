# -*- coding: cp936 -*-
import cx_Oracle
import ConfigParser
import string, os, sys

'''
/*******************************
*保证金中心成交明细表文件结构 V4.1版
*******************************/
//added by czw 20121210
tagFtFieldInfo bzjtrddatatxt[]={
    {1,   "", "date",             "日期",           'D', 10, 0, 0},   // yyyy-mm-dd
    {2,   "", "account",          "资金账户",       'C', 18, 0, 0},
    {3,   "", "matchno",          "成交流水号",     'C',  8, 0, 0},
    {4,   "", "instrumentid",     "合约代码",       'C',  6, 0, 0},
    {5,   "", "direction",        "买卖标志",       'C',  1, 0, 0},   // B-S
    {6,   "", "matchqty",         "成交量",         'N', 10, 0, 0},   // 单位：手
    {7,   "", "matchprice",       "成交价",         'N', 15, 3, 0},
    {8,   "", "matchamt",         "成交金额",       'N', 15, 3, 0},
    {9,   "", "matchtime",        "成交时间",       'N',  8, 0, 0},   // hh:mm:ss
    {10,  "", "offsetflag",       "开平标志",       'C',  1, 0, 0},   // O开仓-L平仓
    {11,  "", "hedgeflag",        "投机套保标志",   'C',  1, 0, 0},   // S投机-H套保
    {12,  "", "tdcloseactual",    "盯日平仓盈亏",   'N', 15, 3, 0},
    {13,  "", "totalcloseactual", "逐笔平仓盈亏",   'N', 15, 3, 0},
    {14,  "", "fee",              "手续费",         'N', 15, 3, 0},
    {15,  "", "rpttranscode",     "交易编码",       'C', 12, 0, 0},
    {16,  "", "market",           "市场",           'C',  1, 0, 0},
    {17,  "", "memberflag",       "是否为交易会员", 'C',  1, 0, 0},   // Y-N
    {18,  "", "rptno",            "报单号",         'C', 12, 0, 0},
    {19,  "", "tradeoperid",      "席位号",         'C', 15, 0, 0},
    {20,  "", "moneytype",        "货币类型",       'C',  3, 0, 0},   // USD CNY HKD
    {21,  "", "matchdate",        "成交日期",       'D', 10, 0, 0}
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

