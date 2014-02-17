
#  Live Streams Module by: Blazetamer


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon,main

from metahandler import metahandlers

try:
        from addon.common.addon import Addon

except:
        from t0mm0.common.addon import Addon
addon_id = 'plugin.video.moviedb'


try:
        from addon.common.net import Net

except:  
        from t0mm0.common.net import Net
net = Net()
try:
     import StorageServer
except:
     import storageserverdummy as StorageServer




#addon = Addon(addon_id, sys.argv)
addon = main.addon
# Cache  
cache = StorageServer.StorageServer("MovieDB", 0)


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

print 'Mode is: ' + mode
print 'Url is: ' + url
print 'Name is: ' + name
print 'Thumb is: ' + thumb
print 'Extension is: ' + ext
print 'File Type is: ' + console
print 'DL Folder is: ' + dlfoldername
print 'Favtype is: ' + favtype
print 'Main Image is: ' + mainimg

# Global Stuff
settings = xbmcaddon.Addon(id=addon_id)
artwork = xbmc.translatePath(os.path.join('http://addonrepo.com/xbmchub/moviedb/images/', ''))
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




def LIVECATS(url):
        link=OPEN_URL(url).replace('\n','').replace('\r','')
        match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode><desc>(.+?)</desc>').findall(link)
        for name,url,thumb,mode,desc in match:
                print 'Description is  ' + desc
                addDir(name,url,mode,thumb,desc,thumb)                        
        main.AUTO_VIEW('movies')
        
def COMMONSTREAMS(url):
        link=OPEN_URL(url).replace('\n','').replace('\r','')
        match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(link)
        for name,url,thumb in match:
                addDir(name,url,'livecatslist',thumb,'',thumb)                        
        main.AUTO_VIEW('movies') 
        
def USERSUB(url):
        #main.addDir('[COLOR blue][B]Author/Updated[/B][/COLOR]' ,'none','usersub',artwork +'usersub.png','','dir')
        link=OPEN_URL(url).replace('\n','').replace('\r','')
        match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail><submitted>(.+?)</submitted>').findall(link)
        for name,url,thumb,date in match:
                if 'menu' in date:
                        addDir(name,url,'commonstreams',thumb,'',thumb)   
                        
                else:
                        addDir(name,url,'livecatslist',thumb,'',thumb)                        
        main.AUTO_VIEW('movies')        



        
def LIVECATSLIST(url):
        mainurl=url
        link=OPEN_URL(url).replace('\n','').replace('\r','')
        match=re.compile('<name>(.+?)</name><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode><desc>(.+?)</desc>').findall(link)
        for name,url,thumb,mode,desc in match:
                print 'Description is  ' + desc
                addDir(name,url,mode,thumb,desc,thumb)                        
        
        link=OPEN_URL(mainurl).replace('\n','').replace('\r','')
        match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(link)
        for name,url,thumb in match:
                addDir(name,url,'liveresolve',thumb,'','dir')       
            

        main.AUTO_VIEW('movies')   







def LIVERESOLVE(name,url,thumb):
         ok=True
         liz=xbmcgui.ListItem(name, iconImage=thumb,thumbnailImage=thumb); liz.setInfo( type="Video", infoLabels={ "Title": name } )
         ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
         xbmc.sleep(1000)
         xbmc.Player ().play(str(url), liz, False)

         main.AUTO_VIEW('')


  

def addDir(name,url,mode,thumb,desc,favtype):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'desc':desc}
        fanart = thumb
        if thumb == artwork + 'icon.png':
                fanart = 'http://addonrepo.com/xbmchub/moviedb/images/fanart2.jpg'
        elif thumb == '-':
                fanart = 'http://addonrepo.com/xbmchub/moviedb/images/fanart2.jpg'        
        if desc == '':
                desc = 'Description not available at this level'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": desc } )
        liz.setProperty( "Fanart_Image", fanart )
        #liz.setProperty( "Addon.Description", desc )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
#==============================Attempt to scrape Ilive.to==============================================================

def ILIVEMAIN():
        link=OPEN_URL('http://goo.gl/WrDOJi').replace('\n','').replace('\r','')
        match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode><desc>(.+?)</desc>').findall(link)
        for name,url,thumb,mode,desc in match:
                print 'Description is  ' + desc
                addDir(name,url,mode,thumb,desc,thumb)
        
        #addDir('All','all','ilivelists',artwork+'/ilive.png','','')
        addDir('All','allenglish','ilivelists',artwork+'/ilive.png','All Streams available from iLive','')
        addDir('Animation','animation','ilivelists',artwork+'/ilive.png','Animation Stream Listings','')
        addDir('Entertainment','entertainmentenglish','ilivelists',artwork+'/ilive.png','Entertainment Streams from iLive','')
        addDir('General','general','ilivelists',artwork+'/ilive.png','General Streams','')
        addDir('Music','music','ilivelists',artwork+'/ilive.png','Current Listed Music Streams','')
        addDir('News','news','ilivelists',artwork+'/ilive.png','Current News Streams','')
        addDir('Sports','sportsenglish','ilivelists',artwork+'/ilive.png','Live Sports Streams from iLive','')
        main.AUTO_VIEW('movies')
        
