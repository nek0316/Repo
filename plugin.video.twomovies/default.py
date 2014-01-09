
#2Movies - Blazetamer


import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc, xbmcaddon, os, sys
import urlresolver
import cookielib
from resources.modules import status
from resources.modules import chia
import downloader
import extract
import time,re
import datetime
import shutil
import mechanize 
from resources.modules import tvshow
from metahandler import metahandlers
from resources.modules import main

try:
        from addon.common.addon import Addon

except:
        from t0mm0.common.addon import Addon
addon_id = 'plugin.video.twomovies'
addon = main.addon


try:
        from addon.common.net import Net

except:  
        from t0mm0.common.net import Net
net = Net(http_debug=True)
newagent ='Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
net.set_user_agent(newagent)

base_url = 'http://www.twomovies.name'


#PATHS
artwork = xbmc.translatePath(os.path.join('http://rowthreemedia.com/xbmchub/2movies/art/', ''))
settings = xbmcaddon.Addon(id='plugin.video.twomovies')
addon_path = os.path.join(xbmc.translatePath('special://home/addons'), '')

#========================DLStuff=======================
mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
ext = addon.queries.get('ext', '')
console = addon.queries.get('console', '')
dlfoldername = addon.queries.get('dlfoldername', '')
favtype = addon.queries.get('favtype', '')
mainimg = addon.queries.get('mainimg', '')
headers = addon.queries.get('headers', '')
loggedin = addon.queries.get('loggedin', '')
header_dict = addon.queries.get('header_dict', '')

print 'Mode is: ' + mode
print 'Url is: ' + url
print 'Name is: ' + name
print 'Thumb is: ' + thumb
print 'Extension is: ' + ext
print 'Filetype is: ' + console
print 'DL Folder is: ' + dlfoldername
print 'Favtype is: ' + favtype
print 'Main Image is: ' + mainimg
print 'Header_Dicts are ' + header_dict
print 'Logged In Status is ' +loggedin
#================DL END==================================
#########################Blazetamer's Log Module########################################
cookiejar = addon.get_profile()
cookiejar = os.path.join(cookiejar,'cookies.lwp')
def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")

username = settings.getSetting('tmovies_user')
password = settings.getSetting('tmovies_pass')

def LOGIN():
    username = settings.getSetting('tmovies_user')
    password = settings.getSetting('tmovies_pass')    
    header_dict = {}
    header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    header_dict['Connection'] = 'keep-alive'
    header_dict['Content-Type'] = 'application/x-www-form-urlencoded'
    header_dict['Host'] = 'twomovies.name'
    header_dict['Referer'] = 'http://www.twomovies.name/login'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'    
    form_data = {'login':username, 'password':password,'remember_me':'on','submit_login':'Login', 'submit_login':''}
    net.set_cookies(cookiejar)
    login = net.http_POST('http://twomovies.name/go_login', form_data=form_data, headers=header_dict)
    net.save_cookies(cookiejar)
    link = net.http_GET('http://twomovies.name/login').content
    logincheck=re.compile('<font class="form-title">Login (.+?)</font>').findall(link)
    for nolog in logincheck:
                    print 'Login Check Return is ' + nolog
                    if 'using TwoMovies account' in nolog :
                        LogNotify('Login Failed at twomovies.name', 'Check settings', '5000', 'http://addonrepo.com/xbmchub/Blazetamer/2movies.png')
                        CATEGORIES('false')
                        return True
    else:
                        LogNotify('Welcome Back ' + username, 'Enjoy your stay!', '5000', 'http://addonrepo.com/xbmchub/Blazetamer/2movies.png')
                        net.save_cookies(cookiejar)
                        CATEGORIES('true')
                        return False
  
def RELOGIN():
        if settings.getSetting('tmovies_account') == 'false':
                dialog = xbmcgui.Dialog()
                ok = dialog.ok('Account Login Not Enabled', '            Please Choose 2Movies Account Tab and Enable')
                if ok:
                        LogNotify('2Movies Account Tab ', 'Please Enable Account', '5000', 'http://addonrepo.com/xbmchub/Blazetamer/2movies.png')        
                        print 'YOU HAVE NOT SET THE USERNAME OR PASSWORD!'
                        addon.show_settings()
                                
        else:
            STARTUP()
        
