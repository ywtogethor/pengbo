#encoding=UTF-8
import MySQLdb
import codecs
import string
import datetime
import sys
import os
import time
import send_mail

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    if (len(sys.argv) != 1):
        print "Usage : ...."
        sys.exit(1)
    db = MySQLdb.connect("rds4f83fd46d4210.mysql.aliyun.com", "dbnwebmaster1", "dbn120410", "dbnwebdb1", charset='utf8');
    cursor = db.cursor()
    result_str = ""

    # 分享统计 
    day_begin_timestamp = int(int(time.time())/int(3600*24))
    day_begin_timestamp = (day_begin_timestamp)*int(3600*24)*1000-8*3600*1000 
    day_end_timestamp = day_begin_timestamp + 24*3600*1000 
    start_timestamp = day_begin_timestamp + 12*3600*1000
    end_timestamp = day_begin_timestamp + 36*3600*1000
    
    sql = 'select count(id) from dbn_purchase_qualification where beginTime=' + str(start_timestamp) + ' and endTime=' + str(end_timestamp);
    print sql
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
      result_str += "分享人数：" + str(row[0]) + "\n"
    
    # 订单数量
    # 秒杀产品付款订单
    sql = "select count(A.id) from dbn_product_order as A,dbn_product_order_info as B,dbn_seller_goods as C where C.flash_start_time >=" +  str(day_begin_timestamp) + ' and C.flash_start_time <= ' + str(day_end_timestamp) + ' and A.id=B.order_id and B.goods_id=C.id and A.status>=2 and A.status<99'
    print sql
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
      result_str += "成交订单数：" + str(row[0]) + "\n"
    
    # 秒杀产品未付款订单
    sql = "select count(A.id) from dbn_product_order as A,dbn_product_order_info as B,dbn_seller_goods as C where C.flash_start_time >=" +  str(day_begin_timestamp) + ' and C.flash_start_time <= ' + str(day_end_timestamp) + ' and A.id=B.order_id and B.goods_id=C.id and A.status<2'
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
      result_str += "未成交订单数：" + str(row[0]) + "\n"

    subject = str(time.strftime('%Y-%m-%d',time.localtime(time.time()))) + "-秒杀数据" 
    #mailto_list=['lijh@dabanniu.com', 'qiaohui@dabanniu.com', 'qiugl@dabanniu.com', 'zhihui@dabanniu.com']
    mailto_list=['lijh@dabanniu.com', 'qiaohui@dabanniu.com', 'qiugl@dabanniu.com', 'zhihui@dabanniu.com']
    send_mail.send_mail(mailto_list, subject.encode("gbk"), result_str.encode("gbk"))
    db.close();

