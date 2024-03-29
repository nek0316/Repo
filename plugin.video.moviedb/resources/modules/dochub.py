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





addon_id = 'plugin.video.moviedb'

addon = xbmcaddon.Addon ('plugin.video.moviedb')

#PATHS
addonPath = addon.getAddonInfo('path')
artPath = addonPath + '/art/'
fanartPath = fanart
#HOOKS
settings = xbmcaddon.Addon(id='plugin.video.moviedb')

#Main Links 
def DOCCATEGORIES():

        addDir('**IN TRANSITION SOME WORK OTHERS DO NOT** ','none','doccategories','')
       
        addDir('Top Documentary Films ','none','topdoc',artPath+'topdocfilm.png')

        addDir('Documentary.net','none','docnet',artPath+'docnet.png')

        addDir('Documentary-Log ','none','doclog',artPath+'doculog.png')

        addDir('Documentary Storm ','none','docstorm',artPath+'docstorm.png')

        main.AUTO_VIEW('list')

def TOPDOC():
        addDir('9/11','http://topdocumentaryfilms.com/category/911/','tdindex','')
        addDir('Art/Artists','http://topdocumentaryfilms.com/category/art-artists/','tdindex','')
        addDir('Biography','http://topdocumentaryfilms.com/category/biography/','tdindex','')
        addDir('Comedy','http://topdocumentaryfilms.com/category/comedy/','tdindex','')
        addDir('Crime/Conspiracy','http://topdocumentaryfilms.com/category/crime-conspiracy/','tdindex','')
        addDir('Crime','http://topdocumentaryfilms.com/category/crime/','tdindex','')
        addDir('Drugs','http://topdocumentaryfilms.com/category/drugs/','tdindex','')
        addDir('Economics','http://topdocumentaryfilms.com/category/economics/','tdindex','')
        addDir('Enviroment','http://topdocumentaryfilms.com/category/enviroment/','tdindex','')
        addDir('Health','http://topdocumentaryfilms.com/category/health/','tdindex','')
        addDir('History','http://topdocumentaryfilms.com/category/history/','tdindex','')
        addDir('Media','http://topdocumentaryfilms.com/category/media/','tdindex','')
        addDir('Military/War','http://topdocumentaryfilms.com/category/military-war/','tdindex','')
        addDir('Mystery','http://topdocumentaryfilms.com/category/mystery/','tdindex','')
        addDir('Nature/Wildlife','http://topdocumentaryfilms.com/category/nature-wildlife/','tdindex','')
        addDir('Performing Arts','http://topdocumentaryfilms.com/category/music-performing-arts/','tdindex','')
        addDir('Philosophy','http://topdocumentaryfilms.com/category/philosophy/','tdindex','')
        addDir('Politics','http://topdocumentaryfilms.com/category/politics/','tdindex','')
        addDir('Psychology','http://topdocumentaryfilms.com/category/psychology/','tdindex','')
        addDir('Religion','http://topdocumentaryfilms.com/category/religion/','tdindex','')
        addDir('Science/Tech','http://topdocumentaryfilms.com/category/science-technology/','tdindex','')
        addDir('Sexuality','http://topdocumentaryfilms.com/category/sex/','tdindex','')
        addDir('Society','http://topdocumentaryfilms.com/category/society/','tdindex','')
        addDir('Sports','http://topdocumentaryfilms.com/category/sports/','tdindex','')
        addDir('Technology','http://topdocumentaryfilms.com/category/technology/','tdindex','')
        main.AUTO_VIEW('list')       

def DOCNET():
        addDir('Latest Documentaries','http://documentary.net/','docnetlatest','')
        addDir('Catagories','http://documentary.net/','docnetcat','')
        main.AUTO_VIEW('list')
        

def DOCLOG():
        addDir('Latest Documentaries','http://www.documentary-log.com/','docloglatest','')
        addDir('Catagories','http://www.documentary-log.com/','doclogcat','')
        main.AUTO_VIEW('list')

        
def DOCSTORM():
        addDir('Latest Documentaries','http://documentarystorm.com/','stormlatest','')
        addDir('Catagories','http://documentarystorm.com/','stormcat','')
        main.AUTO_VIEW('list')

#First Links from RSS 
def TDINDEX(url): 
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('"postTitle"><a\nhref="(.+?)" title="(.+?)">').findall(link)
        for url,name in match:
            name =name.replace("&#039;s","'s")       
            addDir(name,url,'tdvidpage','')
            match=re.compile('rel="next" href="(.+?)"').findall(link)
        if len(match) > 0:
                addDir('Next Page',(match[0]),'tdindex',artPath+'next.png')
                main.AUTO_VIEW('list')