def STARTUP():
        username = settings.getSetting('tmovies_user')
        password = settings.getSetting('tmovies_pass')
        cookiejar = addon.get_profile()
        cookiejar = os.path.join(cookiejar,'cookies.lwp')
        if settings.getSetting('tmovies_account') == 'true':
                if username is '' or password is '':
                        dialog = xbmcgui.Dialog()
                        ok = dialog.ok('Username or Password Not Set', '            Please Choose 2Movies Account Tab and Set')
                        if ok:
                                LogNotify('2Movies Account Tab ', 'Please set Username & Password!', '5000', 'http://addonrepo.com/xbmchub/Blazetamer/2movies.png')        
                                print 'YOU HAVE NOT SET THE USERNAME OR PASSWORD!'
                                addon.show_settings()
                #Add new Cookie*****************************
                #cookiejar = cookiejar.strip()                
                '''if not os.path.exists(cookiejar):
                        f = open(cookiejar, 'w')
                        f.write('#LWP-Cookies-2.0')
                        f.close()
                        #return cookiejar '''               
                #End Add new Cookie*****************************


                LOGIN()      
                       
        else:
              '''try:
                  os.remove(cookiejar)
              except:
                     pass'''  
              CATEGORIES('false')
#************************End Login****************************************************************************
#Main Links
def CATEGORIES(loggedin):
        if loggedin == 'true':
                main.addDir('[COLOR red][B]LOGGED IN[/COLOR][/B]','http://addonrepo.com/xbmchub/twomovies/messages/loggedintrue.txt','addonstatus',artwork +'loggedin.png','','dir')
        if loggedin == 'false':        
                main.addDir('[COLOR white][B]Login/Re-Attempt Login[/COLOR][/B]','none','relogin',artwork +'relogin.png','','dir')
                main.addDir('[COLOR white][B]How to Login[/COLOR][/B]','http://addonrepo.com/xbmchub/twomovies/messages/loggedinfalse.txt','addonstatus',artwork +'howtologin.png','','dir')
        main.addDir('[COLOR white]Movies[/COLOR]','none','moviecat',artwork +'Icon_Menu_Movies_Menu.png','','dir')     
        
        if settings.getSetting('tvshows') == 'true':
                main.addDir('[COLOR white]TV Shows[/COLOR]','none','tvcats',artwork +'Icon_Menu_TVShows_Menu.png','','dir')
        if settings.getSetting('chia') == 'true':
                main.addDir('[COLOR white]Chia-Anime[/COLOR]','none','chiacats',artwork +'anime/Anime_Chia_Anime.png','','dir')        
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
                main.addDir('[COLOR white]Two Movies Adults Only Section[/COLOR]','none','adultallow',artwork +'Icon_Menu_Adult.png'  ,'','dir')                                
        
        
        if settings.getSetting('resolver') == 'true':
                main.addDir('[COLOR white]Resolver Settings[/COLOR]','none','resolverSettings',artwork +'Icon_Menu_Settings_ResolverSettings.png','','dir')
        main.addDir('[COLOR white]Help and Extras[/COLOR]','http://addonrepo.com/xbmchub/twomovies/messages/addon.txt','statuscategories',artwork +'help.png','','dir')
        main.addDir('[COLOR gold]Manage Downloads[/COLOR]','none','viewQueue',artwork +'downloads/Downloads_Manage.png','','')
        main.addDir('[COLOR gold]Announcements/Info[/COLOR]','http://addonrepo.com/xbmchub/twomovies/messages/addonannouncements.txt','addonstatus','http://addonrepo.com/xbmchub/twomovies/images/icon.png','','')
        main.AUTO_VIEW('')



                       
