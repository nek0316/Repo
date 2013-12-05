
# 2Movies Chia Module by: Blazetamer


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon,mechanize,main

from metahandler import metahandlers


from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
net = Net()
try:
     import StorageServer
except:
     import storageserverdummy as StorageServer



#Define common.addon
addon_id = 'plugin.video.twomovies'
addon = Addon(addon_id, sys.argv)

# Cache for favorites  Whenever  do them 
cache = StorageServer.StorageServer("Two Movies", 0)



# Global Stuff
settings = xbmcaddon.Addon(id=addon_id)
artwork = xbmc.translatePath(os.path.join('http://rowthreemedia.com/xbmchub/2movies/art/', ''))
grab=metahandlers.MetaData()
net = Net()
def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")


def CHIACATS():

    
     main.addDir('Latest Anime Episodes','http://www.chia-anime.com/','chialatest','','','dir')
     main.addDir('Anime by Genres','http://www.chia-anime.com/?genre=','chiagenres','','','dir')
     main.addDir('A-Z','none','chiaalph','','','dir')
          
     main.AUTO_VIEW('')    


def CHIALATEST(url):
     link = net.http_GET(url).content
     match=re.compile('<h3><a href="(.+?)" rel="bookmark" title="(.+?)">.+?</a></h3></div></center><div><span class="video-episode">.+?</span></div><div class="thumb" style="background: #000 url(.+?) no-repeat').findall(link)
     for url,name,thumb in match:
          thumb = thumb.replace('(','')
          thumb = thumb.replace(')','')
          main.addDir(name,url,'chiavidpage',thumb,'','')
          main.AUTO_VIEW('movies')

def CHIAVIDPAGE(url,name):
     link = net.http_GET(url).content
     matchvid=re.compile('Watch via Mobile</font></a><a id="download" target="_blank" href="(.+?)">.+?MP4 Video format').findall(link)
     for url in matchvid:
          link = net.http_GET(url).content
          matchsource = re.compile('class="bttn green" href="(.+?)">Save mp4 as Link</a>').findall(link)
          for url in matchsource:
                     CHIARESOLVE(name,url,'')          


def CHIAALPH():
     main.addDir('#','http://www.chia-anime.com/alpha/#','chiaalphmain','','','dir')
     main.addDir('A','http://www.chia-anime.com/alpha/A','chiaalphmain','','','dir')
     main.addDir('B','http://www.chia-anime.com/alpha/B','chiaalphmain','','','dir')
     main.addDir('C','http://www.chia-anime.com/alpha/C','chiaalphmain','','','dir')
     main.addDir('D','http://www.chia-anime.com/alpha/D','chiaalphmain','','','dir')
     main.addDir('E','http://www.chia-anime.com/alpha/E','chiaalphmain','','','dir')
     main.addDir('F','http://www.chia-anime.com/alpha/F','chiaalphmain','','','dir')
     main.addDir('G','http://www.chia-anime.com/alpha/G','chiaalphmain','','','dir')
     main.addDir('H','http://www.chia-anime.com/alpha/H','chiaalphmain','','','dir')
     main.addDir('I','http://www.chia-anime.com/alpha/I','chiaalphmain','','','dir')
     main.addDir('J','http://www.chia-anime.com/alpha/J','chiaalphmain','','','dir')
     main.addDir('K','http://www.chia-anime.com/alpha/K','chiaalphmain','','','dir')
     main.addDir('L','http://www.chia-anime.com/alpha/L','chiaalphmain','','','dir')
     main.addDir('M','http://www.chia-anime.com/alpha/M','chiaalphmain','','','dir')
     main.addDir('N','http://www.chia-anime.com/alpha/N','chiaalphmain','','','dir')
     main.addDir('O','http://www.chia-anime.com/alpha/O','chiaalphmain','','','dir')
     main.addDir('P','http://www.chia-anime.com/alpha/P','chiaalphmain','','','dir')
     main.addDir('Q','http://www.chia-anime.com/alpha/Q','chiaalphmain','','','dir')
     main.addDir('R','http://www.chia-anime.com/alpha/R','chiaalphmain','','','dir')
     main.addDir('S','http://www.chia-anime.com/alpha/S','chiaalphmain','','','dir')
     main.addDir('T','http://www.chia-anime.com/alpha/T','chiaalphmain','','','dir')
     main.addDir('U','http://www.chia-anime.com/alpha/U','chiaalphmain','','','dir')
     main.addDir('V','http://www.chia-anime.com/alpha/V','chiaalphmain','','','dir')
     main.addDir('W','http://www.chia-anime.com/alpha/W','chiaalphmain','','','dir')
     main.addDir('X','http://www.chia-anime.com/alpha/X','chiaalphmain','','','dir')
     main.addDir('Y','http://www.chia-anime.com/alpha/Y','chiaalphmain','','','dir')
     main.addDir('Z','http://www.chia-anime.com/alpha/Z','chiaalphmain','','','dir')
          
        
     main.AUTO_VIEW('')

