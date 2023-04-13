import threading
import urllib.error
import urllib.parse
import urllib.request


import utils

lock = threading.Lock()


def GetWebSiteContent(url):
    try:
        lock.acquire()
        response = urllib.request.urlopen(url, timeout=3)
        webContent = response.read()
        return webContent
    except Exception as e:
        return None
    finally:
        lock.release()


def GetWebSiteContentWithRetry(url):
    try:
        import requests
        from urllib3.exceptions import InsecureRequestWarning
        from urllib3 import disable_warnings
        lock.acquire()
        disable_warnings(InsecureRequestWarning)

        page = requests.get(url, verify=False)

        return page.content
    except Exception as e:
        print('GetWebSiteContentWithRetry', e)
        return None
    finally:
        lock.release()


def GetWebSiteContentWithHeaders(url, headers):
    # print("GetWebSiteContentWithHeaders", url)
    try:
        lock.acquire()
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=3)
        webContent = response.read()
        return webContent
    except Exception as e:
        print('GetWebSiteContentWithHeaders Error', url)
        return None
    finally:
        lock.release()


def GetWebSiteContentViaCloudScrape(url):
    import cfscrape
    from fake_useragent import UserAgent
    ua = UserAgent()
    try:
        lock.acquire()
        s = cfscrape.create_scraper()
        s.options(timeout=3, url=url)
        k = s.get(url, headers={'User-Agent': ua.random})
        stringContent = k.content.decode('utf-8')
        #print(stringContent)
        if utils.IsValid(stringContent) != -1:
            return None
        return k.content
    except Exception as e:
        print("Error CloudScrapper : ", e)
        return None
    finally:
        lock.release()


def GetWebSiteContentViaProxy(proxy, url):

    import requests
    try:
        lock.acquire()
        print("Proxy : ", proxy, " Url : ", url)
        page = requests.get(url,
                            proxies={"http": proxy, "https": proxy}, timeout=3, verify=False)
        return page.text
    except Exception as e:
        print("Error GetWebSiteContentViaProxy : ", e)
    finally:
        lock.release()