def MOVIECAT():
        main.addDir('Movies by Popularity','http://twomovies.name/browse_movies/all/byViews/all/','playyear',artwork +'moviespopularity.png','','dir')
        main.addDir('Movies by Rating','http://twomovies.name/browse_movies/all/byRating/all/','playyear',artwork +'moviesrating.png','','dir')
        main.addDir('Trending Movies','http://twomovies.name/','movieindex1',artwork +'Icon_Menu_Movies_Popularandtrending.png','','dir')
        main.addDir('Newly Added Movies','http://twomovies.name/new_release/','movieindex1',artwork +'moviesnewlyadded.png','','dir')
        main.addDir('Movies by Year ','none','byyear',artwork +'Icon_Menu_Movies_Byyear.png','','dir')
        main.addDir('Movie Genres ','http://twomovies.name/','genres',artwork +'Icon_Menu_Movies_Genre.png','','dir')
        main.addDir('A-Z Index','none','mazindex',artwork +'moviesa-z.png','','dir')
        if settings.getSetting('movietags') == 'true':
                main.addDir('Movies by Tags ','http://twomovies.name/tags/','movietags',artwork +'Icon_Menu_ByTag.png','','dir')
        main.addDir('[COLOR gold]Search by Movie Name[/COLOR] ','http://twomovies.name/search/?search_query=','searchm',artwork +'Icon_Menu_Movies_SearchName.png','','dir')
        if settings.getSetting('movietags') == 'true':
                main.addDir('[COLOR gold]Search by Custom Tag[/COLOR] ','http://twomovies.name/search/?search_query=','searcht',artwork +'Icon_Menu_Movies_SearchCustomTag.png','','dir')
        main.AUTO_VIEW('')
        
def MAZINDEX():
     main.addDir('#','http://twomovies.name/letter/0/','azindex',artwork +'/movieaz/hash.png','','dir')
     main.addDir('A','http://twomovies.name/letter/A/','azindex',artwork +'/movieaz/a.png','','dir')
     main.addDir('B','http://twomovies.name/letter/B/','azindex',artwork +'/movieaz/b.png','','dir')
     main.addDir('C','http://twomovies.name/letter/C/','azindex',artwork +'/movieaz/c.png','','dir')
     main.addDir('D','http://twomovies.name/letter/D/','azindex',artwork +'/movieaz/d.png','','dir')
     main.addDir('E','http://twomovies.name/letter/E/','azindex',artwork +'/movieaz/e.png','','dir')
     main.addDir('F','http://twomovies.name/letter/F/','azindex',artwork +'/movieaz/f.png','','dir')
     main.addDir('G','http://twomovies.name/letter/G/','azindex',artwork +'/movieaz/g.png','','dir')
     main.addDir('H','http://twomovies.name/letter/H/','azindex',artwork +'/movieaz/h.png','','dir')
     main.addDir('I','http://twomovies.name/letter/I/','azindex',artwork +'/movieaz/i.png','','dir')
     main.addDir('J','http://twomovies.name/letter/J/','azindex',artwork +'/movieaz/j.png','','dir')
     main.addDir('K','http://twomovies.name/letter/K/','azindex',artwork +'/movieaz/k.png','','dir')
     main.addDir('L','http://twomovies.name/letter/L/','azindex',artwork +'/movieaz/l.png','','dir')
     main.addDir('M','http://twomovies.name/letter/M/','azindex',artwork +'/movieaz/m.png','','dir')
     main.addDir('N','http://twomovies.name/letter/N/','azindex',artwork +'/movieaz/n.png','','dir')
     main.addDir('O','http://twomovies.name/letter/O/','azindex',artwork +'/movieaz/o.png','','dir')
     main.addDir('P','http://twomovies.name/letter/P/','azindex',artwork +'/movieaz/p.png','','dir')
     main.addDir('Q','http://twomovies.name/letter/Q/','azindex',artwork +'/movieaz/q.png','','dir')
     main.addDir('R','http://twomovies.name/letter/R/','azindex',artwork +'/movieaz/r.png','','dir')
     main.addDir('S','http://twomovies.name/letter/S/','azindex',artwork +'/movieaz/s.png','','dir')
     main.addDir('T','http://twomovies.name/letter/T/','azindex',artwork +'/movieaz/t.png','','dir')
     main.addDir('U','http://twomovies.name/letter/U/','azindex',artwork +'/movieaz/u.png','','dir')
     main.addDir('V','http://twomovies.name/letter/V/','azindex',artwork +'/movieaz/v.png','','dir')
     main.addDir('W','http://twomovies.name/letter/W/','azindex',artwork +'/movieaz/w.png','','dir')
     main.addDir('X','http://twomovies.name/letter/X/','azindex',artwork +'/movieaz/x.png','','dir')
     main.addDir('Y','http://twomovies.name/letter/Y/','azindex',artwork +'/movieaz/y.png','','dir')
     main.addDir('Z','http://twomovies.name/letter/Z/','azindex',artwork +'/movieaz/z.png','','dir')
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
                
                main.addDir('View Adult Movies','http://twomovies.name/browse_movies/Adult/byViews/all/','adultmovieindex',artwork +'Icon_Menu_Adult.png','','dir')
        else:
                notice = xbmcgui.Dialog().ok('Wrong Passcode','The passcode you entered is incorrect')        

