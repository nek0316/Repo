# -*- coding: utf-8 -*-
# moviedb TV SHOW Module by: Blazetamer


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon,main

from metahandler import metahandlers


try:
        from addon.common.addon import Addon

except:
        from t0mm0.common.addon import Addon
addon_id = 'plugin.video.moviedb'
#addon = Addon(addon_id, sys.argv)
addon = main.addon

try:
        from addon.common.net import Net

except:  
        from t0mm0.common.net import Net
net = Net()

try:
     import StorageServer
except:
     import storageserverdummy as StorageServer






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
season = addon.queries.get('season', '')
episode = addon.queries.get('episode', '')

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
cookiejar = addon.get_profile()
cookiejar = os.path.join(cookiejar,'cookies.lwp')
settings = xbmcaddon.Addon(id=addon_id)
artwork = xbmc.translatePath(os.path.join('http://addonrepo.com/xbmchub/moviedb/images/', ''))
grab=metahandlers.MetaData()
net = Net()

basetv_url ='http://www.merdb.ru'
base_url ='http://www.merdb.ru'
def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")


def MERDBTVCATS():

    
          main.addDir('All TV Shows','http://www.merdb.ru/tvshow/','tvindex',artwork + 'all.jpg','','dir')
          main.addDir('Featured TV Shows','http://www.merdb.ru/tvshow/?sort=featured','tvindex',artwork + 'featured.jpg','','dir')
          main.addDir('TV Shows by Popularity','http://www.merdb.ru/tvshow/?featured=1&sort=views','tvindex',artwork + 'popular.jpg','','dir')
          main.addDir('TV Shows by Rating','http://www.merdb.ru/tvshow/?featured=1&sort=ratingp','tvindex',artwork + 'rating.jpg','','dir')
          main.addDir('TV Shows by Release Date','http://www.merdb.ru/tvshow/?sort=year','tvindex',artwork + 'releasedate.jpg','','dir')
          main.addDir('TV Shows by Date Added','http://www.merdb.ru/tvshow/?sort=stamp','tvindex',artwork + 'dateadded.jpg','','dir')
          main.addDir('[COLOR gold]Search TV Shows[/COLOR]','http://www.merdb.ru/tvshow/?search=','searchtv',artwork + 'search.jpg','','dir')
          
          main.AUTO_VIEW('')    





               

        

        
def TVINDEX (url):
        #if settings.getSetting('tmovies_account') == 'true':  
              #net.set_cookies(cookiejar)
        link = net.http_GET(url).content
        match=re.compile('<img src="(.+?)" class=".+?" alt=".+?"/></a><div class=".+?"><a href="(.+?)" title="(.+?)">(.+?)</a>').findall(link)
        if len(match) > 0:
         for sitethumb,url,movie_name,fullyear in match:
                
                inc = 0
                #movie_name = fullyear[:-6]
                year = fullyear[-6:]
                #movie_name = movie_name.decode('UTF-8','ignore')
              
                data = main.GRABTVMETA(movie_name,year)
                thumb = data['cover_url']               
                yeargrab = data['year']
                year = str(yeargrab)               

                favtype = 'tvshow'
                main.addDir(movie_name +'('+ year +')',basetv_url + url,'episodes',thumb,data,favtype)
                
                #main.addSDir(movie_name +'('+ year +')',basetv_url + url,'episodes',thumb,year,favtype)
                
         nmatch=re.compile('<span class="currentpage">.+?</span></li><li><a href="(.+?)">(.+?)</a></li><li>').findall(link)
         if len(nmatch) > 0: 
          for pageurl,pageno in nmatch:
                     
                main.addDir('Page'+ pageno,basetv_url + pageurl,'movieindex',artwork +'nextpage.jpg','','dir')
             
        main.AUTO_VIEW('tvshow')

        
def TVPLAYGENRE (url):
        if settings.getSetting('tmovies_account') == 'true':  
              net.set_cookies(cookiejar)
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)" title=".+?">\r\n                        <img src="(.+?)" class=".+?" style=".+?"  border=".+?" height=".+?" width=".+?" alt="Watch (.+?) Online for Free">\r\n').findall(link)
        if len(match) > 0:
         for url,sitethumb,name in match:
          matchyear=re.compile('<a class="filmyar" href="http://moviedb.name/browse_tv_shows/all/byViews/(.+?)/">\r\n').findall(link)
          if len(matchyear) > 0:
             for year in matchyear:        
                 data = main.GRABTVMETA(name,year)
                 thumb = data['cover_url']
                
                   
             types = 'tvshow'
             main.addSDir(name,url,'episodes',thumb,'',types)
             nmatch=re.compile('<a id="next" class=".+?" href="(.+?)">Next &raquo</a>').findall(link)
        if len(nmatch) > 0:
        
                    main.addDir('Next Page',(nmatch[0]),'tvplaygenre',artwork + 'nextpage.jpg','','dir')
             
                    main.AUTO_VIEW('')



