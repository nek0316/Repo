import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc, xbmcaddon, os, sys
import urlresolver
from metahandler import metahandlers
from resources.modules import main
addon_id = 'plugin.video.twomovies'
from t0mm0.common.addon import Addon
addon = main.addon
from t0mm0.common.net import Net
net = Net()

base_url = 'http://www.twomovies.name'





#Movie Vault - Blazetamer.

#PATHS
artwork = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.twomovies/art/', ''))
settings = xbmcaddon.Addon(id='plugin.video.twomovies')

#Main Links 
def CATEGORIES():
        
        main.addDir('[COLOR gold]Popular and Trending Movies[/COLOR]','http://twomovies.name/','movieindex1','','','dir')     
        main.addDir('[COLOR gold]Movies by Year[/COLOR] ','none','byyear','','','dir')
        main.addDir('[COLOR gold]Movie Genres[/COLOR] ','http://twomovies.name/','genres','','','dir')
        main.addDir('[COLOR gold]Movies by Tags[/COLOR] ','http://twomovies.name/tags/','movietags','','','dir')
        main.addDir('[COLOR gold]Search by Movie Name[/COLOR] ','http://twomovies.name/search/?search_query=','searchm','','','dir')
        main.addDir('[COLOR gold]Search by Custom Tag[/COLOR] ','http://twomovies.name/search/?search_query=','searcht','','','dir')
        main.addDir('TV Shows [COLOR red] Coming SOON [/COLOR] ','none','','','','dir')
        if settings.getSetting('resolver') == 'true':
                main.addDir('[COLOR gold]Resolver Settings[/COLOR]','none','resolverSettings','','','dir')
        
        
        main.AUTO_VIEW('')

def BYYEAR():
        yearurl = 'http://twomovies.name/browse_movies/all/byViews/'
        main.addDir('2013 ',yearurl+'2013','playyear','','','dir')
        main.addDir('2012 ',yearurl+'2012','playyear','','','dir')
        main.addDir('2011 ',yearurl+'2011','playyear','','','dir')
        main.addDir('2010 ',yearurl+'2010','playyear','','','dir')
        main.addDir('2009 ',yearurl+'2009','playyear','','','dir')
        main.addDir('2008 ',yearurl+'2008','playyear','','','dir')
        main.addDir('2007 ',yearurl+'2007','playyear','','','dir')
        main.addDir('2006 ',yearurl+'2006','playyear','','','dir')
        main.addDir('2005 ',yearurl+'2005','playyear','','','dir')
        main.addDir('2004 ',yearurl+'2004','playyear','','','dir')
        main.addDir('2003 ',yearurl+'2003','playyear','','','dir')
        main.addDir('2002 ',yearurl+'2002','playyear','','','dir')
        main.addDir('2001 ',yearurl+'2001','playyear','','','dir')
        main.addDir('2000 ',yearurl+'2000','playyear','','','dir')
        main.addDir('1999 ',yearurl+'1999','playyear','','','dir')
        main.addDir('1998 ',yearurl+'1998','playyear','','','dir')
        
        

def GENRES():
        #main.addDir('All','http://twomovies.name/browse_movies/All/byViews/all/','movieindex','','','dir')
        main.addDir('Action','http://twomovies.name/browse_movies/Action/byViews/all/','movieindex','','','dir')
        main.addDir('Adventure','http://twomovies.name/browse_movies/Adventure/byViews/all/','movieindex','','','dir')
        main.addDir('Animation','http://twomovies.name/browse_movies/Animation/byViews/all/','movieindex','','','dir')
        main.addDir('Biography','http://twomovies.name/browse_movies/Biography/byViews/all/','movieindex','','','dir')
        main.addDir('Comedy','http://twomovies.name/browse_movies/Comedy/byViews/all/','movieindex','','','dir')
        main.addDir('Crime','http://twomovies.name/browse_movies/Crime/byViews/all/','movieindex','','','dir')
        main.addDir('Documentary','http://twomovies.name/browse_movies/Documentary/byViews/all/','movieindex','','','dir')
        main.addDir('Drama','http://twomovies.name/browse_movies/Drama/byViews/all/','movieindex','','','dir')
        main.addDir('Family','http://twomovies.name/browse_movies/Family/byViews/all/','movieindex','','','dir')
        main.addDir('Fantastic','http://twomovies.name/browse_movies/Fantastic/byViews/all/','movieindex','','','dir')
        main.addDir('Fantasy','http://twomovies.name/browse_movies/Fantasy/byViews/all/','movieindex','','','dir')
        main.addDir('Film-Noir','http://twomovies.name/browse_movies/Film-Noir/byViews/all/','movieindex','','','dir')
        main.addDir('History','http://twomovies.name/browse_movies/History/byViews/all/','movieindex','','','dir')
        main.addDir('Music','http://twomovies.name/browse_movies/Music/byViews/all/','movieindex','','','dir')
        main.addDir('Mystery','http://twomovies.name/browse_movies/Mystery/byViews/all/','movieindex','','','dir')
        main.addDir('Reality-TV','http://twomovies.name/browse_movies/Reality-TV/byViews/all/','movieindex','','','dir')
        main.addDir('Romance','http://twomovies.name/browse_movies/Romance/byViews/all/','movieindex','','','dir')
        main.addDir('Sci-Fi','http://twomovies.name/browse_movies/Sci-Fi/byViews/all/','movieindex','','','dir')
        main.addDir('Thriller','http://twomovies.name/browse_movies/Thriller/byViews/all/','movieindex','','','dir')
        main.addDir('Western','http://twomovies.name/browse_movies/Western/byViews/all/','movieindex','','','dir')
        
        main.AUTO_VIEW('')


        