def CHIAGENRES(url):
         genreurl = 'http://www.chia-anime.com/'      
         link = net.http_GET(url).content
         match = re.compile('<a href="/(.+?)">(.+?)</a> - ').findall(link)
         for url,name in match:
              url = genreurl + url
              main.addDir(name,url,'chiagenremain','','','dir')

              
def CHIAGENREMAIN(url):
     link = net.http_GET(url).content
     match=re.compile('overflow:hidden;"> <a href="(.+?)" title="(.+?)"><img width=".+?" height=".+?" src="(.+?)"></a>').findall(link)
     for url,name,thumb in match:
          name = name.replace('View all episode in','')
          main.addDir(name,url,'chiaepisodes',thumb,'','')
          main.AUTO_VIEW('movies')              

def CHIAALPHMAIN(url):
     link = net.http_GET(url).content
     match=re.compile('<img width=".+?" height=".+?" src="(.+?)"></a></p></div></td><div style="width:.+?; float:.+?;"><td class=".+?" style=".+?; overflow:.+?;"><div style="height:.+?; width:.+?;"><div style=".+?;"><a href="(.+?)" title="(.+?)">').findall(link)
     for thumb,url,name in match:
          name = name.replace('View all episode in','')
          main.addDir(name,url,'chiaepisodes',thumb,'','')
          main.AUTO_VIEW('movies')
               
def CHIAEPISODES(url,name,year):
    link = net.http_GET(url).content
    match=re.compile('background: #000 url(.+?) no-repeat.+?;" alt="(.+?)"><a href="(.+?)"').findall(link)             
    for thumb,name,url in match:
         thumb = thumb.replace('(','')
         thumb = thumb.replace(')','')
         name = name.replace('&#8211','-')
         link = net.http_GET(url).content
         matchvid=re.compile('Watch via Mobile</font></a><a id="download" target="_blank" href="(.+?)">.+?MP4 Video format').findall(link)
         for url in matchvid:
              main.addDir(name,url,'chialinkpage',thumb,'','')
              main.AUTO_VIEW('movies')
          
                      

def CHIALINKPAGE(url,name):
     link = net.http_GET(url).content
     matchsource = re.compile('class="bttn green" href="(.+?)">Save mp4 as Link</a>').findall(link)
     for url in matchsource:
          CHIARESOLVE(name,url,'')
     
        

                     

#Start Search Function
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default

                
def SEARCHCIA(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching for TV Shows" )
	if ( not vq ): return False, 0
	title = urllib.quote_plus(vq)
	searchUrl += title + '&criteria=title' 
	print "Searching URL: " + searchUrl 
	SEARCHSHOW(searchUrl)

	main.AUTO_VIEW('movies')


def CHIARESOLVE(name,url,iconimage):
         ok=True
         liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
         ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
         xbmc.sleep(1000)
         xbmc.Player ().play(str(url), liz, False)

         main.AUTO_VIEW('')