def SEARCHSHOW(url):
             if settings.getSetting('tmovies_account') == 'true':  
              net.set_cookies(cookiejar)
             link = net.http_GET(url).content
             match=re.compile('<a href="(.+?)">\r\n        <img src=".+?" data-original="(.+?)"  class=".+?" style=".+?"  border=".+?" height=".+?" width=".+?" alt="Watch (.+?) Online for Free">\r\n').findall(link)
             if len(match) > 0:
              for url,sitethumb,name in match:
               matchyear=re.compile('<div class="filmyar"><a class="filmyar" href="http://moviedb.name/browse_tv_shows/all/byViews/.+?/">(.+?)</a>').findall(link)
               if len(match) > 0:
                    for year in matchyear:        
                         data = main.GRABTVMETA(name,year)
                         thumb = data['cover_url']
                    types = 'tvshow'
                    if 'watch_tv_show' in url:
                              main.addTVDir(name,url,'episodes',thumb,data,types,'')
                              main.AUTO_VIEW('tvshows')


                                
def EPISODES(url,name,thumb):
    params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb,} 
    dlfoldername = name
    mainimg = thumb
    show = name
    link = net.http_GET(url).content
    matchurl=re.compile('<div class="tv_episode_item"> <a href="(.+?)">Episode (.+?)<span class="tv_episode_name"> - (.+?)</span>').findall(link)             
    for url,epnum,epname in matchurl:
         matchse=re.compile('/tvshow_.+?/season-(.+?)-episode-(.+?)').findall(url)
         for season,episode2 in matchse:
              s = 'S' + season
              e = 'E' + epnum
              se = s+e
              name = se + ' ' + epname
              favtype = 'episodes'
              main.addEPDir(name,base_url + url,thumb,'tvlinkpage',show,dlfoldername,mainimg,season,epnum)
             
              main.AUTO_VIEW('episode')


def TVLINKPAGE(url,name,thumb,mainimg):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername,'mainimg':mainimg}
        inc = 0
        mainimg = mainimg
        link = net.http_GET(url).content
        match=re.compile('<span class="movie_version_link">.+?<a href="(.+?)"').findall(link)
  
        for url in match:
           if 'http://' not in url:     
                 url = base_url + url
           print 'host url look is' + url    
            
                   
           if inc < 50:
                 link = net.http_GET(url).content
                 hostmatch=re.compile('name="bottom" src="(.+?)"/>\n</frameset>').findall(link)        
                 for urls in hostmatch:
                   print 'Pre HMF url is  ' +urls
                   hmf = urlresolver.HostedMediaFile(urls)
                  ##########################################
                   print 'URLS is ' +urls
                   if hmf:
                          #try:
                                  host = hmf.get_host()
                                  hthumb = main.GETHOSTTHUMB(host)
                                  #dlurl = urlresolver.resolve(vidUrl)
                                  data = main.GRABTVMETA(name,'')
                                  thumb = data['cover_url']
                                  favtype = 'movie'
                                  try:    
                                        main.addTVDLDir(name,urls,'vidpage',hthumb,data,dlfoldername,favtype,mainimg)
                                        inc +=1
                                  except:
                                        continue
                                   
def DLTVVIDPAGE(url,name):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':mainimg, 'dlfoldername':dlfoldername,}
        #link = net.http_GET(url).content
        #match=re.compile('<iframe.*?src="(http://.+?)".*?>').findall(link)
        
        #for url in match:
         
                
        main.RESOLVETVDL(name,url,thumb)

def TVVIDPAGE(url,name):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':mainimg, 'dlfoldername':dlfoldername,} 
        #link = net.http_GET(url).content
        #match=re.compile('<iframe.*?src="(http://.+?)".*?>').findall(link)
        
        #for url in match:
        url = url
        name =name
                
        main.RESOLVE2(name,url,thumb)

#Start Search Function
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default

                
def SEARCHTV(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching for TV Shows" )
	if ( not vq ): return False, 0
	title = urllib.quote_plus(vq)
	searchUrl += title + '&criteria=title' 
	print "Searching URL: " + searchUrl 
	TVINDEX(searchUrl)

	main.AUTO_VIEW('movies')




#NAME METHOD*****************************