def PLAYYEAR (url):
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)" title=".+?">\n                        <img src="(.+?)" class=".+?" style=".+?"  border=".+?" height="147px" width="102px" alt="Watch (.+?) Online for Free">\n').findall(link)
        if len(match) > 0:
         for url,sitethumb,name in match:
          matchyear=re.compile('<a class="filmyar" href="http://twomovies.name/browse_movies/all/byViews/(.+?)/">').findall(link)
          if len(matchyear) > 0:
             for year in matchyear:        
                 data = main.GRABMETA(name,year)
                 #thumb = data['cover_url']               
                   
             favtype = 'movie'
             main.addDir(name+' ('+ year +')',url,'linkpage',sitethumb,data,favtype)
             nmatch=re.compile('<a id="next" class=".+?" href="(.+?)">Next &raquo</a>\n').findall(link)
        if len(nmatch) > 0:
                  main.addDir('Next Page',(nmatch[0]),'playyear','','','dir')
             
                  main.AUTO_VIEW('')

def MOVIETAGS(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)" style=".+?; font-style: .+?; font-variant: .+?; font-size-adjust: .+?; font-stretch:.+?; -x-system-font: .+?; color: .+?; font-weight:.+?; line-height: .+?; word-spacing: .+?; letter-spacing:.+?;font-size:.+?;margin:.+?;">(.+?)</a>').findall(link)
        for url,name in match:
                
                main.addDir(name,url,'movietagindex','','','dir')
                main.AUTO_VIEW('')
                
def MOVIETAGINDEX(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)">\n        <img src=".+?" data-original="(.+?)"  class=".+?" style=".+?"  border=".+?" height=".+?" width=".+?" alt="Watch (.+?) Online for Free">\n').findall(link)
        if len(match) > 0:
         for url,sitethumb,name in match:
          matchyear=re.compile('<a class="filmyar" href="http://twomovies.name/browse_movies/all/byViews/(.+?)/">').findall(link)
          if len(matchyear) > 0:
             for year in matchyear:        
                 data = main.GRABMETA(name,year)
                 #thumb = data['cover_url']               
                 
                            
             favtype = 'movie'
             main.addDir(name+' ('+ year +')',url,'linkpage',sitethumb,data,favtype)
             
             main.AUTO_VIEW('movies')

             
def MOVIEINDEX(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)" title=".+?">\n                        <img src="(.+?)" class=".+?" style=".+?"  border=".+?" height="147px" width="102px" alt="Watch (.+?) Online for Free">\n').findall(link)
        if len(match) > 0:
         for url,sitethumb,name in match:
          matchyear=re.compile('<a class="filmyar" href="http://twomovies.name/browse_movies/all/byViews/(.+?)/">').findall(link)
          if len(matchyear) > 0:
             for year in matchyear:        
                 data = main.GRABMETA(name,year)
                 #thumb = data['cover_url']               
                 
             main.addDir(name+' ('+ year +')',url,'linkpage',sitethumb,data,'')
             nmatch=re.compile('<a id="next" class=".+?" href="(.+?)">Next &raquo</a>\n').findall(link)
        if len(nmatch) > 0:
                    
                 main.addDir('Next Page',(nmatch[0]),'movieindex','','','dir')
             
                 main.AUTO_VIEW('movies')

                 
