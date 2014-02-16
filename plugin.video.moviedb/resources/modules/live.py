
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
        #main.AUTO_VIEW('movies') 
        #addDir('User Submitted','http://addonrepo.com/xbmchub/moviedb/streams/userstreams.xml','usersub',artwork +'usersub.png','','user')
        #addDir('Community Streams','http://addonrepo.com/xbmchub/moviedb/streams/streamsets.xml','commonstreams',artwork +'community.png','','comm')
        #addDir(name,url,'livecatslist',thumb,'','dir')
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
        link=OPEN_URL(url).replace('\n','').replace('\r','')
        mainurl=url
        match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(link)
        for name,url,thumb in match:
                addDir(name,url,'liveresolve',thumb,'','dir')       
        link=OPEN_URL(mainurl).replace('\n','').replace('\r','').replace('\x93','').replace('\x80','').replace('\xe2','')
        match2=re.compile('<stream>(.+?)  (.+?)</stream>').findall(link)
        for name,url in match2:
                addDir(name,url,'liveresolve',thumb,'','dir')

        link=OPEN_URL(mainurl).replace('\n','').replace('\r','').replace('\x93','').replace('\x80','').replace('\xe2','')
        match2=re.compile('<stream>(.+?)-(.+?)</stream>').findall(link)
        for name,url in match2:
                addDir(name,url,'liveresolve',thumb,'','dir')

        link=OPEN_URL(mainurl).replace('\n','').replace('\r','').replace('\x93','').replace('\x80','').replace('\xe2','')
        match2=re.compile('XTINF:-1,(.+?) -(.+?)#E').findall(link)
        for name,url in match2:
                addDir(name,url,'liveresolve',thumb,'','dir')        

        main.AUTO_VIEW('movies')   







def LIVERESOLVE(name,url,iconimage):
         ok=True
         liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
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



