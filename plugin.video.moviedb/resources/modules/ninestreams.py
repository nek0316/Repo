
#  Live Streams Module by: Blazetamer


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon,main

from metahandler import metahandlers
from resources.utils import buggalo
import urlresolver
import live

from addon.common.addon import Addon
addon_id = 'plugin.video.moviedb'

from addon.common.net import Net
net = Net()
try:
     import StorageServer
except:
     import storageserverdummy as StorageServer




#addon = Addon(addon_id, sys.argv)
addon = main.addon
# Cache  
streamcache = StorageServer.StorageServer("MovieDBfavs", 0)
standardstreamcache = StorageServer.StorageServer("MovieDBSTfavs", 0)

mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
ext = addon.queries.get('ext', '')
console = addon.queries.get('console', '')
dlfoldername = addon.queries.get('dlfoldername', '')
favtype = addon.queries.get('favtype', '')
mainimg = addon.queries.get('mainimg', '')
desc = addon.queries.get('desc', '')
gomode = addon.queries.get('gomode', '')
regex = addon.queries.get('regex', '')
page = addon.queries.get('page', '')
stream = addon.queries.get('stream', '')


# Global Stuff
settings = xbmcaddon.Addon(id=addon_id)
if settings.getSetting('theme') == '0':
    artwork = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/', ''))
    fanart = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/fanart/fanart.jpg', ''))
else:
    artwork = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/', ''))
    fanart = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart/fanart.jpg', ''))
grab=metahandlers.MetaData()
net = Net()
def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")
def OPEN_URL(url):
  req=urllib2.Request(url)
  req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  response=urllib2.urlopen(req)
  link=response.read()
  response.close()
  return link




def NINEINDEX():       
     live.addDir('External Stream File' ,'none','ninemain','','Your Own Custom Playlist','')
     live.addDir('Local Stream File' ,'none','ninemainlocal','','Your Own Local Playlist','')
     live.addDir('URL Tester' ,'none','addfile','','Test your playable url','')
     #live.addDir('Developer Testing Tester' ,'none ','ninelists','','Dev Testing Mode','')
                    
     main.AUTO_VIEW('movies')
          
        



        



         

  

def addDir(name,url,mode,thumb,stream):
        
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb,  'page':page, 'stream':stream}        
        desc = 'Description not available at this level'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        fanart = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/fanart/fanart.jpg'
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": desc } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


        
#==============================Attempt to scrape ==============================================================
#testurl ='https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/streams/ninestream.xml'
def NINEMAIN():
     customstream =settings.getSetting('custom_streams')
     customname =settings.getSetting('custom_name')
     if customname =='':
          customname= 'Custom Streams'
     if customstream =='':
                dialog = xbmcgui.Dialog()
                ok = dialog.ok('Source Not Set', '               Please Choose Custom Tab and Add Source')
                if ok:
                        LogNotify('Choose Custom Tab ', 'Add Source & Name', '5000', 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/icon.png')        
                        print 'Source Not Set!'
                        addon.show_settings()
     else:     
          
        live.addDir(customname,customstream,'ninelists','','Your Own Custom Playlist','')
        
        main.AUTO_VIEW('movies')

def NINEMAINLOCAL():
     customstream =settings.getSetting('local_file')
     customname =settings.getSetting('local_custom_name')
     if customname =='':
          customname= 'Custom Local Stream'
     if customstream =='':
                dialog = xbmcgui.Dialog()
                ok = dialog.ok('Source Not Set', '               Please Choose Custom Tab and Add Source')
                if ok:
                        LogNotify('Choose Custom Tab ', 'Add Local Source & Name', '5000', 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/icon.png')        
                        print 'Source Not Set!'
                        addon.show_settings()
     else:     
          
        live.addDir(customname,customstream,'ninelocallists','','Your Own Custom Playlist','')
        
        main.AUTO_VIEW('movies')                 
   
        
def NINELISTS(url):

     link=OPEN_URL(url).replace('\n','').replace('\r','')
     match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(link)
     for name,url,thumb in match:
          live.addSTFavDir(name,url,'nineresolver',thumb,'','',isFolder=False, isPlayable=True)
     match=re.compile('<name>(.+?)</name><thumbnail>(.+?)</thumbnail><link>(.+?)</link>').findall(link)
     for name,thumb,url in match:
          live.addDir(name,url,'ninelists',thumb,'',thumb)
     match=re.compile('<name>(.+?)</name><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(link)
     for name,url,thumb in match:
          live.addDir(name,url,'ninelists',thumb,'',thumb)     

def NINELOCALLISTS(url):
     file = open(url, 'r')
     file = file.read()
     file = str(file).replace('\n','').replace('\r','')
     print 'FILE CONTENT IS ' +file
     match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(file)
     for name,url,thumb in match:
          live.addSTFavDir(name,url,'nineresolver',thumb,'','',isFolder=False, isPlayable=True)               


def NINEPLAYLINK(name,url,thumb,stream):
     playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
     playlist.clear()
       
       
     #playable ='rtmp://82.192.95.75/vl/_definst_ playpath=maderoscabrones1 swfUrl=http://www.veemi.com/player/player-licensed.swf live=1 pageUrl=http://www.veemi.com/'
     playable = url
     print 'RTMP IS ' +  playable
     live.LIVERESOLVE(name,playable,thumb)
                                                              


        
def NINERESOLVER(url,name):
     try:        
        dlfoldername = name                            
        urls = url
        hmf = urlresolver.HostedMediaFile(urls)
        if hmf:
                host = hmf.get_host()
                dlurl = urlresolver.resolve(urls)
                live.ILIVERESOLVE(name,dlurl,'')
        else:
                live.ILIVERESOLVE(name,urls,'')        
                                  
     except Exception:
        buggalo.onExceptionRaised()



#Start Search Function
def _get_keyboard( default="", heading="", hidden=False ):
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if keyboard.isConfirmed() :
		return keyboard.getText()
	return default

                
def ADDFILE():
	vq = _get_keyboard( heading="Add your url" )
	if ( not vq ): return False, 0
	url = vq  
	print "Searching URL: " + url 
	#NINERESOLVER(url,'URL TESTER')
	live.addSTFavDir('Click to Try URL',url,'nineresolver','','','',isFolder=False, isPlayable=True)
     
        
def URLTEST(url):
     try:        
        name= 'URL TESTER'                           
        urls = url
        hmf = urlresolver.HostedMediaFile(urls)
        if hmf:
                host = hmf.get_host()
                dlurl = urlresolver.resolve(urls)
                live.ILIVERESOLVE(name,dlurl,'')
        else:
                live.ILIVERESOLVE(name,urls,'')        
                                  
     except Exception:
        buggalo.onExceptionRaised()
