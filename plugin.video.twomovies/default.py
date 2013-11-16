
#2Movies - Blazetamer


import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc, xbmcaddon, os, sys
import urlresolver
import cookielib
from resources.modules import gethtml
from resources.modules import weblogin
import setup

from metahandler import metahandlers
from resources.modules import main
addon_id = 'plugin.video.twomovies'
from t0mm0.common.addon import Addon
addon = main.addon
from t0mm0.common.net import Net
net = Net()

base_url = 'http://www.twomovies.name'


#PATHS
artwork = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.twomovies/art/', ''))
settings = xbmcaddon.Addon(id='plugin.video.twomovies')
addon_path = os.path.join(xbmc.translatePath('special://home/addons'), '')

#******************NEWLOGIN ATTEMPT*************************************************************************

TMUSER = settings.getSetting('tmovies_user')
TMPASSWORD = settings.getSetting('tmovies_pass')
cookie_jar = setup.cookie_jar()
'''
def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")
def LOGIN():
  if settings.getSetting('tmovies_account') == 'true':      
    header_dict = {}
    header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header_dict['Accept-Encoding'] = 'gzip,deflate'
    header_dict['Accept-Language'] = 'en-US,en;q=0.8'
    header_dict['Connection'] = 'keep-alive'
    header_dict['Content-Type'] = 'application/x-www-form-urlencoded'
    header_dict['Host'] = 'twomovies.name'
    header_dict['Referer'] = 'twomovies.name'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'
    
    
    #### Get token ###
    net.set_cookies(cookie_jar)
    url = 'http://twomovies.name/login/'
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)
    
    header_dict['Referer'] = 'http://twomovies.name/login'
    ### Login ###	
    form_data = ({'login':TMUSER, 'password':TMPASSWORD,'submit_login':'Login','submit_login':''})	
    net.set_cookies(cookie_jar)
    loginlink = net.http_POST('http://twomovies.name/login', form_data=form_data, headers=header_dict).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)
    if 'Invalid Username/Email or password' in loginlink:
        LogNotify('[COLOR red]Not logged in at twomovies.name[/COLOR]', 'Check settings', '5000', '')
        CATEGORIES()
    else:
        LogNotify('[COLOR gold]Logged in at twomovies.name[/COLOR]', '', '5000', '')


  else:  
                       CATEGORIES()'''



#*********************END NEWLOGIN ATTEMPT**********************************************************************
#Login Setup****************************************************************************************************

cookiepath = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.twomovies/resources/modules/', ''))
def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")



def LOGIN(username,password,hidesuccess):
            
                logged_in = weblogin.doLogin(cookiepath,username,password)
                if logged_in == True:

                     LogNotify('Welcome back ',username,'4000','')
                     CATEGORIES()
                elif logged_in == False:

                         LogNotify('Login Failure',' Check Account Settings','4000','')
                         CATEGORIES()
        
def STARTUP():
        username = settings.getSetting('tmovies_user')
        password = settings.getSetting('tmovies_pass')
        if settings.getSetting('tmovies_account') == 'true':
                LOGIN(username,password,'')             
        else:  
                       CATEGORIES()

