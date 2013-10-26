import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc, xbmcaddon, os, sys
import urlresolver

#from meta import TheTVDBInfo, set_movie_meta, download_movie_meta, set_tv_show_meta, download_tv_show_meta, meta_exist

#Popcorn Flix - Blazetamer.
addon = xbmcaddon.Addon ('plugin.video.popcornflix')
URL= 'http://popcornflix.com'
#_plugin = xbmcaddon.Addon(id=addon_id)
#PATHS

addonPath = addon.getAddonInfo('path')
artPath = addonPath + '/art/'
fanartPath = addonPath + '/art/'

#HOOKS
settings = xbmcaddon.Addon(id='plugin.video.popcornflix')



def CATEGORIES():
    
    addDir('[COLOR blue]New Arrivals[/COLOR]','http://popcornflix.com/New-Arrivals-movies/',1,artPath+'newarrival.png')
    addDir('[COLOR orange]Most Popular[/COLOR]','http://popcornflix.com/most-popular-movies/',1,artPath+'mostpopular.png')
    addDir('[COLOR blue]Rock Stars[/COLOR]','http://popcornflix.com/Rock-Star-movies',3,artPath+'rockstars.png')
    addDir('[COLOR orange]Action/Thriller[/COLOR]','http://popcornflix.com/Action/Thriller-movies',3,artPath+'thriller.png')
    addDir('[COLOR blue]Comedy[/COLOR]','http://www.popcornflix.com/Comedy-movies',3,artPath+'comedy.png')
    addDir('[COLOR orange]Horror Movies[/COLOR]','http://popcornflix.com/Horror-movies',3,artPath+'horror.png')
    addDir('[COLOR blue]Drama[/COLOR]','http://popcornflix.com/Drama-movies',3,artPath+'drama.png')
    addDir('[COLOR orange]Romance[/COLOR]','http://popcornflix.com/Romance-movies',3,artPath+'romance.png')
    addDir('[COLOR blue]Kids/Family[/COLOR]','http://popcornflix.com/Family/Kids-movies',3,artPath+'kidfamily.png')
    addDir('[COLOR orange]TV Series[/COLOR]','http://popcornflix.com/TV-Series',3,artPath+'tvseries.png')
    addDir('[COLOR blue]Urban Movies[/COLOR]','http://popcornflix.com/Urban-movies',3,artPath+'urbanmovies.png')
    addDir('[COLOR orange]Documentary/Shorts[/COLOR]','http://popcornflix.com/Documentary/Shorts-movies',3,artPath+'documentary.png')
    addDir('[COLOR blue]Bollywood[/COLOR]','http://popcornflix.com/Bollywood-movies',3,artPath+'bollywood.png')
    addDir('[COLOR red][B]Search[/B] >>>[/COLOR]','http://www.popcornflix.com/search?query=',10,artPath+'search.png')

def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)">\n\t\t  <img width="184" height="256" src="(.+?)" alt="(.+?)"/>').findall(link)
        for url,iconimage,name in match:
                addDir(name,URL+url,2,iconimage)
                
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
                 addLink(name+year,url,'')


def INDEX_DEEP(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)"><img width="184" height="256" src="(.+?)" alt="(.+?)">').findall(link)
        for url,iconimage,name in match:
                addDir(name,URL+url,2,iconimage)
                
#Set View Function
def set_view(content='none',view_mode=50,do_sort=False):
	h=int(sys.argv[1])
	if (content is not 'none'): xbmcplugin.setContent(h, content)
	if (tfalse(addst("auto-view"))==True): xbmc.executebuiltin("Container.SetViewMode(%s)" % str(view_mode))

	
#Start Ketboard Function                
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default


#Start Search Function
def SEARCH(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching  PoPcornflix" )
	# if blank or the user cancelled the keyboard, return
	if ( not vq ): return False, 0
	# we need to set the title to our query
	title = urllib.quote_plus(vq)
	searchUrl += title 
	print "Searching URL: " + searchUrl 
	INDEX,INDEX_DEEP(searchUrl)
        

                
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
        liz=xbmcgui.ListItem(name,iconImage=iconimage, thumbnailImage=iconimage); liz.setInfo('video',{'Title':name,'Genre':'Live','Studio':name})
        #liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.sleep(1000)
        xbmc.Player (xbmc.PLAYER_CORE_PAPLAYER).play(url, liz, False)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        xbmc.executebuiltin("Container.SetViewMode(500)")
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
       
#For Search Function
elif mode==10:
        print ""+url
        SEARCH(url)



xbmcplugin.endOfDirectory(int(sys.argv[1]))