# For Documentary.net
def DOCNETINDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)"   class=\'fix\'><img src="(.+?)" alt="(.+?)"').findall(link)
        #matchimg=re.compile('src="(.+?)" class="alignleft').findall(link)
        for url,iconimage,name in match:
                name =name.replace("&#039;s","'s")
         #for thumb in matchimg:        
                addDir(name,url,'docnetvidpage',iconimage)
        match=re.compile("<a class='page-numbers' href='(.+?)'>(.+?)</a>").findall(link)
        for url, number in match:
          if len(match) > 0:
                  addDir('Page'+number,'http://documentary.net'+url,'docnetindex',artPath+'next.png')
                  main.AUTO_VIEW('movies')


def DOCNETCAT(url):
#link = net.http_GET(url).content
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<li><a href="(.+?)">(.+?)</a>').findall(link)
        for url,name in match:
         #for thumb in matchimg:        
            addDir(name,url,'docnetindex','')
            main.AUTO_VIEW('list')            

def DOCNETLATEST(url):
#link = net.http_GET(url).content
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)"   class=.+?><img src="(.+?)" alt="(.+?)" />').findall(link)
        #matchimg=re.compile('src="(.+?)" class="alignleft').findall(link)
        for url,iconimage,name in match:
             name =name.replace("&#039;s","'s")
             name =name.replace("&#8211;","-")   
         #for thumb in matchimg:        
             addDir(name,url,'docnetvidpage',iconimage)
             main.AUTO_VIEW('movies')

