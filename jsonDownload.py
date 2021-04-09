import urllib.request, string, ast, os, json

def dl_urlReqOpen(URL):
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"
    request = urllib.request.Request(URL, headers = headers)
    return urllib.request.urlopen(request)

def dl_json2dict(URL):
    with dl_urlReqOpen(URL) as url:
        data = json.loads(url.read().decode())
        return data