def BYYEAR():
        yearurl = 'http://twomovies.name/browse_movies/all/byViews/'
        main.addDir('2014 ',yearurl+'2014','playyear',artwork +'Icon_Menu_2014.png','','dir')
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

def AZINDEX(url):
        if settings.getSetting('tmovies_account') == 'true':  
              net.set_cookies(cookiejar)
        link = net.http_GET(url).content   
        match=re.compile('<a href="(.+?)">\r\n        <img src=".+?" data-original="(.+?)"  class=".+?" style=".+?"  border=".+?" height=".+?" width=".+?" alt="Watch (.+?) Online for Free">\r\n').findall(link)
        if len(match) > 0:
         for url,sitethumb,name in match:
          matchyear=re.compile('<a class="filmyar" href=".+?">(.+?)</a>').findall(link)
          #if len(matchyear) > 0:
          for year in matchyear:        
                 data = main.GRABMETA(name,year)
                 thumb = data['cover_url']               
                 yeargrab = data['year']
                 year = str(yeargrab)
          favtype = 'movie'
          if 'watch_movie' in url:
               
                main.addDir(name+ ' (' + year +')',url,'linkpage',thumb,data,favtype)
                
          nmatch=re.compile('<a id="next" class=".+?" href="(.+?)">Next &raquo</a>\n').findall(link)
        if len(nmatch) > 0:
                  main.addDir('Next Page',(nmatch[0]),'azindex',artwork +'Icon_Menu_Movies_nextpage.png','','dir')
             
        main.AUTO_VIEW('movies')
        
def PLAYYEAR (url):
        if settings.getSetting('tmovies_account') == 'true':  
              net.set_cookies(cookiejar)
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)" title=".+?">\r\n                        <img src="(.+?)" class=".+?" style=".+?"  border=".+?" height="147px" width="102px" alt="Watch (.+?) Online for Free">\r\n').findall(link)
        if len(match) > 0:
         for url,sitethumb,name in match:
          matchyear=re.compile('<a class="filmyar" href="http://twomovies.name/browse_movies/all/byViews/(.+?)/">').findall(link)
          if len(matchyear) > 0:
             for year in matchyear:        
                 data = main.GRABMETA(name,year)
                 thumb = data['cover_url']               
                 yeargrab = data['year']
                 year = str(yeargrab)               
                   
             favtype = 'movie'
             main.addDir(name+' ('+ year +')',url,'linkpage',thumb,data,favtype)
             nmatch=re.compile('<a id="next" class=".+?" href="(.+?)">Next &raquo</a>\n').findall(link)
        if len(nmatch) > 0:
                  main.addDir('Next Page',(nmatch[0]),'playyear',artwork +'Icon_Menu_Movies_nextpage.png','','dir')
             
        main.AUTO_VIEW('movies')

def MOVIETAGS(url):
        if settings.getSetting('tmovies_account') == 'true':  
              net.set_cookies(cookiejar)
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)" style=".+?; font-style: .+?; font-variant: .+?; font-size-adjust: .+?; font-stretch:.+?; -x-system-font: .+?; color: .+?; font-weight:.+?; line-height: .+?; word-spacing: .+?; letter-spacing:.+?;font-size:.+?;margin:.+?;">(.+?)</a>').findall(link)
        for url,name in match:
                
                main.addDir(name,url,'movietagindex',artwork +'Icon_Menu_Movies_ByTag.png','','dir')
        main.AUTO_VIEW('')
                
def MOVIETAGINDEX(url):
        if settings.getSetting('tmovies_account') == 'true':  
              net.set_cookies(cookiejar)
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)">\r\n        <img src=".+?" data-original="(.+?)"  class=".+?" style=".+?"  border=".+?" height=".+?" width=".+?" alt="Watch (.+?) Online for Free">\r\n').findall(link)
        if len(match) > 0:
         for url,sitethumb,name in match:
          matchyear=re.compile('<a class="filmyar" href="http://twomovies.name/browse_movies/all/byViews/(.+?)/">').findall(link)
          if len(matchyear) > 0:
             for year in matchyear:        
                 data = main.GRABMETA(name,year)
                 thumb = data['cover_url']               
                 yeargrab = data['year']
                 year = str(yeargrab)              
                 
                            
             favtype = 'movie'
             main.addDir(name+' ('+ year +')',url,'linkpage',thumb,data,favtype)
             
        main.AUTO_VIEW('movies')