#Main Links 
def CATEGORIES():
        
        main.addDir('[COLOR gold]Popular and Trending Movies[/COLOR]','http://twomovies.name/','movieindex1',artwork +'Icon_Menu_Movies_Popularandtrending.png','','dir')     
        main.addDir('[COLOR gold]Movies by Year[/COLOR] ','none','byyear',artwork +'Icon_Menu_Movies_Byyear.png','','dir')
        main.addDir('[COLOR gold]Movie Genres[/COLOR] ','http://twomovies.name/','genres',artwork +'Icon_Menu_Movies_Genre.png','','dir')
        if settings.getSetting('movietags') == 'true':
                main.addDir('[COLOR gold]Movies by Tags[/COLOR] ','http://twomovies.name/tags/','movietags',artwork +'Icon_Menu_Movies_ByTag.png','','dir')
        main.addDir('[COLOR gold]Search by Movie Name[/COLOR] ','http://twomovies.name/search/?search_query=','searchm',artwork +'Icon_Menu_Movies_SearchName.png','','dir')
        if settings.getSetting('movietags') == 'true':
                main.addDir('[COLOR gold]Search by Custom Tag[/COLOR] ','http://twomovies.name/search/?search_query=','searcht',artwork +'Icon_Menu_Movies_SearchCustomTag.png','','dir')
        if settings.getSetting('tvshows') == 'true':
                main.addDir('TV Shows [COLOR red] Coming SOON [/COLOR] ','none','',artwork +'Icon_Menu_TVSHows_ComingSoon.png','','dir')
        if settings.getSetting('adult') == 'true':
                text_file = None
                if not os.path.exists(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.twomovies/")):
                        os.makedirs(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.twomovies/"))

                if not os.path.exists(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.twomovies/apc.24")):
                        pin = ''
                        notice = xbmcgui.Dialog().yesno('Would You Like To Set an Adult Passcode','Would you like to set a passcode for the adult movies section?','','')
                        if notice:
                                keyboard = xbmc.Keyboard(pin,'Choose A New Adult Movie Passcode')
                                keyboard.doModal()
                                if keyboard.isConfirmed():
                                        pin = keyboard.getText()
                                text_file = open(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.twomovies/apc.24"), "w")
                                text_file.write(pin)
                                text_file.close()
                        else:
                                text_file = open(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.twomovies/apc.24"), "w")
                                text_file.write(pin)
                                text_file.close()
                main.addDir('[COLOR gold]Adults Only Section[/COLOR]','none','adultallow',artwork +'Icon_Menu_Adult.png'  ,'','dir')                                
        
        
        if settings.getSetting('resolver') == 'true':
                main.addDir('[COLOR gold]Resolver Settings[/COLOR]','none','resolverSettings',artwork +'Icon_Menu_Settings_ResolverSettings.png','','dir')
        
        
        main.AUTO_VIEW('')

def ADULTALLOW():
        text_file = open(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.twomovies/apc.24"), "r")
        line = file.readline(text_file)
        pin = ''
        if not line == '':
                keyboard = xbmc.Keyboard(pin,'Enter Your Passcode')
                keyboard.doModal()
                if keyboard.isConfirmed():
                        pin = keyboard.getText()
        
        if pin == line:
                
                main.addDir('[COLOR gold]View Adult Movies[/COLOR]','http://twomovies.name/browse_movies/Adult/byViews/all/','adultmovieindex',artwork +'Icon_Menu_Adult.png','','dir')
        else:
                notice = xbmcgui.Dialog().ok('Wrong Passcode','The passcode you entered is incorrect')        

def BYYEAR():
        yearurl = 'http://twomovies.name/browse_movies/all/byViews/'
        main.addDir('2013 ',yearurl+'2013','playyear',artwork +'Icon_Menu_2013.png','','dir')
        main.addDir('2012 ',yearurl+'2012','playyear',artwork +'Icon_Menu_2012.png','','dir')
        main.addDir('2011 ',yearurl+'2011','playyear',artwork +'Icon_Menu_2011.png','','dir')
        main.addDir('2010 ',yearurl+'2010','playyear',artwork +'Icon_Menu_2010.png','','dir')
        main.addDir('2009 ',yearurl+'2009','playyear',artwork +'Icon_Menu_2009.png','','dir')
        main.addDir('2008 ',yearurl+'2008','playyear',artwork +'Icon_Menu_2008.png','','dir')
        main.addDir('2007 ',yearurl+'2007','playyear',artwork +'Icon_Menu_2007.png','','dir')
        main.addDir('2006 ',yearurl+'2006','playyear',artwork +'Icon_Menu_2006.png','','dir')
        main.addDir('2005 ',yearurl+'2005','playyear',artwork +'Icon_Menu_2005.png','','dir')
        main.addDir('2004 ',yearurl+'2004','playyear',artwork +'Icon_Menu_2004.png','','dir')
        main.addDir('2003 ',yearurl+'2003','playyear',artwork +'Icon_Menu_2003.png','','dir')
        main.addDir('2002 ',yearurl+'2002','playyear',artwork +'Icon_Menu_2002.png','','dir')
        main.addDir('2001 ',yearurl+'2001','playyear',artwork +'Icon_Menu_2001.png','','dir')
        main.addDir('2000 ',yearurl+'2000','playyear',artwork +'Icon_Menu_2000.png','','dir')
        main.addDir('1999 ',yearurl+'1999','playyear',artwork +'Icon_Menu_1999.png','','dir')
        main.addDir('1998 ',yearurl+'1998','playyear',artwork +'Icon_Menu_1998.png','','dir')
        
        

def GENRES():
        
        main.addDir('Action','http://twomovies.name/browse_movies/Action/byViews/all/','movieindex',artwork +'Icon_Menu_action.png','','dir')
        main.addDir('Adventure','http://twomovies.name/browse_movies/Adventure/byViews/all/','movieindex',artwork +'Icon_Menu_adventure.png','','dir')
        main.addDir('Animation','http://twomovies.name/browse_movies/Animation/byViews/all/','movieindex',artwork +'Icon_Menu_animation.png','','dir')
        main.addDir('Biography','http://twomovies.name/browse_movies/Biography/byViews/all/','movieindex',artwork +'Icon_Menu_biography.png','','dir')
        main.addDir('Comedy','http://twomovies.name/browse_movies/Comedy/byViews/all/','movieindex',artwork +'Icon_Menu_comedy.png','','dir')
        main.addDir('Crime','http://twomovies.name/browse_movies/Crime/byViews/all/','movieindex',artwork +'Icon_Menu_crime.png','','dir')
        main.addDir('Documentary','http://twomovies.name/browse_movies/Documentary/byViews/all/','movieindex',artwork +'Icon_Menu_documentary.png','','dir')
        main.addDir('Drama','http://twomovies.name/browse_movies/Drama/byViews/all/','movieindex',artwork +'Icon_Menu_drama.png','','dir')
        main.addDir('Family','http://twomovies.name/browse_movies/Family/byViews/all/','movieindex',artwork +'Icon_Menu_family.png','','dir')
        main.addDir('Fantastic','http://twomovies.name/browse_movies/Fantastic/byViews/all/','movieindex',artwork +'Icon_Menu_fantastic.png','','dir')
        main.addDir('Fantasy','http://twomovies.name/browse_movies/Fantasy/byViews/all/','movieindex',artwork +'Icon_Menu_fantasy.png','','dir')
        main.addDir('Film-Noir','http://twomovies.name/browse_movies/Film-Noir/byViews/all/','movieindex',artwork +'Icon_Menu_film-noir.png','','dir')
        main.addDir('History','http://twomovies.name/browse_movies/History/byViews/all/','movieindex',artwork +'Icon_Menu_history.png','','dir')
        main.addDir('Horror','http://twomovies.name/browse_movies/Horror/byViews/all/','movieindex',artwork +'Icon_Menu_horror.png','','dir')
        main.addDir('Music','http://twomovies.name/browse_movies/Music/byViews/all/','movieindex',artwork +'Icon_Menu_music.png','','dir')
        main.addDir('Mystery','http://twomovies.name/browse_movies/Mystery/byViews/all/','movieindex',artwork +'Icon_Menu_mystery.png','','dir')
        main.addDir('Reality-TV','http://twomovies.name/browse_movies/Reality-TV/byViews/all/','movieindex',artwork +'Icon_Menu_reality-tv.png','','dir')
        main.addDir('Romance','http://twomovies.name/browse_movies/Romance/byViews/all/','movieindex',artwork +'Icon_Menu_romance.png','','dir')
        main.addDir('Sci-Fi','http://twomovies.name/browse_movies/Sci-Fi/byViews/all/','movieindex',artwork +'Icon_Menu_sci-fi.png','','dir')
        main.addDir('Thriller','http://twomovies.name/browse_movies/Thriller/byViews/all/','movieindex',artwork +'Icon_Menu_thriller.png','','dir')
        main.addDir('Western','http://twomovies.name/browse_movies/Western/byViews/all/','movieindex',artwork +'Icon_Menu_western.png','','dir')
        
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
                  main.addDir('Next Page',(nmatch[0]),'playyear',artwork +'Icon_Menu_Movies_nextpage.png','','dir')
             
                  main.AUTO_VIEW('movies')

def MOVIETAGS(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)" style=".+?; font-style: .+?; font-variant: .+?; font-size-adjust: .+?; font-stretch:.+?; -x-system-font: .+?; color: .+?; font-weight:.+?; line-height: .+?; word-spacing: .+?; letter-spacing:.+?;font-size:.+?;margin:.+?;">(.+?)</a>').findall(link)
        for url,name in match:
                
                main.addDir(name,url,'movietagindex',artwork +'Icon_Menu_Movies_ByTag.png','','dir')
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

def ADULTMOVIEINDEX(url):
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
                    
                 main.addDir('Next Page',(nmatch[0]),'movieindex',artwork +'Icon_Menu_Movies_nextpage.png','','dir')
             
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
             favtype = 'movie'    
             main.addDir(name+' ('+ year +')',url,'linkpage',sitethumb,data,favtype)
             nmatch=re.compile('<a id="next" class=".+?" href="(.+?)">Next &raquo</a>\n').findall(link)
        if len(nmatch) > 0:
                    
                 main.addDir('Next Page',(nmatch[0]),'movieindex',artwork +'Icon_Menu_Movies_nextpage.png','','dir')
             
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
                  main.addDir('Next Page',(nmatch[0]),'movieindex1',artwork +'Icon_Menu_Movies_nextpage.png','','dir')
             
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
                                hthumb = main.GETHOSTTHUMB(host)
                                data = main.GRABMETA(movie_name,year)
                                thumb = data['cover_url']
                                try:
                                        #main.addDir(movie_name + ' /Source =' + linkname ,url,'vidpage',thumb,'','')
                                        main.addDir(movie_name,url,'vidpage',hthumb,'','')
                                        #main.addHDir(movie_name,urls,'resolve2',thumb,hthumb)
                                        inc +=1
                                except:
                                        continue       
                   


def VIDPAGE(url,name):
        link = net.http_GET(url).content
        match=re.compile('<iframe.*?src="(http://.+?)".*?>').findall(link)
        
        for url in match:
                
                main.RESOLVE2(name,url,'')
                
                



            
                

	
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
        STARTUP()
        
elif mode=='categories':
        print ""
        CATEGORIES()

elif mode=='adultallow':
        print ""
        ADULTALLOW()        
        
elif mode=='byyear':
        print ""
        BYYEAR()


elif mode=='genres':
        print ""
        GENRES()

        
elif mode=='playyear':
        print ""+url
        PLAYYEAR(url)
        
elif mode=='adultmovieindex':
        print ""+url
        ADULTMOVIEINDEX(url)

        
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
        main.RESOLVE(url,name,iconimage)

elif mode=='resolve2':
        print ""+url
        main.RESOLVE2(url,name,thumb)        


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


