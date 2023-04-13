import time


def UpdateBacklinkList(webSiteId, status, mydb, userId):
    mycursor = mydb.cursor()
    insertTime = int(time.time())
    sql = "UPDATE backlink_list SET status = %s,last_control_date=%s WHERE id = %s and user_id = %s"
    val = (status, insertTime, webSiteId, userId)
    mycursor.execute(sql, val)
    mydb.commit()


# 1 Backlink Mevcut 2 Mevcut Değil 3 WebSite Error 4 Dns Error
def AddLog(domain, contains_key, status, mydb, userId):
    mycursor = mydb.cursor()
    insertTime = int(time.time())
    sql = "INSERT INTO backlink_log (domain, contains_key, status,insert_time,user_id) VALUES (%s, %s, %s,%s,%s)"
    val = (domain, contains_key, status, insertTime, userId)
    mycursor.execute(sql, val)
    mydb.commit()




def GetBacklinkList(mydb, userId):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM backlink_list where user_id = '" + str(userId) + "' and is_active = 1")
    myresult = mycursor.fetchall()
    mydb.close()
    return myresult


def GetBacklinkListViaId(id, mydb, userId):
    print("GetBacklinkListViaId")
    print("id -> ", id)
    print("userId -> ", userId)

    mycursor = mydb.cursor()
    sql = "SELECT * FROM backlink_list where id = %s and user_id = '" + str(userId) + "'"
    val = (str(id),)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    return myresult