def ADULTMOVIEINDEX(url):
        if settings.getSetting('tmovies_account') == 'true':  
              net.set_cookies(cookiejar)
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)" title=".+?">\r\n                        <img src="(.+?)" class=".+?" style=".+?"  border=".+?" height="147px" width="102px" alt="Watch (.+?) Online for Free">\r\n').findall(link)
        if len(match) > 0:
         for url,sitethumb,name in match:
          matchyear=re.compile('<a class="filmyar" href="http://twomovies.name/browse_movies/all/byViews/(.+?)/">').findall(link)
          if len(matchyear) > 0:
             for year in matchyear:        
                 data = main.GRABMETA(name,year)
                 thumb = data['cover_url']               
                 yeargrab = data['year']
                 year = str(yeargrab)               
             favtype = 'movie'   
             main.addDir(name+' ('+ year +')',url,'linkpage',thumb,data,favtype)
             nmatch=re.compile('<a id="next" class=".+?" href="(.+?)">Next &raquo</a>\n').findall(link)
        if len(nmatch) > 0:
                    
                 main.addDir('Next Page',(nmatch[0]),'movieindex',artwork +'Icon_Menu_Movies_nextpage.png','','dir')
             
        main.AUTO_VIEW('movies')             

             
def MOVIEINDEX(url):
        if settings.getSetting('tmovies_account') == 'true':  
              net.set_cookies(cookiejar)
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)" title=".+?">\r\n                        <img src="(.+?)" class=".+?" style=".+?"  border=".+?" height="147px" width="102px" alt="Watch (.+?) Online for Free">\r\n').findall(link)
        if len(match) > 0:
         for url,sitethumb,name in match:   
          matchyear=re.compile('<a class="filmyar" href="http://twomovies.name/browse_movies/all/byViews/(.+?)/">').findall(link)
          if len(matchyear) > 0:
             for year in matchyear:        
                 data = main.GRABMETA(name,year)
                 thumb = data['cover_url']               
                 yeargrab = data['year']
                 year = str(yeargrab)               
             favtype = 'movie'    
             main.addDir(name+' ('+ year +')',url,'linkpage',thumb,data,favtype)
             nmatch=re.compile('<a id="next" class=".+?" href="(.+?)">Next &raquo</a>\n').findall(link)
        if len(nmatch) > 0:
                    
                 main.addDir('Next Page',(nmatch[0]),'movieindex',artwork +'Icon_Menu_Movies_nextpage.png','','dir')
             
        main.AUTO_VIEW('movies')

                 
def MOVIEINDEX1(url):
        if settings.getSetting('tmovies_account') == 'true':  
              net.set_cookies(cookiejar)
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)">\r\n        <img src=".+?" data-original="(.+?)"  class=".+?" style=".+?"  border=".+?" height=".+?" width=".+?" alt="Watch (.+?) Online for Free">\r\n').findall(link)
        if len(match) > 0:
         for url,sitethumb,name in match: 
           matchyear=re.compile('<a class="filmyar" href=".+?">(.+?)</a>').findall(link)
           #matchview=re.compile('<span class="filmtime">(.+?)</span></div><br>').findall(link)
           if len(matchyear) > 0:
              for year in matchyear:
                 try:     
                         data = main.GRABMETA(name,year)
                         thumb = data['cover_url']               
                         yeargrab = data['year']
                         year = str(yeargrab)
                 except:
                         data = ''
                         thumb = sitethumb
                         year = year
              favtype = 'movie'
                  #if 'watch_movie' in url:
              try:        
                   main.addDir(name+ ' (' + year +')',url,'linkpage',thumb,data,favtype)
              except:
                   pass
              nmatch=re.compile('<a id="next" class=".+?" href="(.+?)">Next &raquo</a>\n').findall(link)
              if len(nmatch) > 0:
                     main.addDir('Next Page',(nmatch[0]),'movieindex1',artwork +'Icon_Menu_Movies_nextpage.png','','dir')
             
        main.AUTO_VIEW('movies')

             
