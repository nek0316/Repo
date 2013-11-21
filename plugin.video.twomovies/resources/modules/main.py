# -*- coding: cp1252 -*-
# Main Module by: Blazetamer

import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon,mechanize
from metahandler import metahandlers
import SimpleDownloader as downloader
downloader = downloader.SimpleDownloader()

from t0mm0.common.addon import Addon
from t0mm0.common.net import Net

try:
     import StorageServer
except:
     import storageserverdummy as StorageServer



#Define common.addon
addon_id = 'plugin.video.twomovies'
addon = Addon(addon_id, sys.argv)

# Cache for favorites  Whenever i do them 
cache = StorageServer.StorageServer("Two Movies", 0)



# Global Stuff
settings = xbmcaddon.Addon(id=addon_id)
artwork = xbmc.translatePath(os.path.join('http://rowthreemedia.com/xbmchub/2movies/art/', ''))
net = Net()


def nameCleaner(name):
          name = name.replace('&#8211;','')
          name = name.replace("&#8217;","")
          name = name.replace("&#039;s","'s")
          return(name)
     


#Metadata    
grab=metahandlers.MetaData()

def GRABMETA(name,year):
        meta = grab.get_meta('movie',name,year,None,None)
        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
        'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
        'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year']}
                
        return infoLabels
        
        

def GRABTVMETA(name,year):
        meta = grab.get_meta('tvshow',name,year,None,None)
        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
        'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],
        'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'imdb_id': meta['imdb_id'],'year': meta['year']}
                
        return infoLabels
        

def GRABEPISODEMETA(name,imdb_id,season,episode):
        meta = grab.get_episode_meta('tvshow',name,imdb_id,season,episode)
        #meta = grab.get_episode_meta('tvshow',name,year,None,None)
        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
        'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
        'director': meta['director'],'backdrop_url': meta['backdrop_url'],'imdb_id': meta['imdb_id']}
                
        return infoLabels
                


#Add Directory Stuff
def addDiralt(name,url,mode,thumb):
     name = nameCleaner(name)
     if thumb == '':
          thumb = artwork + '/main/noepisode.png'
     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'year':year, 'types':'movie'}
     addon.add_directory(params, {'title':name}, img= thumb, fanart= artwork + '/main/fanart.jpg')

def addHELPDir(name,data,mode,imdb_id):
    u=sys.argv[0]+"?data="+urllib.quote_plus(data)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&imdb_id="+str(imdb_id)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=imdb_id)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok

     
#For Movie/TV Download
def addDLDir(name,url,mode,thumb,labels,dlurl,favtype):
        contextMenuItems = []
        
                
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels=labels )   
        #if favtype == 'links':
        contextMenuItems.append(('Download This File', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'url':url, 'mode':'dlvidpage', 'name':name, 'thumb':thumb, 'types':favtype})))
                    
                          
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        try:
             liz.setProperty( "Fanart_Image", labels['backdrop_url'] )
        except:
             pass
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

#Resolve DL Links******************************************
def RESOLVEDL(name,url,thumb):
         
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
          addon.add_video_item(params, {'title':name}, img=data['cover_url'])
          liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=data['cover_url'])
          liz.setInfo('video',infoLabels=data)

     xbmc.sleep(1000)
        
     downloadFile(url,name)#.play(url, liz, False)     
     

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
        elif favtype == 'tvshow':
                contextMenuItems.append(('TV Show  Information', 'XBMC.Action(Info)'))
        elif favtype == 'episode':
                contextMenuItems.append(('TV Show  Information', 'XBMC.Action(Info)'))       
                
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        try:
             liz.setProperty( "Fanart_Image", labels['backdrop_url'] )
        except:
             pass
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
# AddDir for TV SHows to add a year forpass

def addTVDir(name,url,mode,thumb,labels,favtype,year):
        #params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'year':year}
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
          
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&year="+urllib.quote_plus(year)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels=labels )
        if favtype == 'movie':
                contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
        elif favtype == 'tvshow':
                contextMenuItems.append(('TV Show  Information', 'XBMC.Action(Info)'))
        elif favtype == 'episodes':
                contextMenuItems.append(('Episode  Information', 'XBMC.Action(Info)'))       
                
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        try:
             liz.setProperty( "Fanart_Image", labels['backdrop_url'] )
        except:
             pass
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


