import json
from multiprocessing import Pool, cpu_count
from timeit import default_timer as timer
import mysql.connector
import cache
import database
import redisoperation
import utils
from cache import runcacheproccess
from database import GetBacklinkList


def startServiceSingle(userId, websiteId):
    print("Redis Test")
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="user",
        password="passwd",
        database="db"
    )

    siteList = database.GetBacklinkListViaId(websiteId, mydb, userId)

    if siteList is None:
        print("Site List is Empty")
        return False

    StartCacheProccess(siteList)

    StartService(siteList, userId)

    return True


def startService(userId):
    print("Redis Test")
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="user",
        password="passwd",
        database="db"
    )

    siteList = GetBacklinkList(mydb, userId)

    if siteList is None:
        print("Site List is Empty")
        return False

    StartCacheProccess(siteList)

    StartService(siteList, userId)

    return True


def runserviceproccess(elem, userId):
    print("Service Proccess Starting..")
    print("Id -> ", id)
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="user",
        password="passwd",
        database="db"
    )

    pId = elem[0]
    domain = elem[1]
    containsKey = elem[2]
    domain = utils.prepareUrl(domain)
    domainContent = redisoperation.GetKey(domain)
    # print("Domain -> ", domain, " ContainsKey -> ", containsKey)

    exists = utils.findTextInDomainContent(domain, domainContent, containsKey)
    if exists:
        database.AddLog(domain, containsKey, 1, mydb, userId)
        database.UpdateBacklinkList(pId, 1, mydb, userId)
        print("Backlink Mevcut : ", domain)
    else:
        database.AddLog(domain, containsKey, 2, mydb, userId)
        database.UpdateBacklinkList(pId, 2, mydb, userId)
        print("Backlink Yok : ", domain, " ContainsKey -> ", containsKey)

def StartService(WEBSITE_LIST, userId):
    print("Service Starting..")
    start = timer()
    print(f'starting computations on {cpu_count()} cores')
    if len(WEBSITE_LIST) == 1:
        runserviceproccess(WEBSITE_LIST[0], userId)
        return
    cacheServicePool = Pool(50)

    cacheServicePool.starmap(runserviceproccess,  [(elem, userId) for elem in WEBSITE_LIST])
    cacheServicePool.close()
    end = timer()
    print(f'elapsed time: {end - start}')
    print("Service End")


domainList = []


# Cachleme işlemini 25 thread ile yapar belki de yapmaz :D
def StartCacheProccess(WEBSITE_LIST):
    start = timer()
    print(f'starting computations on {cpu_count()} cores')
    totalCount = len(WEBSITE_LIST)
    for elem in WEBSITE_LIST:
        domain = elem[1]
        if domain not in domainList:
            domainList.append(domain)
    print("Total Count : ", totalCount)
    print("Distinct Count : ", len(domainList))
    print("CACHE START")
    cachePool = Pool(20)
    cachePool.map(runcacheproccess, WEBSITE_LIST)
    cachePool.close()
    # close the process pool
    end = timer()
    print(f'elapsed time: {end - start}')
    print("CACHE END")