'''def LINKPAGE(url,name):
        inc = 0
        movie_name = name[:-6]
        year = name[-6:]
        movie_name = movie_name.decode('UTF-8','ignore')
        dlfoldername = name
        link = net.http_GET(url).content
        match=re.compile('href="(.+?)" target=".+?" rel=".+?" onclick=".+? = \'.+?">Watch Movie!</a>\n                                                       </div>\n                        </td>\n                        <td valign=.+? style=.+?>\n                          <span class=.+?>&nbsp;Site:&nbsp;</span><span class=.+?>(.+?)</span>').findall(link)

        for url,linkname in match:
                 
          if inc < 50:
                        link = net.http_GET(url).content
                        urls=re.compile('<a rel="nofollow" href="(.+?)" target="_blank">').findall(link)

                        hmf = urlresolver.HostedMediaFile(urls[0])
                        if hmf:
                                host = hmf.get_host()
                                hthumb = main.GETHOSTTHUMB(host)
                                dlurl = urlresolver.resolve(url)
                                data = main.GRABMETA(movie_name,year)
                                thumb = data['cover_url']
                                favtype = 'movie'
                                mainimg = thumb
                                try:
                                        main.addDLDir(movie_name,url,'vidpage',hthumb,data,dlfoldername,favtype,mainimg)
                                        inc +=1
                                except:
                                        continue    '''

def LINKPAGE(url,name):
        inc = 0
        movie_name = name[:-6]
        year = name[-6:]
        movie_name = movie_name.decode('UTF-8','ignore')
        dlfoldername = name
        
        if settings.getSetting('tmovies_account') == 'true':  
              net.set_cookies(cookiejar)
        link = net.http_GET(url).content
        match=re.compile('href="(.+?)" target=".+?" rel=".+?" onclick=".+? = \'.+?">Watch Movie!</a>\n                                                       </div>\n                        </td>\n                        <td valign=.+? style=.+?>\n                          <span class=.+?>&nbsp;Site:&nbsp;</span><span class=.+?>(.+?)</span>').findall(link)
  
        for url,linkname in match:
            
                   
          if inc < 50:
                 #This gets around the Continue Button
                link = net.http_GET(url).content 
                conmatch=re.compile('/>Please click (.+?):</p>').findall(link)
                #formmatch=re.compile('input class="(.+?)" type="(.+?)" value="(.+?)" name="(.+?)" /').findall(link)
                for button in conmatch:
                        if 'continue button' in conmatch:
                                        conmatch =str(conmatch)
                                        print 'Button SAYS ' +conmatch
                                        url = url
                                        header_dict = {}
                                        header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
                                        header_dict['Connection'] = 'keep-alive'
                                        header_dict['Content-Type'] = 'application/x-www-form-urlencoded'
                                        header_dict['Host'] = 'twomovies.name'
                                        header_dict['Referer'] = url
                                        header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
                                        
                                        form_data = {'confirm':'Continue'}
                                        net.set_cookies(cookiejar)
                                        conbutton = net.http_POST(url, form_data=form_data,headers=header_dict)
                                
                  #This gets around the Continue Button
                #link = net.http_GET(url).content
                matchurl=re.compile('go=(.+?)"').findall(link)
                for urls in matchurl:
                
                  
  ################srting conversion########################
                
                 urls = str(urls)
                 print 'First urls is ' +urls       
                
##################Try to replace urlparts##################
                 
                 urls = urls.replace('&rel=nofollow','')
                        #hmf = urlresolver.HostedMediaFile(urls[0])  
                  ##########################################      
                  #returns true or false media file resolve
                 print 'Pre HMF url is  ' +urls
                 hmf = urlresolver.HostedMediaFile(urls)
                  ##########################################
                 print 'URLS is ' +urls
                 if hmf:
                          #try:
                                  host = hmf.get_host()
                                  hthumb = main.GETHOSTTHUMB(host)
                                  #dlurl = urlresolver.resolve(vidUrl)
                                  data = main.GRABMETA(movie_name,year)
                                  thumb = data['cover_url']
                                  favtype = 'movie'
                                  mainimg = thumb
                                  try:
                                          main.addDLDir(movie_name,urls,'vidpage',hthumb,data,dlfoldername,favtype,mainimg)
                                          inc +=1
                                  except:
                                          continue
                          #except:
                                  #pass
                   