def ILIVELISTS(menuurl):
        if menuurl=='general':
            try:
                urllist=['http://www.ilive.to/channels/General','http://www.ilive.to/channels/General?p=2']
            except:
                urllist=['http://www.ilive.to/channels/General']
        
        if menuurl=='news':
            try:
                urllist=['http://www.ilive.to/channels/News']
            except:
                urllist=['http://www.ilive.to/channels/News']
        if menuurl=='music':
            try:
                urllist=['http://www.ilive.to/channels/Music']
            except:
                urllist=['http://www.ilive.to/channels/Music']
        if menuurl=='animation':
            try:
                urllist=['http://www.ilive.to/channels/Animation']
            except:
                urllist=['http://www.ilive.to/channels/Animation']

        if menuurl=='allenglish':
            try:
                urllist=['http://www.ilive.to/channels?lang=1','http://www.ilive.to/channels?lang=1&p=2','http://www.ilive.to/channels?lang=1&p=3','http://www.ilive.to/channels?lang=1&p=4','http://www.ilive.to/channels?lang=1&p=5','http://www.ilive.to/channels?lang=1&p=6','http://www.ilive.to/channels?lang=1&p=7','http://www.ilive.to/channels?lang=1&p=8','http://www.ilive.to/channels?lang=1&p=9','http://www.ilive.to/channels?lang=1&p=10']
            except:
                urllist=['http://www.ilive.to/channels?lang=1','http://www.ilive.to/channels?lang=1&p=2','http://www.ilive.to/channels?lang=1&p=3','http://www.ilive.to/channels?lang=1&p=4','http://www.ilive.to/channels?lang=1&p=5','http://www.ilive.to/channels?lang=1&p=6','http://www.ilive.to/channels?lang=1&p=7','http://www.ilive.to/channels?lang=1&p=8','http://www.ilive.to/channels?lang=1&p=9']
        if menuurl=='entertainmentenglish':
            try:
                urllist=['http://www.ilive.to/channels/Entertainment?lang=1','http://www.ilive.to/channels/Entertainment?lang=1&p=2','http://www.ilive.to/channels/Entertainment?lang=1&p=3','http://www.ilive.to/channels/Entertainment?lang=1&p=4','http://www.ilive.to/channels/Entertainment?lang=1&p=5','http://www.ilive.to/channels/Entertainment?lang=1&p=6']
            except:
                urllist=['http://www.ilive.to/channels/Entertainment?lang=1','http://www.ilive.to/channels/Entertainment?lang=1&p=2','http://www.ilive.to/channels/Entertainment?lang=1&p=3','http://www.ilive.to/channels/Entertainment?lang=1&p=4','http://www.ilive.to/channels/Entertainment?lang=1&p=5']
        if menuurl=='sportsenglish':
            try:
                urllist=['http://www.ilive.to/channels/Sport?lang=1','http://www.ilive.to/channels/Sport?lang=1&p=2']
            except:
                urllist=['http://www.ilive.to/channels/Sport?lang=1']
        if 'http' in menuurl:
                print 'MENUURL IS '+ menuurl
                urllist = [menuurl]
                
                urllistlist = str(urllist)
                print 'URLLIST is ' + urllistlist

        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Loading Menu..Standby...')
        pages = len(urllist)
        gotpages = 0
        remaining_display = 'Pages  :: [B]'+str(gotpages)+' / '+str(pages)+'[/B].'
        dialogWait.update(0,'[COLOR gold][B]Loading.....[/B][/COLOR]',remaining_display)
        for durl in urllist:
                link=OPEN_URL(durl)
                link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
                match=re.compile('src=".+?" alt=".+?<img width=".+?" height=".+?" src="([^<]+)" alt=".+?"/></noscript></a><a href="(.+?)"><strong>(.*?)</strong></a><br/>').findall(link)
                for thumb,url,name in match:
                        addDir(name,url,'iliveplaylink',thumb,'','')
                                      
                gotpages = gotpages + 1
                percent = (gotpages * 100)/gotpages
                remaining_display = 'Pages loaded :: [B]'+str(gotpages)+' / '+str(pages)+'[/B].'
                dialogWait.update(percent,'[COLOR gold][B]Loading.....[/B][/COLOR]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
         


def ILIVEPLAYLINK(name,menuurl,thumb):
        
        LogNotify('Attempting to play Stream', 'Please Wait...', '3000', artwork+'/ilive.png')
        link=OPEN_URL(menuurl)
        ok=True
        if link:
                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                playlist.clear()
                link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
                match=re.compile('http://www.ilive.to/embed/(.+?)&width=(.+?)&height=(.+?)&autoplay=true').findall(link)
                for fid,wid,hei in match:
                    pageUrl='http://www.ilive.to/m/channel.php?n='+fid
                link=OPEN_URL(pageUrl).replace('\/','/').replace('\\','')
                newlink=re.compile('''file': "([^"]+?)"''').findall(link)
                playable = newlink[0]
                print 'RTMP IS ' +  playable
                LIVERESOLVE(name,playable,thumb)


#Start Ketboard Function                
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default


#Start Search Function
def SEARCHILIVE(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching for Streams" )
	if ( not vq ): return False, 0
	title = urllib.quote_plus(vq)
	searchUrl += title  
	print "Searching Streams: " + searchUrl 
	SEARCHLINKS(searchUrl)
             
               
def SEARCHLINKS(urllist):                 
        
                link=OPEN_URL(urllist)
                link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
                match=re.compile('src=".+?" alt=".+?<img width=".+?" height=".+?" src="([^<]+)" alt=".+?"/></noscript></a><a href="(.+?)"><strong>(.*?)</strong></a><br/>').findall(link)
                if len(match) > 0:
                        for thumb,url,name in match:
                                addDir(name,url,'iliveplaylink',thumb,'','')
                                  
                else:
                        addDir('[COLOR red]None Found Try again[/COLOR]','http://www.ilive.to/channels/?q=','searchilive','','','')
        
