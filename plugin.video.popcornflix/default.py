import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc, xbmcaddon, os, sys

from meta import TheTVDBInfo, set_movie_meta, download_movie_meta, set_tv_show_meta, download_tv_show_meta, meta_exist

#Popcorn Flix - Blazetamer.
addon_id = 'plugin.video.popcornflix'
URL= 'http://popcornflix.com'


def CATEGORIES():
    addDir('New Arrivals','http://popcornflix.com/New-Arrivals-movies/',1,'')
    addDir('Most Popular','http://popcornflix.com/most-popular-movies/',1,'')
    addDir('Rock Stars','http://popcornflix.com/Rock-Star-movies',3,'')
    addDir('Action/Thriller','http://popcornflix.com/Action/Thriller-movies',3,'')
    addDir('Comedy','http://popcornflix.com/Action/Thriller-movies',3,'')
    addDir('Horror Movies','http://popcornflix.com/Horror-movies',3,'')
    addDir('Drama','http://popcornflix.com/Drama-movies',3,'')
    addDir('Romance','http://popcornflix.com/Romance-movies',3,'')
    addDir('Kids/Family','http://popcornflix.com/Family/Kids-movies',3,'')
    addDir('TV Series','http://popcornflix.com/TV-Series',3,'')
    addDir('Urban Movies','http://popcornflix.com/Urban-movies',3,'')
    addDir('Documentary/Shorts','http://popcornflix.com/Documentary/Shorts-movies',3,'')
    addDir('Bollywood','http://popcornflix.com/Bollywood-movies',3,'')

def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)">\n\t\t  <img width="184" height="256" src="(.+?)" alt="(.+?)"/>').findall(link)
        for url,thumbnail,name in match:
                addDir(name,URL+url,2,thumbnail)
                
def VIDEOLINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('"flashContent" data-videosrc="(.+?)" data-videodata="').findall(link)
        matchyear=re.compile('<span class="year">(.+?)</span>').findall(link)
        for url in match:
            for year in matchyear:
                 addLink(name+year,match[0],'')


def INDEX_DEEP(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)"><img width="184" height="256" src="(.+?)" alt="(.+?)">').findall(link)
        for url,thumbnail,name in match:
                addDir(name,URL+url,2,thumbnail)                 

        

                
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
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.sleep(1000)
        xbmc.Player ().play(url, liz, False)
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


elif mode==3:
        print ""+url
        INDEX_DEEP(url)        



xbmcplugin.endOfDirectory(int(sys.argv[1]))