def VIDPAGE(url,name):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':mainimg, 'dlfoldername':dlfoldername,}
       #link = net.http_GET(url).content
       # match=re.compile('<iframe.*?src="(http://.+?)".*?>').findall(link)
        
        #for url in match:
        url = url
        name = name
        thumb=mainimg
                
        main.RESOLVE2(name,url,thumb)


def DLVIDPAGE(url,name):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':mainimg, 'dlfoldername':dlfoldername,}
        #link = net.http_GET(url).content
        #match=re.compile('<iframe.*?src="(http://.+?)".*?>').findall(link)
        
        #for url in match:
                
                
        main.RESOLVEDL(name,url,thumb)                
                
                



            
                

	
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
year=None
imdb_id=None

#------added for Help Section
try:        
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass

try:        
        thumb=urllib.unquote_plus(params["thumb"])
except:
        pass

try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass

try:        
        filetype=urllib.unquote_plus(params["filetype"])
except:
        pass    

# END OF HelpSection addition ===========================================
    
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

try:
        year=urllib.unquote_plus(params["year"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Year: "+str(year)


if mode==None or url==None or len(url)<1:
        print ""
        STARTUP()
        
elif mode=='categories':
        print ""+loggedin
        CATEGORIES(loggedin)

elif mode=='login':
        print ""+url
        LOGIN(url)

elif mode=='relogin':
        print ""
        RELOGIN()          

        
elif mode=='helpmenu':
        print ""
        HELPMENU()

elif mode == "help list menu": 
        items = HELP(name)

elif mode == "wizardstatus":
        print""+url    
        items = WIZARDSTATUS(url)        


        
elif mode=='moviecat':
        print ""
        MOVIECAT()        

elif mode=='tvcats':
        print ""
        tvshow.TVCATS()

elif mode=='chiacats':
        print ""
        chia.CHIACATS()        

elif mode=='adultallow':
        print ""
        ADULTALLOW()        
        
elif mode=='byyear':
        print ""
        BYYEAR()
        
elif mode=='tvbyyear':
        print ""
        tvshow.TVBYYEAR()
        


elif mode=='genres':
        print ""
        GENRES()

elif mode=='tvgenres':
        print ""
        tvshow.TVGENRES()

elif mode=='chiaalph':
        print ""
        chia.CHIAALPH()        

        
elif mode=='mazindex':
        print ""
        MAZINDEX() 
        

        
elif mode=='playyear':
        print ""+url
        PLAYYEAR(url)


elif mode=='tvplayyear':
        print ""+url
        tvshow.TVPLAYYEAR(url)

        

elif mode=='tvplaygenre':
        print ""+url
        tvshow.TVPLAYGENRE(url)        

        
elif mode=='adultmovieindex':
        print ""+url
        ADULTMOVIEINDEX(url)

        
elif mode=='movieindex':
        print ""+url
        MOVIEINDEX(url)

elif mode=='lateshow':
        print ""+url
        tvshow.LATESHOW(url)

elif mode=='searchshow':
        print ""+url
        tvshow.SEARCHSHOW(url)        

elif mode=='movietagindex':
        print ""+url
        MOVIETAGINDEX(url)        

elif mode=='movieindex1':
        print ""+url
        MOVIEINDEX1(url)

elif mode=='azindex':
        print ""+url
        AZINDEX(url)        

elif mode=='movietags':
        print ""+url
        MOVIETAGS(url)        
        
elif mode=='vidpage':
        print ""+url
        VIDPAGE(url,name)


elif mode=='dlvidpage':
        print ""+url
        DLVIDPAGE(url,name)

elif mode=='dltvvidpage':
        print ""+url
        tvshow.DLTVVIDPAGE(url,name)        

elif mode=='chiadlvidpage':
        print ""+url
        chia.CHIADLVIDPAGE(url,name)        

elif mode=='tvvidpage':
        print ""+url
        tvshow.TVVIDPAGE(url,name)

elif mode=='chiavidpage':
        print ""+url
        chia.CHIAVIDPAGE(url,name)        


elif mode=='linkpage':
        print ""+url
        LINKPAGE(url,name)

elif mode=='azlinkpage':
        print ""+url
        tvshow.AZLINKPAGE(url,name)        

elif mode=='tvlinkpage':
        print ""+url
        tvshow.TVLINKPAGE(url,name,thumb,mainimg)

elif mode=='chialinkpage':
        print ""+url
        chia.CHIALINKPAGE(url,name,thumb)

elif mode=='chialatest':
        print ""+url
        chia.CHIALATEST(url)
        
elif mode=='chiaalphmain':
        print ""+url
        chia.CHIAALPHMAIN(url)

elif mode=='chiagenremain':
        print ""+url
        chia.CHIAGENREMAIN(url)
        

elif mode=='chiagenres':
        print ""+url
        chia.CHIAGENRES(url)        

elif mode=='episodes':
        print ""+url
        tvshow.EPISODES(url,name,thumb)

elif mode=='chiaepisodes':
        print ""+url
        chia.CHIAEPISODES(url,name,year,thumb)        

elif mode=='resolve':
        print ""+url
        main.RESOLVE(url,name,iconimage)

elif mode=='chiaresolve':
        print ""+url
        chia.CHIARESOLVE(url,name,iconimage)

elif mode=='videoresolve':
        print ""+url
        status.VIDEORESOLVE(url,name,iconimage)

elif mode=='ytvideoresolve':
        print ""+url
        status.YTVIDEORESOLVE(url,name,iconimage)        

elif mode=='resolve2':
        print ""+url
        main.RESOLVE2(name,url,thumb)

elif mode=='resolvedl':
        print ""+url
        main.RESOLVEDL(url,name,thumb,favtype)
        
elif mode=='resolvetvdl':
        print ""+url
        main.RESOLVETVDL(name,url,thumb,favtype)



elif mode=='searchm':
        print ""+url
        SEARCHM(url)

elif mode=='searchanime':
        print ""+url
        chia.SEARCHANIME(url)

elif mode=='chiasearch':
        print ""+url
        chia.CHIASEARCH(url)        

elif mode=='searchtv':
        print ""+url
        tvshow.SEARCHTV(url)

elif mode=='downloadFile':
        print ""+url
        main.downloadFile(url)

        
elif mode=='helpcatagories':
        print ""+url
        HELPCATEGORIES(url)

elif mode=='helpstat':
        HELPSTAT(name,url,description)
                


elif mode=='searcht':
        print ""+url
        SEARCHT(url)        

elif mode=='resolverSettings':
        print ""+url
        urlresolver.display_settings()

elif mode=='loginSettings':
        print ""+url
        addon.show_settings('tmovies_account')        

elif mode == "dev message":
    ADDON.setSetting('dev_message', value='run')
    dev_message()

elif mode=='helpwizard':
        HELPWIZARD(name,url,description,filetype)

#=================ForDL===========================
elif mode=='viewQueue':
        print ""+url
        main.viewQueue()

elif mode=='download':
        print ""+url
        main.download()

elif mode=='removeFromQueue':
        print ""+url
        main.removeFromQueue(name,url,thumb,ext,console)

elif mode=='killsleep':
        print ""+url
        main.KILLSLEEP()        

elif mode=='chiaresolvedl':
        print ""+url
        chia.CHIARESOLVEDL(url,name,thumb,favetype)        

#==================END DL=====================================
        
#==================Start Status/Help==========================
        
elif mode == "statuscategories": print""+url; items=status.STATUSCATEGORIES(url)
elif mode == "addonstatus": print""+url; items=status.ADDONSTATUS(url)
elif mode=='getrepolink': print""+url; items=status.GETREPOLINK(url)
elif mode=='getshorts': print""+url; items=status.GETSHORTS(url)
elif mode=='getrepo': status.GETREPO(name,url,description,filetype)
elif mode=='getvideolink': print""+url; items=status.GETVIDEOLINK(url)
elif mode=='getvideo': status.GETVIDEO(name,url,iconimage,description,filetype)
elif mode=='addoninstall': status.ADDONINSTALL(name,url,description,filetype)
elif mode=='addshortcuts': status.ADDSHORTCUTS(name,url,description,filetype)
elif mode=='addsource': status.ADDSOURCE(name,url,description,filetype)
elif mode=='playstream': status.PLAYSTREAM(name,url,iconimage,description)
xbmcplugin.endOfDirectory(int(sys.argv[1]))


