import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc, xbmcaddon, os, sys
import urlresolver
import cookielib
import downloader
import extract
import time,re
import datetime
import shutil
from metahandler import metahandlers
from resources.modules import main
from resources.modules import live
from resources.utils import buggalo


from addon.common.addon import Addon
from addon.common.net import Net
net = Net(http_debug=True)
        
addon_id = 'plugin.video.moviedb'
addon = main.addon
ADDON = xbmcaddon.Addon(id='plugin.video.moviedb')

#PATHS
settings = xbmcaddon.Addon(id='plugin.video.moviedb')

if settings.getSetting('theme') == '0':
    artwork = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/', ''))
    fanart = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/fanart/fanart.jpg', ''))
else:
    artwork = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/', ''))
    fanart = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart/fanart.jpg', ''))

    

URL= 'http://popcornflix.com'

popartpath = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/popcornflix/images/', ''))



#HOOKS
settings = xbmcaddon.Addon(id='plugin.video.moviedb')






def POPCATS():
    
    main.addDir('[COLOR blue]New Arrivals[/COLOR]','http://popcornflix.com/New-Arrivals-movies/','flixindex',popartpath+'newarrival.png','','movies')
    main.addDir('[COLOR orange]Most Popular[/COLOR]','http://popcornflix.com/most-popular-movies/','flixindex',popartpath+'mostpopular.png','','movies')
    main.addDir('[COLOR blue]Rock Stars[/COLOR]','http://popcornflix.com/Rock-Star-movies','flixindexdeep',popartpath+'rockstars.png','','other')
    main.addDir('[COLOR orange]Action/Thriller[/COLOR]','http://popcornflix.com/Action/Thriller-movies','flixindexdeep',popartpath+'thriller.png','','movies')
    main.addDir('[COLOR blue]Comedy[/COLOR]','http://www.popcornflix.com/Comedy-movies','flixindexdeep',popartpath+'comedy.png','','movies')
    main.addDir('[COLOR orange]Horror Movies[/COLOR]','http://popcornflix.com/Horror-movies','flixindexdeep',popartpath+'horror.png','','movies')
    main.addDir('[COLOR blue]Drama[/COLOR]','http://popcornflix.com/Drama-movies','flixindexdeep',popartpath+'drama.png','','movies')
    main.addDir('[COLOR orange]Romance[/COLOR]','http://popcornflix.com/Romance-movies','flixindexdeep',popartpath+'romance.png','','movies')
    main.addDir('[COLOR blue]Kids/Family[/COLOR]','http://popcornflix.com/Family/Kids-movies','flixindexdeep',popartpath+'kidfamily.png','','movies')
    main.addDir('[COLOR orange]TV Series[/COLOR]','http://popcornflix.com/TV-Series','flixindexdeep',popartpath+'tvseries.png','','tv')
    main.addDir('[COLOR blue]Urban Movies[/COLOR]','http://popcornflix.com/Urban-movies','flixindexdeep',popartpath+'urbanmovies.png','','movies')
    main.addDir('[COLOR orange]Documentary/Shorts[/COLOR]','http://popcornflix.com/Documentary/Shorts-movies','flixindexdeep',popartpath+'documentary.png','','movies')
    main.addDir('[COLOR blue]Bollywood[/COLOR]','http://popcornflix.com/Bollywood-movies','flixindexdeep',popartpath+'bollywood.png','','movies')
    main.addDir('[COLOR red][B]Search[/B] >>>[/COLOR]','http://www.popcornflix.com/search?query=','popcornsearch',popartpath+'search.png','','')
    main.AUTO_VIEW('')
        
def FLIXINDEX(url,favtype):
          params = {'url':url, 'favtype':favtype}
          link = net.http_GET(url).content
          #match=re.compile('<a href="(.+?)">\n\t\t  <img width="184" height="256" src="(.+?)" alt="(.+?)"/>').findall(link)
          match=re.compile('<a href="(.+?)">\n                    <img width="184" height="256" src="(.+?)" alt="(.+?)"/>').findall(link)
          for url,thumb,name in match:
                    url = URL + url
                    data = main.GRABMETA(name,'')
                    thumb = data['cover_url']
                    favtype = 'movies'
                    main.addMDCDir(name,url,'flixvideolinks',thumb,data,favtype)
                    main.AUTO_VIEW('movies')
                    

                
def FLIXVIDEOLINKS(name,url,thumb,favtype):
        params = {'url':url, 'name':name, 'thumb':thumb, 'favtype':favtype}  
        link = net.http_GET(url).content
        match=re.compile('id="flashContent" data-videosrc="(.+?)"\n         data-videodata="(.+?)"></div>').findall(link)
        matchyear=re.compile('<span class="year">(.+?)</span>').findall(link)
        for url,url2 in match:
             #if 'undefined' in url:
                  url = url2
                  for year in matchyear:
                       link = net.http_GET(url).content
                       url = URL + url
                       match4=re.compile('"poster":"(.+?)","slider":".+?","duration":.+?,"rating":"(.+?)","language":".+?","cuepoints":".+?","urls":{".+?":"(.+?)"}').findall(link)
                       for thumb,rating,url in match4:
                              #replace odd strings
                              thumb = thumb.replace("\/","/")
                              url = url.replace("\/","/")
                              mainimg = thumb
                              favtype = 'movies'
                              link = net.http_GET(url).content
                              match3=re.compile('RESOLUTION=864x480\r\n(.+?)\r\n#').findall(link)
                              for url in match3:
                                   live.addDir(name + year + ' Rated- ' +rating,url,'flixaddlink',thumb,'',fanart)
                                   main.AUTO_VIEW('movies')



def FLIXINDEX_DEEP(url,favtype):
        params = {'url':url,'favtype':favtype}  
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)"><img width="184" height="256" src="(.+?)" alt="(.+?)"></a>').findall(link)
        for url,thumb,name in match:
                    url = URL + url
                    data = main.GRABMETA(name,'')
                    thumb = data['cover_url'] 
                    main.addMDCDir(name,url,'flixvideolinks',thumb,data,favtype)
                    main.AUTO_VIEW('movies')
               
	
#Start Ketboard Function                
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default


#Start Search Function
def POPSEARCH(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching  PoPcornflix" )
	# if blank or the user cancelled the keyboard, return
	if ( not vq ): return False, 0
	# we need to set the title to our query
	title = urllib.quote_plus(vq)
	searchUrl += title 
	print "Searching URL: " + searchUrl 
	flixindex,flixindex_DEEP(searchUrl,'')
        

                


def FLIXADDLINK(name,url,thumb):
         #params = {'url':url, 'name':name, 'thumb':thumb}      
         url= url
         ok=True
         liz=xbmcgui.ListItem(name, iconImage=thumb,thumbnailImage=thumb); liz.setInfo( type="Video", infoLabels={ "Title": name } )
         ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
         xbmc.executebuiltin("XBMC.Notification(Building Video File!,Please Wait,3000)")
         xbmc.sleep(1000)
         xbmc.Player ().play(url, liz, False)

         
             

def addDir(name,url,mode,thumb):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


def addlinkDir(name,url,mode,thumb):
     u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(thumb)
     liz = xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
     liz.setProperty("IsPlayable","true")
     xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = False)

     
              








