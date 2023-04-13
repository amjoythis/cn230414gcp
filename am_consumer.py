import certifi
import ssl
from urllib.request import urlopen, Request
from http.client import HTTPResponse

import bs4
from bs4 import BeautifulSoup

USER_AGENT_STRING_MOZ47 = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
USER_AGENT_STRING_GOOGLE_NEWS = 'Googlebot-News'
REFERER_GOOGLE = "https://www.google.com"
MARK_MEDIA = ".4cdn.org"

def buildDictOfHeadersToFakeAgent(
    pUserAgent:str=USER_AGENT_STRING_MOZ47
):
    ret = dict()
    ret['User-Agent'] = pUserAgent
    return ret
# def buildDictOfHeadersToFakeAgent

def buildDictOfHeadersToFakeReferer(
    pStrReferer:str=REFERER_GOOGLE
):
    ret = dict()
    ret['Referer'] = pStrReferer
    return ret
# def buildDictOfHeadersToFakeReferer

def combineAllDicts(*pDicts):
    ret = dict()
    for d in pDicts:
        ret.update(d)
        # if
    # for

    return ret
# def combineAllDicts

def findAnchorsAtUrl(pUrl):
    listHrefs = []

    strContent = consumeUrl(pUrl)
    bs = BeautifulSoup(
        strContent,
        "html5lib"
    )
    theAs = bs.findAll("a")
    for a in theAs:
        if(a.attrs):
            bWithHref = "href" in a.attrs.keys()
            if(bWithHref):
                listHrefs.append(
                    {
                        "anchor":a.text,
                        "href":a["href"]
                    }
                )
            # if
        # if
    # for
    return listHrefs
# def findAnchorsAtUrl

def findMediaUrlsIn(pListOfAnchors):
    ret = []
    for a in pListOfAnchors:
        anchor = a['anchor']
        href = a['href']
        bMedia = MARK_MEDIA in href
        if(bMedia):
            a['href'] = "https:"+a['href']
            ret.append(a)
        # if
    # for
    return ret
# def findMediaUrlsIn

def consumeUrl(
    pUrl:str,
    pbResponseAsBytes:bool=False,
    pStrEncodingIfResponseAsString:str="UTF-8",
    pStrUserAgentString:str = USER_AGENT_STRING_MOZ47,
    pStrReferer:str = REFERER_GOOGLE
):
    strWhereIsCAfile = certifi.where()
    sslContext = ssl.create_default_context(cafile=strWhereIsCAfile)

    userAgent = buildDictOfHeadersToFakeAgent(pStrUserAgentString)
    referer = buildDictOfHeadersToFakeReferer(pStrReferer)
    allHeaders = combineAllDicts(userAgent, referer)
    #Cookie: cf_clearance=wsuokqrPMyqgJfj0lIAQioc7WMV03vqS1b3mNbpSWBM-1670839993-0-160

    req:Request = Request(
        url = pUrl,
        headers=allHeaders
    )

    #req.add_header("cookie", "cf_clearance=wsuokqrPMyqgJfj0lIAQioc7WMV03vqS1b3mNbpSWBM-1670839993-0-160")
    req.add_header("cf_clearance", "wsuokqrPMyqgJfj0lIAQioc7WMV03vqS1b3mNbpSWBM-1670839993-0-160")
    req.add_header("Accept-Encoding", "text/html")

    response:HTTPResponse = urlopen(
        req,
        context = sslContext,
    )

    theBytes = response.read()

    if(pbResponseAsBytes):
        return theBytes
    else:
        strTheResponse = str(
            theBytes,
            pStrEncodingIfResponseAsString
        )
        return strTheResponse
    # if-else
# def consumeUrl

def get_google_organic_result_anchors(
    pListAnchors:list
):
    ret = list()
    for anchor in pListAnchors:
        href:str  = anchor['href']
        iWhereDoesHttpsStart:int = href.find("https://")
        if(iWhereDoesHttpsStart!=-1):
            href_starting_at_https:str = href[iWhereDoesHttpsStart:]
            iWhereDoesVedStart:int = href_starting_at_https.find("&ved=")
            href_clean:str = href_starting_at_https[0:iWhereDoesVedStart]
            b_google:bool = href_clean.find(".google.com/")!=-1
            b_empty_anchor:bool = anchor['anchor']==""

            if(not b_google and not b_empty_anchor):
                a = {
                    'href' : href_clean,
                    'anchor' : anchor['anchor']
                }
                ret.append(a)
            # if
        # if
    # for
    return ret
# def