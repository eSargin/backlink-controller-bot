import redis
import mysql.connector
import database

# Redis connection

r = redis.Redis(host='localhost', port=6379, db=0)

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="user",
    password="passwd",
    database="db"
)


def GetKey(key):
    return r.get(key)


def SetKey(key, value):
    r.set(key, value)


def SetKeyWithExpire(key, value, expire):
    r.set(key, value, ex=expire)


def DeleteKey(key):
    r.delete(key)


def GetAllWebsites(userId):
    print("Redis GetAllWebsites")
    # Get all websites

    siteList = database.GetBacklinkList(mydb, userId)
    return siteList


def RemoveCacheAll(userId):
    print("RemoveCacheAll")
    # Get all websites
    websites = GetAllWebsites(userId)
    for elem in websites:
        domain = elem[1]
        DeleteKey(domain)
        print("RemoveCacheAll -> ", domain)


def RemoveCacheAllById(userId, websiteId):
    print("RemoveCacheAllById")
    # Get all websites
    websites = database.GetBacklinkListViaId(websiteId, mydb, userId)
    for elem in websites:
        domain = elem[1]
        DeleteKey(domain)
        print("RemoveCacheAllById -> ", domain)