def STORMLATEST(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('class="cover">\r\n\t\t<a href="(.+?)" title="(.+?)" >\r\n   \t\t\t<img width="198" height="297" src="(.+?)"').findall(link)
        for url,name,iconimage in match:        
            addDir(name,url,'stormvidpage',iconimage)
            main.AUTO_VIEW('movies')

def STORMCAT(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" title=".+?">(.+?)</a></li>').findall(link)
        for url,name in match:        
            addDir(name,url,'stormindex','')
            main.AUTO_VIEW('list')

def STORMINDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('class="cover">\r\n\t\t<a href="(.+?)" title="(.+?)" >\r\n   \t\t\t<img width="198" height="297" src="(.+?)"').findall(link)
        for url,name,iconimage in match:
                name =name.replace("&#039;s","'s")
                name =name.replace("&#8211;","-")        
                addDir(name,url,'stormvidpage',iconimage)
        match=re.compile('<link rel="next" href="(.+?)" />').findall(link)
        if len(match) > 0:
           addDir('Next Page',(match[0]),'stormindex',artPath+'next.png')
           main.AUTO_VIEW('movies')

def STORMVIDPAGE(url,name):
        #link = net.http_GET(url).content
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        #match=re.compile('<p><iframe src="(.+?)" .+?" .+?"').findall(link)==========old links
        match=re.compile('<p><iframe width=".+?" height=".+?" src="(.+?)" frameborder=".+?" ').findall(link)
        if len(match) > 0:
           for url in match:
                if 'youtube' in url:
                        if 'http:' in url:
                                url = url.replace('http:','')
                                
                                url = url.replace('//www.youtube.com/embed/','http://www.youtube.com/embed?v=')
                                   
                                RESOLVE(name,url,'')

                                main.AUTO_VIEW('movies')
                        else:
                                url = url.replace('//www.youtube.com/embed/','http://www.youtube.com/embed?v=')
                                   
                                RESOLVE(name,url,'')

                                main.AUTO_VIEW('movies')
#for Vimeo first page
        #if len(match)<1:           
        if 'vimeo' in url:
                #else:   
        
                #match=re.compile('<p><iframe src="(.+?)" .+?" .+?"').findall(link)
                for url in match:
                         #url = url.replace('//player.vimeo.com/video/','http://player.vimeo.com/video/')
                        
                         TDVIMEO(name,url,'')

                         main.AUTO_VIEW('movies')

        else:
                match=re.compile('<iframe class=".+?" width=".+?" src="(.+?)" frameborder=').findall(link)
                for url in match:
                        TDVIMEO(name,url,'')

                        main.AUTO_VIEW('movies')
                
            
def DOCLOGCAT(url):
#link = net.http_GET(url).content
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<li class=".+?"><a href="(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:       
            addDir(name,url,'docloglatest','')
            main.AUTO_VIEW('list')

def DOCLOGVIDPAGE(url):
        #link = net.http_GET(url).content
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<iframe.*?src="(http://.+?)".*?>').findall(link)
        for url in match:
                if 'youtube' in url:
                   url = url.replace('embed/','embed?v=')
                    
                   RESOLVE(name,url,'')

                   main.AUTO_VIEW('movies')

#for Vimeo first page
        #if len(match)<1:           
        if 'vimeo' in url:
                #else:   
        
                #match=re.compile('"url":"(.+?)"').findall(link)
                for url in match:
                         #url = url.replace('vimeo.com/moogaloop.swf?','player.vimeo.com/video/')
                        
                         TDVIMEO(name,url,'')

                         main.AUTO_VIEW('movies')                     

def DOCLOGLATEST(url):
#link = net.http_GET(url).content
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" title="(.+?)">\r\n          <img src="(.+?)" alt=".+?" class="thumb"').findall(link)
        #matchimg=re.compile('src="(.+?)" class="alignleft').findall(link)
        for url,name,iconimage in match:
         #for thumb in matchimg:        
            addDir(name,url,'doclogvidpage',iconimage)
        match=re.compile("<a href='(.+?)' class='page larger'>(.+?)</a>").findall(link)
        for url, number in match:
         if len(match) > 0:
           addDir('Page'+number,url,'docloglatest',artPath+'next.png')
           main.AUTO_VIEW('movies')                        
    
# For Primary YouTube Listing                
def TDVIDPAGE(url,name):
        #link = net.http_GET(url).content
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('width=".+?" height=".+?" src="(.+?)rel=0.+?"').findall(link)
        for url in match:
                if 'http:'in url:
                   url = url.replace('embed/','embed?v=')
                    
                   RESOLVE(name,url,'')

                   main.AUTO_VIEW('movies')
                else:
                 
                   url = 'http:'+url
                   url = url.replace('embed/','embed?v=')
                    
                   RESOLVE(name,url,'')

                   main.AUTO_VIEW('movies')

#for odd YT and Vimeo first page 
        if len(match)<1:
                match=re.compile('width="530" height="325" src="(.+?)"').findall(link)
                for url in match:
                      if 'youtube' in url:
                         url = 'http:'+url
                         url = url.replace('/embed/videoseries?list=','embed?=')
                         RESOLVE(name,url,'')

                         main.AUTO_VIEW('movies') 
        
                
                
                      if 'vimeo' in url:  
                         TDVIMEO(name,url,'')

                         main.AUTO_VIEW('movies')

              
        
                                

#Scrape and Play TD Vimeo url
def TDVIMEO(name,url,iconimage):
          req = urllib2.Request(url)
          req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
          response = urllib2.urlopen(req)
          link=response.read()
          response.close()
          match=re.compile('"url":"(.+?)","height":.+?,"width":.+?,').findall(link)
          for url in match:
           ok=True
          liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
          ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
          xbmc.executebuiltin("XBMC.Notification(Please Wait!,Preparing Your Video,3000)")
          xbmc.sleep(1000)
          xbmc.Player ().play(str(url), liz, False)

          main.AUTO_VIEW('')

# DocNet  Start                          
def DOCNETVIDPAGE(url,name):
        #link = net.http_GET(url).content
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('"embedURL" content="(.+?)?version').findall(link)
        for url in match:
                #url = url.replace('v/','embed?v=')
                if 'youtube' in url:
                   url = url.replace('v/','embed?v=')
                    
                   RESOLVE(name,url,'')

                   main.AUTO_VIEW('movies')

#for Vimeo first page
        if len(match)<1:           
        #if 'vimeo' in url:
                #else:   
        
                match=re.compile('"embedURL" content="(.+?)" />').findall(link)
                for url in match:
                         url = url.replace('vimeo.com/moogaloop.swf?','player.vimeo.com/video/')
                        
                         TDVIMEO(name,url,'')

                         main.AUTO_VIEW('movies')                   
                         

# Second From Source to YT
def VIDEOLINKSYT(url,name):
        link = net.http_GET(url).content
        match=re.compile('<a class="title " href="(.+?)" tabindex="1"').findall(link)
        for url in match:
         movie_name = name[:-6]
         year = name[-6:]
         movie_name = movie_name.decode('UTF-8','ignore')
                                
         data = GRABMETA(movie_name,year)
         thumb = data['cover_url']
         RESOLVEYT(name,url,iconimage)
            
         main.AUTO_VIEW('movies') 



def RESOLVE(name,url,iconimage):
         url = urlresolver.HostedMediaFile(url=url).resolve()
         ok=True
         liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
         ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
         xbmc.executebuiltin("XBMC.Notification(Please Wait!,Preparing Your Video,3000)")
         xbmc.sleep(1000)
         xbmc.Player ().play(str(url), liz, False)

         main.AUTO_VIEW('')

#Resolve 2 forYouTube

def RESOLVEYT(name,url,iconimage):
         url = urlresolver.HostedMediaFile(url=url).resolve()
         ok=True
         liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
         ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
         xbmc.executebuiltin("XBMC.Notification(Please Wait!,Preparing Your Video,3000)")
         xbmc.sleep(1000)
         xbmc.Player ().play(url, liz, False)         

         main.AUTO_VIEW('')
            
                

	


                

# addLink for direct play
def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage);liz.setInfo('video',{'Title':name,'Genre':'Live','Studio':name})
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
        xbmc.sleep(1000)
        xbmc.Player (xbmc.PLAYER_CORE_PAPLAYER).play(url, liz, False)
        return ok

# Standard addDir
def addDir(name,url,mode,iconimage):
        
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        xbmc.executebuiltin("Container.SetViewMode(500)")
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
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok  



