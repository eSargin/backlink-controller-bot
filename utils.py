from webutils import GetWebSiteContentWithRetry


def prepareUrl(url):
    if url.startswith('www.'):
        url = url[4:]
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
    return url


def loadProxyList():
    print("Loading Proxy List")
    try:
        webContent = GetWebSiteContentWithRetry(
            "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc")
        if webContent is None:
            return None
        return webContent
    except Exception as e:
        print('loadProxyList Error', e)
        return None


def findTextInDomainContent(domain, domainContent, text):
    print("Domain -> ", domain, " ContainsKey -> ", text)
    # print(domainContent, ' -> ', text)
    # print("TEXT ->", text)
    if text == 'emin':
        print("domainContent ->", toStr(text))
    # print("domainContent ->", domainContent)
    #domaincontent to lower
    text = toStr(text).lower()
    domainContent = toStr(domainContent).lower()
    if domainContent is not None:
        if toStr(domainContent).find(toStr(text)) != -1:
            return True
        else:
            return False
    else:
        return False


def toStr(text):
    if text is None:
        return ''
    else:
        return str(text)


def IsValid(text):
    return text.find('Method Not Allowed') or ('404 Not Found') or ('403 Forbidden') or ('502 Bad Gateway') or('503 Service Temporarily Unavailable') or ('504 Gateway Time-out') or('500 Internal Server Error')


def CheckIsEmpty(text):
    if text is None or text == "" or text == "null" or text == "undefined":
        return True
    else:
        return False