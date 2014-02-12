# -*- coding: utf-8 -*-
# moviedb Series Gate TV SHOW Module by: Blazetamer


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
show = addon.queries.get('show', '')

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

basetv_url ='http://seriesgate.tv/'
def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")


def SGCATS():

    
          main.addDir('All Series Gate TV Shows','http://seriesgate.tv/tvshows/','sgindex',artwork + 'all.jpg','','dir')
          main.addDir('[COLOR gold]Search TV Shows[/COLOR]','http://seriesgate.tv/search/indv_episodes/','searchsgtv',artwork + 'search.jpg','','dir')
          
          main.AUTO_VIEW('')    





               

        

        
def SGINDEX (url):
        #if settings.getSetting('tmovies_account') == 'true':  
              #net.set_cookies(cookiejar)
        link = net.http_GET(url).content
        match=re.compile('<a href = "(.+?)"><img src = "(.+?)" height=".+?/><div class = "_tvshow_title">(.+?)</div>').findall(link)
        if len(match) > 0:
         for url,sitethumb,name in match:
                
                inc = 0
                #movie_name = fullyear[:-6]
                #year = fullyear[-6:]
                #movie_name = movie_name.decode('UTF-8','ignore')
              
                data = main.GRABTVMETA(name,'')
                thumb = data['cover_url']               
                yeargrab = data['year']
                year = str(yeargrab)               
                dlfoldername = name
                favtype = 'tvshow'
                main.addDir(name,url,'sgepisodelist',thumb,data,favtype)
                
                #main.addSDir(movie_name +'('+ year +')',basetv_url + url,'episodes',thumb,year,favtype)
                
         nmatch=re.compile('<span class="currentpage">.+?</span></li><li><a href="(.+?)">(.+?)</a></li><li>').findall(link)
         if len(nmatch) > 0: 
          for pageurl,pageno in nmatch:
                     
                main.addDir('Page'+ pageno,basetv_url + pageurl,'movieindex',artwork +'nextpage.jpg','','dir')
             
        main.AUTO_VIEW('movies')

                                
def SGEPISODES(url,name,thumb):
    params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb} 
    dlfoldername = name
    mainimg = thumb
    show = name
    link = net.http_GET(url).content
    matchurl=re.compile('<div class="season_page">\n\t\t\t\t\t\t<a href="(.+?)" >(.+?)</a>').findall(link)             
    for url,snumber in matchurl:
              favtype = 'episodes'
              #main.addDir(snumber,url,'sgepisodelist',thumb,'',favtype)
              main.addEPNOCLEANDir(snumber,url,thumb,'sgepisodelist',show,dlfoldername,mainimg,'','')
             
              main.AUTO_VIEW('movies')

def SGEPISODELIST(url,name,thumb):   
    params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb}
    dlfoldername = name
    mainimg = thumb
    show = name
    link = net.http_GET(url).content
    match=re.compile('<a href="(.+?)">&raquo S(.+?) - E(.+?)  (.+?)</a><span>(.+?)</span>').findall(link)             
    for url,season,epnum,epname, date in match:
              s = 'S'+season
              e = 'E'+epnum
              se = s+e
              name = se + ' ' + epname
              favtype = 'episodes'
              main.addEPNOCLEANDir(name,url,thumb,'sgtvlinkpage',show,dlfoldername,mainimg,season,epnum)
             
              main.AUTO_VIEW('movies')              

'''def SGEPISODELIST(url,name,thumb):
    params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb} 
    #dlfoldername = name
    mainimg = thumb
    link = net.http_GET(url).content
    match=re.compile('<div class=".+?" style=".+?" >Season(.+?) Episode(.+?)- <span><a href = ".+?">.+?</a></span></div><div class=".+?" >(.+?)</div><div class = ".+?"></div><div style=".+?"><a href="(.+?)"><img src="(.+?)" width=".+?" height=".+?"  alt=".+?" title = "(.+?)" ></a>').findall(link)             
    for season,epnum, date, url, thumb, epname in match:
              s = 'S'+season
              e = 'E'+epnum
              se = s+e
              name = se + ' ' + epname
              favtype = 'episodes'
              main.addEPNOCLEANDir(name,url,thumb,'sgtvlinkpage',show,dlfoldername,mainimg,season,epnum)
             
              main.AUTO_VIEW('movies') '''             


def SGTVLINKPAGE(url,name,thumb,mainimg):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername,'mainimg':mainimg}
        inc = 0
        linkbase = 'http://seriesgate.tv'
        mainimg = mainimg
        #link = net.http_GET(url).content
        #match=re.compile('href="(.+?)">More Links').findall(link)
        #for surl in match:
           #url = linkbase + surl
        url = url +'searchresult/'    
            
                
  
        
        print 'host url look is' + url    
            
                   
        if inc < 50:
                 link = net.http_GET(url).content
                 hostmatch=re.compile('<a rel="nofollow" href="(.+?)" TARGET="_blank" >(.+?)</a>').findall(link)        
                 for urls,sourcename in hostmatch:
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
                                   


#Start Search Function
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default

                
def SEARCHSGTV(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching for TV Shows" )
	if ( not vq ): return False, 0
	title = urllib.quote_plus(vq)
	searchUrl += title + '&criteria=tag' 
	print "Searching URL: " + searchUrl 
	SGSEARCHINDEX(searchUrl)

	main.AUTO_VIEW('movies')



def SGSEARCHINDEX (url):
        #if settings.getSetting('tmovies_account') == 'true':  
              #net.set_cookies(cookiejar)
        link = net.http_GET(url).content
        match=re.compile('</a><div class = ".+?" style=".+?"><div class = ".+?"><a href = "(.+?)">(.+?)</a>').findall(link)
        if len(match) > 0:
         for url,name in match:
                
                inc = 0
                #movie_name = fullyear[:-6]
                #year = fullyear[-6:]
                #movie_name = movie_name.decode('UTF-8','ignore')
              
                data = main.GRABTVMETA(name,'')
                thumb = data['cover_url']               
                yeargrab = data['year']
                year = str(yeargrab)               
                dlfoldername = name
                favtype = 'tvshow'
                main.addDir(name,url,'sgepisodelist',thumb,data,favtype)
                
                #main.addSDir(movie_name +'('+ year +')',basetv_url + url,'episodes',thumb,year,favtype)
                
         nmatch=re.compile('<span class="currentpage">.+?</span></li><li><a href="(.+?)">(.+?)</a></li><li>').findall(link)
         if len(nmatch) > 0: 
          for pageurl,pageno in nmatch:
                     
                main.addDir('Page'+ pageno,basetv_url + pageurl,'movieindex',artwork +'nextpage.jpg','','dir')
             
        main.AUTO_VIEW('movies')