#Season Directory for TV Shows

def addSDir(name,url,mode,thumb,year,types):
     name = nameCleaner(name)
     contextMenuItems = []
     meta = {}
     
     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'year':year, 'types':types, 'show':name}

     if settings.getSetting('metadata') == 'true':
          meta = grab.get_meta('tvshow',name)
          if meta['backdrop_url'] == '':
               fanart = artwork + '/main/fanart.jpg'
          else:
               fanart = meta['backdrop_url']
     else:
          fanart = artwork + '/main/fanart.jpg'
          

     if settings.getSetting('metadata') == 'true':
               if settings.getSetting('banners') == 'false':
                    if thumb == '':
                         thumb = meta['cover_url']
               else:
                    thumb = meta['banner_url']
     if thumb == '':
          thumb = artwork + '/main/noepisode.png'
     
     contextMenuItems.append(('Tv Show Information', 'XBMC.Action(Info)'))

     
     if settings.getSetting('metadata') == 'true':
          addon.add_directory(params, meta, contextMenuItems, img=thumb, fanart=fanart)          
     else:
          addon.add_directory(params, {'title':name}, contextMenuItems, img= thumb, fanart=fanart)     



# Episode add DirFunction 
def addEPDir(name,url,thumb,mode,show):
        contextMenuItems = []
        ep_meta = None
        show_id = None
        meta = None
        othumb = thumb
        if settings.getSetting('metadata') == 'true':
          meta = grab.get_meta('tvshow',show)
          show_id = meta['imdb_id']
        else:
          fanart = artwork + '/tvshows/fanart.jpg'
        s,e = GET_EPISODE_NUMBERS(name)
        if settings.getSetting('metadata') == 'true':
          try:
              ep_meta = grab.get_episode_meta(show,show_id,s,e)
              if ep_meta['cover_url'] == '':
                    thumb = artwork + '/tvshows/icon.png'
              else:
                    thumb = str(ep_meta['cover_url'])
          except:
               ep_meta=None
               thumb = artwork + '/tvshows/icon.png'
             
        else:
          thumb = othumb
          if thumb == '':
               thumb = artwork + '/tvshows/icon.png'
     
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'season':s, 'episode':e, 'show':show, 'types':'episode'}        
        if settings.getSetting('metadata') == 'true':

          if ep_meta==None:
               fanart = artwork + '/tvshows/fanart.jpg'
               addon.add_directory(params, {'title':name}, img=thumb, fanart=fanart) 
          else:
               if meta['backdrop_url'] == '':
                    fanart = artwork + '/tvshows/fanart.jpg'
               else:
                    fanart = meta['backdrop_url']
               ep_meta['title'] = name
               addon.add_directory(params, ep_meta, fanart=fanart, img=thumb)
        else:
            addon.add_directory(params, {'title':name},fanart=fanart, img=thumb)
     

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
          addon.add_video_item(params, {'title':name}, img=data['cover_url'])
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
                        if content == 'tvshows':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('tvshows-view') )

                        if content == 'episode':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('episode-view') )
                        if content == 'season':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('season-view') )
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

#Episode directory function to be used when adding a Episode, all metadata scrapes and context menu items are handled within_________
def addEDir(name,url,mode,thumb,show):
     #name =
     ep_meta = None
     show_id = None
     meta = None
     othumb = thumb
                
     if settings.getSetting('metadata') == 'true':
          data = GRABTVMETA('tvshow',show)
          #show_id = data['tmdb_id']

     else:
          fanart = artwork + '/main/fanart.jpg'
     
     s,e = GET_EPISODE_NUMBERS(name)

     if settings.getSetting('metadata') == 'true':
          try:
               ep_meta = GRABTVMETA(show,show_id,int(s),int(e))
               if ep_meta['cover_url'] == '':
                    thumb = artwork + '/main/noepisode.png'
               else:
                    thumb = str(ep_meta['cover_url'])
          except:
               ep_meta=None
               thumb = artwork + '/main/noepisode.png'
             
     else:
          thumb = othumb
          if thumb == '':
               thumb = artwork + '/main/noepisode.png'
     
     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'season':s, 'episode':e, 'show':show, 'types':'episode'}        
     if settings.getSetting('metadata') == 'true':

          if ep_meta==None:
               fanart = artwork + '/main/fanart.jpg'
               addon.add_directory(params, {'title':name}, img=thumb, fanart=fanart) 
          else:
               if data['backdrop_url'] == '':
                    fanart = artwork + '/main/fanart.jpg'
               else:
                    fanart = data['backdrop_url']
               ep_meta['title'] = name
               addon.add_directory(params, ep_meta, fanart=fanart, img=thumb)
     else:
          addon.add_directory(params, {'title':name},fanart=fanart, img=thumb) 


