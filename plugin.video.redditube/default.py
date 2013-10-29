import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc, xbmcaddon, os, sys
import urlresolver
from metahandler import metahandlers



#ReddiTube - Blazetamer.
addon = xbmcaddon.Addon ('plugin.video.redditube')
URL= 'http://www.reddit.com/r/fullmoviesonyoutube/'

#PATHS
addonPath = addon.getAddonInfo('path')
artPath = addonPath + '/art/'
fanartPath = addonPath + '/art/'

#HOOKS
settings = xbmcaddon.Addon(id='plugin.video.redditube')

#Setup Meta
grab=metahandlers.MetaData()

def GRABMETA(name,year):
        meta = grab.get_meta('movie',name,year,None,None,overlay=6)
        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
        'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
        'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year']}
                
        return infoLabels


#AutoView
def AUTO_VIEW(content):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
                if settings.getSetting('auto-view') == 'true':
                        if content == 'movies':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('movies-view') )
                        else:
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('default-view') )
                else:
                        xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('default-view') )    


#Main Links 
def CATEGORIES():
    
    addDir('[COLOR green]New Putlocker Arrivals[/COLOR]','http://www.reddit.com/r/FullMoviesOnPutLocker/new/.rss',1,artPath+'putlocker.png','','dir')
    addDir('[COLOR red]Whats Hot on Putlocker[/COLOR]','http://www.reddit.com/r/FullMoviesOnPutLocker/.rss',1,artPath+'putlocker.png','','dir')
    addDir('[COLOR blue]Top Putlocker Movies[/COLOR]','http://www.reddit.com/r/FullMoviesOnPutLocker/top/.rss',1,artPath+'putlocker.png','','dir')
    addDir('[COLOR green]New SockShare Arrivals[/COLOR]','http://www.reddit.com/r/FullMoviesonSockshare/new/.rss',1,artPath+'sockshare.png','','dir')
    addDir('[COLOR red]Whats Hot on SockShare[/COLOR]','http://www.reddit.com/r/fullmoviesonsockshare.rss',1,artPath+'sockshare.png','','dir')
    addDir('[COLOR blue]Top SockShare Movies[/COLOR]','www.reddit.com/r/FullMoviesonSockshare/top/.rss',1,artPath+'sockshare.png','','dir')
    addDir('[COLOR red]Whats Hot on YouTube[/COLOR]','http://www.reddit.com/r/fullmoviesonyoutube.rss',1,artPath+'youtube.png','','dir')
    addDir('[COLOR green]New YouTube Arrivals[/COLOR]','http://www.reddit.com/r/fullmoviesonyoutube/new/.rss',1,artPath+'youtube.png','','dir')
    addDir('[COLOR blue]Top YouTube Movies[/COLOR]','http://www.reddit.com/r/fullmoviesonyoutube/top/.rss',1,artPath+'youtube.png','','dir')
    
    AUTO_VIEW('')

#First Links from RSS 
def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        matchlink=re.compile('<item><title>(.+?)</title><link>(.+?)</link><guid isPermaLink="true">.+?</guid>').findall(link)
        inc = 0
        if len(matchlink) > 0:
         for name,url in matchlink:
            if 'youtube' in url:

                inc += 1
                if inc > 8:
                   movie_name = name[:-6]
                   year = name[-6:]
                   movie_name = movie_name.decode('UTF-8','ignore')
                                
                   data = GRABMETA(movie_name,year)
                   thumb = data['cover_url']
                                
                   favtype = 'movie'
                   addDir(name,url,3,thumb,data,favtype)

                   AUTO_VIEW('movies')

            else:
                inc += 1
                if inc > 8:
                 movie_name = name[:-6]
                 year = name[-6:]
                 movie_name = movie_name.decode('UTF-8','ignore')
                                
                 data = GRABMETA(movie_name,year)
                 thumb = data['cover_url']
                                
                 favtype = 'movie'
                 addDir(name,url,2,thumb,data,favtype)

                 AUTO_VIEW('movies')
                
# Second From Source Single Page                
def VIDEOLINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a class="title " href="(.+?)" tabindex="1"').findall(link)
        for url in match:
         movie_name = name[:-6]
         year = name[-6:]
         movie_name = movie_name.decode('UTF-8','ignore')
                                
         data = GRABMETA(movie_name,year)
         thumb = data['cover_url']   
         RESOLVE(name,url,thumb)
  
         AUTO_VIEW('movies')

# Second From Source to YT
def VIDEOLINKSYT(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a class="title " href="(.+?)" tabindex="1"').findall(link)
        for url in match:
         movie_name = name[:-6]
         year = name[-6:]
         movie_name = movie_name.decode('UTF-8','ignore')
                                
         data = GRABMETA(movie_name,year)
         thumb = data['cover_url']
         RESOLVEYT(name,url,thumb)
            
         AUTO_VIEW('movies') 


# Resolve and  Play for Putlocker/Sockshare
def RESOLVE(name,url,iconimage):
         url = url.replace('watch','embed')
         url = urlresolver.HostedMediaFile(url=url).resolve()
         ok=True
         liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
         ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
         xbmc.executebuiltin("XBMC.Notification(Please Wait!,Preparing Your Video,3000)")
         xbmc.sleep(1000)
         xbmc.Player ().play(url, liz, False)

         AUTO_VIEW('')

#Resolve 2 forYouTube

def RESOLVEYT(name,url,iconimage):
         #url = url.replace('file','embed')
         url = urlresolver.HostedMediaFile(url=url).resolve()
         ok=True
         liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
         ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
         xbmc.executebuiltin("XBMC.Notification(Please Wait!,Preparing Your Video,3000)")
         xbmc.sleep(1000)
         xbmc.Player ().play(url, liz, False)         

         AUTO_VIEW('')
            
                

	
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
	INDEX(searchUrl)

	AUTO_VIEW('movies') 
        

                
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



# addLink for direct play
def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
        xbmc.sleep(1000)
        xbmc.Player (xbmc.PLAYER_CORE_PAPLAYER).play(url, liz, False)
        return ok

# Standard addDir
def addDir(name,url,mode,iconimage,labels,favtype):
        contextMenuItems = []
        
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels=labels )
        if favtype == 'movie':
                contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

#Alt addDir
def addDird(name,url,mode,iconimage,labels,favtype):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels=labels )
        if favtype == 'movie':
                contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
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
        VIDEOLINKSYT(url,name)        

       
#For Search Function
elif mode==10:
        print ""+url
        SEARCH(url)



xbmcplugin.endOfDirectory(int(sys.argv[1]))


