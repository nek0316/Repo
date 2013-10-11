import urllib,urllib2,re,xbmcplugin,xbmcgui

#Free Funny Videos - Blazetamer.

url= 'http://www.freefunnyvideo.org/'

def CATEGORIES():
    addDir('Funny Commercials','http://www.freefunnyvideo.org/funny-commercials/1/',1,"'icon.png'")
    addDir('Funny Animal Videos','http://www.freefunnyvideo.org/funny-animal-videos/1/',1,"'icon.png'")
    addDir('Cartoons and Animation','http://www.freefunnyvideo.org/cartoons-animation/1/',1,"'icon.png'")
    addDir('Comedy Channel','http://www.freefunnyvideo.org/comedy-humor/1/',1,"'icon.png'")
    addDir('Stupid and Funny Videos','http://www.freefunnyvideo.org/stupidandfunny/1/',1,"'icon.png'")
    addDir('Funny Sports Videos','http://www.freefunnyvideo.org/sports-bloopers/1/',1,"'icon.png'")
    addDir('Funny Pranks','http://www.freefunnyvideo.org/funny-pranks/1/',1,"'icon.png'")
    addDir('The Funny Channel','http://www.freefunnyvideo.org/funny-channel/1/',1,"'icon.png'")

def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<div class="videotitle"><a href="(.+?)" >(.+?)</a></div>\r\n<div class="v">\r\n\t\t\t\t<a href=".+?" >\r\n                <img class="i" src="(.+?)"  alt=".+?"></a>').findall(link)
        for url, name, thumbnail in match:
                addDir(name,url,2,thumbnail)
                
def VIDEOLINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile("{   url: \'(.+?)' ").findall(link)
        for url in match:
                 addLink(name,match[0],'')

        

                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param




def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)
        

elif mode==2:
        print ""+url
        VIDEOLINKS(url,name)



xbmcplugin.endOfDirectory(int(sys.argv[1]))