def MOVIEINDEX1(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)">\n        <img src=".+?" data-original="(.+?)"  class=".+?" style=".+?"  border=".+?" height=".+?" width=".+?" alt="Watch (.+?) Online for Free">\n').findall(link)
        if len(match) > 0:
         for url,sitethumb,name in match:
          matchyear=re.compile('<a class="filmyar" href=".+?">(.+?)</a>').findall(link)
          if len(matchyear) > 0:
             for year in matchyear:        
                 data = main.GRABMETA(name,year)
                 #thumb = data['cover_url']               
                      
             favtype = 'movie'
             main.addDir(name+' ('+ year +')',url,'linkpage',sitethumb,data,favtype)
             nmatch=re.compile('<a id="next" class=".+?" href="(.+?)">Next &raquo</a>\n').findall(link)
        if len(nmatch) > 0:
                  main.addDir('Next Page',(nmatch[0]),'movieindex1','','','dir')
             
                  main.AUTO_VIEW('movies')

             
def LINKPAGE(url,name):
        inc = 0
        movie_name = name[:-6]
        year = name[-6:]
        movie_name = movie_name.decode('UTF-8','ignore')
        link = net.http_GET(url).content
        match=re.compile('href="(.+?)" target=".+?" rel=".+?" onclick=".+? = \'.+?">Watch Movie!</a>\n                                                       </div>\n                        </td>\n                        <td valign=.+? style=.+?>\n                          <span class=.+?>&nbsp;Site:&nbsp;</span><span class=.+?>(.+?)</span>').findall(link)
        for url,linkname in match:
                 
          if inc < 50:
                        link = net.http_GET(url).content
                        urls=re.compile('<iframe.*?src="(http://.+?)".*?>').findall(link)

                        hmf = urlresolver.HostedMediaFile(urls[0])
                        if hmf:
                                host = hmf.get_host()
                                data = main.GRABMETA(movie_name,year)
                                thumb = data['cover_url']
                                try:
                                        main.addDir(movie_name + ' /Source =' + linkname ,url,'vidpage','','','')
                                        inc +=1
                                except:
                                        continue       
                   


def VIDPAGE(url,name):
        link = net.http_GET(url).content
        match=re.compile('<iframe.*?src="(http://.+?)".*?>').findall(link)
        
        for url in match:
                
                main.RESOLVE(name,url,'')
                
                



            
                

	
#Start Ketboard Function                
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default


#Start Search Function
def SEARCHM(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching for Movies" )
	# if blank or the user cancelled the keyboard, return
	if ( not vq ): return False, 0
	# we need to set the title to our query
	title = urllib.quote_plus(vq)
	searchUrl += title + '&criteria=title' 
	print "Searching URL: " + searchUrl 
	MOVIEINDEX1(searchUrl)

	main.AUTO_VIEW('movies')



	
def SEARCHT(url):
	searchUrl = url 
	vq = _get_keyboard( heading="TIME INTENSIVE!! Be Patient!!" )
	# if blank or the user cancelled the keyboard, return
	if ( not vq ): return False, 0
	# we need to set the title to our query
	title = urllib.quote_plus(vq)
	searchUrl += title + '&criteria=tag' 
	print "Searching URL: " + searchUrl 
	MOVIEINDEX1(searchUrl)

	main.AUTO_VIEW('movies')        

                
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
#May need toremove
#try:
 #       mode=int(params["mode"])
#except:
 #       pass

try:
        mode=urllib.unquote_plus(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)


if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
        
elif mode=='byyear':
        print ""
        BYYEAR()


elif mode=='genres':
        print ""
        GENRES()

        
elif mode=='playyear':
        print ""+url
        PLAYYEAR(url)      
       
elif mode=='movieindex':
        print ""+url
        MOVIEINDEX(url)

elif mode=='movietagindex':
        print ""+url
        MOVIETAGINDEX(url)        

elif mode=='movieindex1':
        print ""+url
        MOVIEINDEX1(url)

elif mode=='movietags':
        print ""+url
        MOVIETAGS(url)        
        
elif mode=='vidpage':
        print ""+url
        VIDPAGE(url,name)


elif mode=='linkpage':
        print ""+url
        LINKPAGE(url,name)

elif mode=='resolve':
        print ""+url
        main.RESOLVE(url,name)        


elif mode=='searchm':
        print ""+url
        SEARCHM(url)


elif mode=='searcht':
        print ""+url
        SEARCHT(url)        

elif mode=='resolverSettings':
        print ""+url
        urlresolver.display_settings()





xbmcplugin.endOfDirectory(int(sys.argv[1]))


