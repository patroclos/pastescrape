from lxml import html
import spiderweb
import sys, time, traceback, re, os, socks, socket

_verbose = True
webapi=spiderweb
pastefolder = "pastebin"
pastesfolder = "%s/pastes"%pastefolder

if not os.path.isdir(pastefolder):
    os.mkdir(pastefolder)

if not os.path.isdir(pastesfolder):
    os.mkdir(pastesfolder)

def savePaste(pId, content=None):
    if not content:
        content = getPaste(pId)
    
    if pId.startswith("/"):
        pId=pId[1:]
    fd = open("%s/%s"%(pastesfolder,pId),"w")
    fd.write("%s" % content)
    fd.close()
    
    if _verbose:
        print "Saved paste: %s" % pId

def loadPaste(pId):
    path = "%s/%s" % (pastesfolder, pId)
    if not os.path.isfile(path):
        return None
    fd = open(path, "r")
    content = fd.read()
    fd.close()
    return content

def request(url):
    try:
        html=webapi.request(url).read()
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        e = sys.exc_info()[0]
        print "Error: %s" % str(e)
        if _verbose:
            traceback.print_exc()
        return ""
    if html:
        return html
    else:
        if _verbose:
            print "Error: Download is empty - %s" % url
        return ""

def getRecentPastes():
    page = request("http://pastebin.com/archive")
    pTree = html.fromstring(page)
    entrys = pTree.xpath("//table[@class='maintable']/tr/td/a")
    pastes = []
    for l in entrys:
        link = l.get("href")
        if link.startswith("/archive"):
            continue
        pastes.append(link)
    return pastes

def getPaste(pasteID):
    url = "http://pastebin.com/raw.php?i=%s" % pasteID
    return request(url)

def main():
    latest = None
    scanned=0

    while True:
        try:
            recent = getRecentPastes()

            if latest:
                for index in range(len(recent)):
                    if recent[index] == latest:
                        recent=recent[:index-1]
                        break
            if len(recent) > 0:
                latest=recent[0]
                for pid in recent:
                    savePaste(pid)
                    scanned+=1
            else:
                if _verbose:
                    print "[*] Could not find any new pastes"
            time.sleep(90)
            if _verbose:
                print "[*] Getting recent pastes"
        except SystemExit:
            break
        except:
            e = sys.exc_info()[0]
            print "Error: %s" % str(e)
            if _verbose:
                traceback.print_exc()
    print "\n[*] Stopping (%s pastes found)" % (scanned)
if __name__=="__main__":
    main()
