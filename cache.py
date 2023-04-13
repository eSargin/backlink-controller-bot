import random
import threading
import time

import redisoperation
import utils
import webutils

proxyList = []

count = 0
def runcacheproccess(elem):
    # print("algorithm -> ",elem)
    domain = elem[1]
    contains_key = elem[2]
    # print(domain, contains_key)
    response = None
    responseService = ''
    # create WebUtils Class

    if redisoperation.GetKey(domain) is None:
        print('Cache is None : ', domain)
        domain = utils.prepareUrl(domain)
        response = webutils.GetWebSiteContentViaCloudScrape(domain)
        responseService = 'CloudScrape'
        if response is None:
            # create google bot user agent header
            header = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
            response = webutils.GetWebSiteContentWithHeaders(domain, header)
            responseService = 'GoogleBot'
        if response is None:
            response = webutils.GetWebSiteContent(domain)
            responseService = 'Default'
        if response is None:
            response = webutils.GetWebSiteContentWithRetry(domain)
            responseService = 'Retry'
        if response is None:
            print(responseService, ':', domain, ' Response is None!')

            if proxyList is not None:
                global count

                for proxy in proxyList:
                    # f1.lavingaforward.xyz:45211
                    # get random int
                    randomProxy = proxyList[random.randint(0, len(proxyList) - 1)]

                    response = webutils.GetWebSiteContentViaProxy(randomProxy['ip'] + ':' + randomProxy['port'], domain)
                    responseService = 'Proxy'
                    count += 1
                    # check try count

                    if response is not None:
                        break
                    if count == 5:
                        # reset count
                        count = 0
                        #response none
                        response = None
                        # break loop
                        break
        if response is None:
            print(responseService, ':', domain, ' Response is None!')

        else:
            print(responseService, ':', domain, ' Response is OK!')
            redisoperation.SetKeyWithExpire(domain, response, 3600 * 3)
            # 3600*3 = 3 hours
    # else:
    #     print('Cache : ',domain)

    # 3600*3 = 3 hours
