# Main Module by: Blazetamer

import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon,mechanize
from metahandler import metahandlers

from t0mm0.common.addon import Addon
from t0mm0.common.net import Net

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
artwork = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.twomovies/art/', ''))
grab=metahandlers.MetaData()
net = Net()


def nameCleaner(name):
          name = name.replace('&#8211;','')
          name = name.replace("&#8217;","")
          name = name.replace("&#039;s","'s")
          return(name)
     


#Metadata    
grab=metahandlers.MetaData()

def GRABMETA(name,year):
        meta = grab.get_meta('movie',name,year,None,None,overlay=6)
        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
        'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
        'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year']}
                
        return infoLabels


#Add Directory Stuff
def addDiralt(name,url,mode,thumb):
     name = nameCleaner(name)
     if thumb == '':
          thumb = artwork + '/main/noepisode.png'
     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'year':year, 'types':'movie'}
     addon.add_directory(params, {'title':name}, img= thumb, fanart= artwork + '/main/fanart.jpg')


# Standard addDir
def addDir(name,url,mode,thumb,labels,favtype):
        contextMenuItems = []
        sitethumb = thumb
        sitename = name
        try:
                name = data['title']
                thumb = data['cover_url']
                fanart = data['backdrop_url']
        except:
                name = sitename
                
        if thumb == '':
                thumb = sitethumb
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels=labels )
        if favtype == 'movie':
                contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        try:
             liz.setProperty( "Fanart_Image", labels['backdrop_url'] )
        except:
             pass
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
     



#Host directory function for  Host Dir , hthumb =  host thumb and should be grabbed using the 'GETHOSTTHUMB(host)' function before 
def addHDir(name,url,mode,thumb,hthumb):
     

     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'year':year, 'types':types, 'season':season, 'episode':episode, 'show':show}
     addon.add_directory(params, {'title':name}, img=hthumb, fanart=fanart)




#Resolve Functions
     
def RESOLVE(name,url,iconimage):
         url = urlresolver.HostedMediaFile(url=url).resolve()
         ok=True
         liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
         ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
         xbmc.sleep(1000)
         xbmc.Player ().play(str(url), liz, False)

         AUTO_VIEW('')

#Resolve 2 

def RESOLVE2(name,url,thumb):
         
     data=0
     try:
          data = GRABMETA(movie_name,year)
     except:
           data=0
     hmf = urlresolver.HostedMediaFile(url)
     host = ''
     if hmf:
          url = urlresolver.resolve(url)
          host = hmf.get_host() 
             
     params = {'url':url, 'name':name, 'thumb':thumb}
     if data == 0:
          addon.add_video_item(params, {'title':name}, img=thumb)
          liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)

     else:
          addon.add_video_item(params, {'title':name}, img=meta['cover_url'])
          liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=data['cover_url'])
          liz.setInfo('video',infoLabels=data)

     xbmc.sleep(1000)
        
     xbmc.Player ().play(url, liz, False)

#AutoView
def AUTO_VIEW(content):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
                if settings.getSetting('auto-view') == 'true':
                        if content == 'movies':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('movies-view') )
                        if content == 'list':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('list-view') )
                else:
                        xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('default-view') )

        


     

#Returns the host thumbnail so that you can pass it as and argument 
def GETHOSTTHUMB(host):
     if host.endswith('.com'):
          host = host[:-4]
     if host.endswith('.org'):
          host = host[:-4]
     if host.endswith('.eu'):
          host = host[:-3]
     if host.endswith('.ch'):
          host = host[:-3]
     if host.endswith('.in'):
          host = host[:-3]
     if host.endswith('.es'):
          host = host[:-3]
     if host.endswith('.tv'):
          host = host[:-3]
     if host.endswith('.net'):
          host = host[:-4]
     if host.endswith('.me'):
          host = host[:-3]
     if host.endswith('.ws'):
          host = host[:-3]
     if host.endswith('.sx'):
          host = host[:-3]
     if host.startswith('www.'):
             host = host[4:]
     
     
     host = artwork + '/hosts/' + host +'.png'
     return(host)
