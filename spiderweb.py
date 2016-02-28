import cookielib
import urllib2

cookies = cookielib.LWPCookieJar()
proxies = {"http":"31.173.74.73:8080"}

handlers = [
    urllib2.HTTPHandler(),
    urllib2.HTTPSHandler(),
    urllib2.HTTPCookieProcessor(cookies),
    urllib2.ProxyHandler(proxies)
    ]
opener = urllib2.build_opener(*handlers)

def request(uri):
    req = urllib2.Request(uri)
    req.add_header("User-Agent", "Mozilla/5.0")
    return opener.open(req)

def dump():
    for cookie in cookies:
        print cookie.name, cookie.value


def main():
    uri = 'http://pastebin.com/archive'
    res = request(uri)
    print res.read()
    dump()

    res = request(uri)
    dump()

if __name__=="__main__":
    main()