#Called within the addEDir function, returns needed season and episode numbers needed for metadata scraping___________________________

def GET_EPISODE_NUMBERS(ep_name):
     s = None
     e = None
     ep_name = re.sub('×','X',ep_name)

     S00E00 = re.findall('[Ss]\d\d[Ee]\d\d',ep_name)
     SXE = re.findall('\d[Xx]\d',ep_name)
     SXEE = re.findall('\d[Xx]\d\d',ep_name)
     SXEEE = re.findall('\d[Xx]\d\d\d',ep_name)

     SSXE = re.findall('\d\d[Xx]\d',ep_name)
     SSXEE = re.findall('\d\d[Xx]\d\d',ep_name)
     SSXEEE = re.findall('\d\d[Xx]\d\d\d',ep_name)
     
     if S00E00:
          print 'Naming Style Is S00E00'
          S00E00 = str(S00E00)
          S00E00.strip('[Ss][Ee]')
          S00E00 = S00E00.replace("u","")
          e = S00E00[-4:]
          e = e[:-2]
          s = S00E00[:5]
          s = s[-2:]
          
     if SXE:
          print 'Naming Style Is SXE'
          SXE = str(SXE)
          SXE = SXE.replace("u","")
          print 'Numer String is ' + SXE
          s = SXE[2]
          e = SXE[4]

     if SXEE:
          print 'Naming Style Is SXEE'
          SXEE = str(SXEE)
          SXEE = SXEE.replace("u","")
          print 'Numer String is ' + SXEE
          s = SXEE[2]
          e = SXEE[4] + SXEE[5]

     if SXEEE:
          print 'Naming Style Is SXEEE'
          SXEEE = str(SXEEE)
          SXEEE = SXEEE.replace("u","")
          print 'Numer String is ' + SXEEEE
          s = SXEEE[2]
          e = SXEEE[4] + SXEEE[5] + SXEEE[6]

     if SSXE:
          print 'Naming Style Is SSXE'
          SSXE = str(SSXE)
          SSXE = SSXE.replace("u","")
          print 'Numer String is ' + SSXE
          s = SSXE[2] + SSXE[3]
          e = SSXE[5]

     if SSXEE:
          print 'Naming Style Is SSXEE'
          SSXEE = str(SSXEE)
          SSXEE = SSXEE.replace("u","")
          print 'Numer String is ' + SSXEE
          s = SSXEE[2] + SSXEE[3]
          e = SSXEE[5] + SSXEE[6]

     if SSXEEE:
          print 'Naming Style Is SSXEEE'
          SSXEEE = str(SSXEEE)
          SSXEEE = SSXEEE.replace("u","")
          print 'Numer String is ' + SSXEEE
          s = SSXEEE[2] + SSXEE[3]
          e = SSXEEE[5] + SSXEEE[6] + SSXEEE[7]

     return s,e



def downloadFile(url,name):
     download_folder = settings.getSetting('download_folder')
     if download_folder == '':
          addon.show_small_popup(title='File Not Downloadable', msg='You need to set your download folder in addon settings first', delay=int(5000), image='')
     else:     
          #if resolvable(url):
               #url = resolve(url)
               ext = ''
               if '.mp4' in url:
                    ext = '.mp4'
               elif '.flv' in url:
                    ext = '.flv'
               elif '.avi' in url:
                    ext = '.avi'
               if not ext == '':
                    if not os.path.exists(download_folder):
                         os.makedirs(download_folder)

                    params = {"url":url, "download_path":download_folder}
                    downloader.download(name + ext, params)
               else:
                    addon.show_small_popup(title='Can Not Download File', msg='Unsupported Host', delay=int(5000), image='')
          #else:
               #addon.show_small_popup(title='Can Not Download File', msg='Unable To Resolve Url', delay=int(5000), image='')
                              



