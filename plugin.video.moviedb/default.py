
#Default moviedb - Blazetamer


import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc, xbmcaddon, os, sys
import urlresolver
import cookielib
from resources.modules import status
import downloader
import extract
import time,re
import datetime
import shutil
from resources.modules import tvshow
from metahandler import metahandlers
from resources.modules import main
from resources.modules import moviedc
from resources.modules import sgate
from resources.modules import chia, supertoons
from resources.modules import chanufc, epornik, live

try:
        from addon.common.addon import Addon

except:
        from t0mm0.common.addon import Addon
addon_id = 'plugin.video.moviedb'
addon = main.addon
ADDON = xbmcaddon.Addon(id='plugin.video.moviedb')
xmlpath = 'http://addonrepo.com/xbmchub/moviedb/messages/skins/DefaultSkin/720p/'


try:
        from addon.common.net import Net

except:  
        from t0mm0.common.net import Net
net = Net(http_debug=True)
newagent ='Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
net.set_user_agent(newagent)

base_url = 'http://www.merdb.ru/'


#PATHS
#language            = xbmcaddon.Addon().getLocalizedString
artwork = xbmc.translatePath(os.path.join('http://addonrepo.com/xbmchub/moviedb/images/', ''))
settings = xbmcaddon.Addon(id='plugin.video.moviedb')
addon_path = os.path.join(xbmc.translatePath('special://home/addons'), '')
fanart = 'http://addonrepo.com/xbmchub/moviedb/images/fanart2.jpg'
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
season = addon.queries.get('season', '')
episode = addon.queries.get('episode', '')
repourl = addon.queries.get('repourl', '')

print 'Mode is: ' + mode
print 'Url is: ' + url
print 'Name is: ' + name
print 'Thumb is: ' + thumb
print 'Extension is: ' + ext
print 'Filetype is: ' + console
print 'DL Folder is: ' + dlfoldername
print 'Favtype is: ' + favtype
print 'Main Image is: ' + mainimg
print 'Headers are ' +headers
print 'Logged In Status is ' +loggedin
print 'RepoUrl is ' +repourl
#================DL END==================================
#########################Blazetamer's Login Module########################################
cookiejar = addon.get_profile()
cookiejar = os.path.join(cookiejar,'cookies.lwp')
def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")

        
def STARTUP():
        CATEGORIES('false')
#************************End Login****************************************************************************
#Main Links
def CATEGORIES(loggedin):
        main.addDir('[COLOR blue][B]WELCOME TO MDB ULTRA[/B] [/COLOR]','none','categories',artwork +'icon.png','','dir')
        #main.addDir('[COLOR blue]**Choose an Option Below**[/COLOR]','none','categories',artwork +'icon.png','','dir')
        if settings.getSetting('adult') == 'true':
                text_file = None
                if not os.path.exists(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.moviedb/")):
                        os.makedirs(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.moviedb/"))

                if not os.path.exists(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.moviedb/apc.69")):
                        pin = ''
                        notice = xbmcgui.Dialog().yesno('Would You Like To Set an Adult Passcode','Would you like to set a passcode for the adult movies section?','','')
                        if notice:
                                keyboard = xbmc.Keyboard(pin,'Choose A New Adult Movie Passcode')
                                keyboard.doModal()
                                if keyboard.isConfirmed():
                                        pin = keyboard.getText()
                                text_file = open(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.moviedb/apc.69"), "w")
                                text_file.write(pin)
                                text_file.close()
                        else:
                                text_file = open(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.moviedb/apc.69"), "w")
                                text_file.write(pin)
                                text_file.close()
                main.addDir('[COLOR white]Adults Only[/COLOR]','none','adultcats',artwork +'adult.jpg','','dir')
                
        main.addDir('[COLOR white]Movies[/COLOR]','none','moviecat',artwork +'movies.jpg','','dir')
        main.addDir('[COLOR white]TV Shows[/COLOR]','none','tvcats',artwork +'tvshows.jpg','','dir')
        if settings.getSetting('toons') == 'true':
                main.addDir('[COLOR white]Cartoons[/COLOR]','none','cartooncats',artwork +'cartoons.jpg','','dir')
        if settings.getSetting('sports') == 'true':        
                main.addDir('[COLOR white]Sports[/COLOR]','none','sportcats',artwork +'sports.jpg','','dir')
        if settings.getSetting('streams') == 'true':        
                main.addDir('[COLOR white]Live Streams[/COLOR]','http://goo.gl/1EMDrC','livecats',artwork +'live.jpg','','dir')
        if settings.getSetting('resolver') == 'true':
                main.addDir('[COLOR gold]Resolver Settings[/COLOR]','none','resolverSettings',artwork +'resolversettings.jpg','','dir')
        if settings.getSetting('addons') == 'true':        
                main.addDir("[COLOR gold]Browse More Addons by Blazetamer[/COLOR]",'http://addons.xbmchub.com/author/Blazetamer/','addonlist',artwork +'moreaddons.jpg','','')
                main.addDir('[COLOR gold]Get the Addon Browser Here[/COLOR]','http://addons.xbmchub.com/search/?keyword=browser','addonlist',artwork +'addonbrowser.jpg','','dir')
        if settings.getSetting('special') == 'true':        
                main.addDir('[COLOR gold]Special Menus/Announcements[/COLOR]','none','pop',artwork +'announcements.jpg','','dir')
        #main.addDir('[COLOR gold]About MDB Ultra[/COLOR]','http://addonrepo.com/xbmchub/moviedb/messages/addon.txt','statuscategories',artwork +'icon.png','','dir')
        #main.addDir('[COLOR red]Shut Down XBMC[/COLOR]','none','shutdownxbmc',artwork +'shutdown.png','','dir')
        main.addDir('[COLOR red]Manage Downloads[/COLOR]','none','viewQueue',artwork +'downloadsmanage.jpg','','')
#======================Developer Testing Section========================================================================        
        #main.addDir('[COLOR gold]Test Functions[/COLOR]','none','testfunction',artwork +'shutdown.png','','dir')
        
        main.AUTO_VIEW('')

def TESTFUNCTION():

        link=OPEN_URL('http://addonrepo.com/xbmchub/moviedb/controls/xmlcontroltest.txt').replace('\n','').replace('\r','')
        match=re.compile('name="(.+?)"').findall(link)
        for winxml in match:
                
                testwin = TEST(winxml,'http://addonrepo.com/xbmchub/moviedb/','DefaultSkin',close_time=60,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%ADDON.getAddonInfo('path'))
                #testwin = TEST(winxml,ADDON.getAddonInfo('path'),'DefaultSkin''DefaultSkin',close_time=60,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%ADDON.getAddonInfo('path'))
                testwin.doModal()
                #MERDBMOVIES()
                #xbmc.executebuiltin ("PreviousMenu")
                del testwin

                
class TEST( xbmcgui.WindowXMLDialog ): 
    def __init__( self, *args, **kwargs ):
        self.shut = kwargs['close_time'] 
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        xbmc.executebuiltin( "Skin.SetBool(AnimeWindowXMLDialogClose)" )
                                       
    def onInit( self ):
        #xbmc.Player().play('%s/resources/skins/DefaultSkin/media/xbmchub.mp3'%ADDON.getAddonInfo('path'))# Music.
        '''xbmc.Player().play(''%ADDON.getAddonInfo('path'))# Music.
        while self.shut > 0:
            xbmc.sleep(1000)
            self.shut -= 1
        xbmc.Player().stop()
        self._close_dialog()'''
                
    def onFocus( self, controlID ): pass
    
    def onClick( self, controlID ): 
        if controlID == 12:
            xbmc.Player().stop()
            self._close_dialog()

    def onAction( self, action ):
        if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
            xbmc.Player().stop()
            self._close_dialog()

    def _close_dialog( self ):
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        time.sleep( .4 )
        self.close()     
                        
                     
            
        
def SHUTDOWNXBMC():
        xbmc.executebuiltin('XBMC.ActivateWindow(111)')


def MERDBMOVIES():
        main.addDir('All Movies','http://www.merdb.ru/','movieindex',artwork +'all.jpg','','dir')
        main.addDir('Featured Movies','http://www.merdb.ru/?featured=1&sort=stamp','movieindex',artwork +'featured.jpg','','dir')
        main.addDir('Movies by Popularity','http://www.merdb.ru/?sort=views','movieindex',artwork +'popular.jpg','','dir')
        main.addDir('Movies by Rating','http://www.merdb.ru/?sort=ratingp','movieindex',artwork +'rating.jpg','','dir')
        main.addDir('Movies by Genre','none','genres',artwork +'genre.jpg','','dir')
        main.addDir('Movies by Release Date','http://www.merdb.ru/?sort=year','movieindex',artwork +'releasedate.jpg','','dir')
        main.addDir('Movies by Date Added','http://www.merdb.ru/?sort=stamp','movieindex',artwork +'dateadded.jpg','','dir')
        main.addDir('[COLOR gold]Search Movies[/COLOR]','http://www.merdb.ru/?search=','searchm',artwork + 'search.jpg','','dir')
        main.AUTO_VIEW('')
        
        

                       
def MOVIECAT():
        main.addDir('Movies [COLOR red](MerDB)[/COLOR] ','none','merdbmovies',artwork +'merdbmovies.jpg','','dir')
        main.addDir('Movies [COLOR red](Movie DataCenter)[/COLOR]','none','moviedccats',artwork +'moviedcmovies.jpg','','dir')
        main.addDir('[COLOR gold]**More Movies Coming Soon**[/COLOR]','none','moviecat',artwork +'merdbmovies.jpg','','dir')
        
        
        main.AUTO_VIEW('')

def TVCATS():        
        main.addDir('TV Shows [COLOR red](MerDB)[/COLOR]','none','merdbtvcats',artwork +'merdbtv.jpg','','dir')
        main.addDir('TV Shows [COLOR red](Series Gate)[/COLOR]','none','sgcats',artwork +'sgatetv.jpg','','dir')
        main.addDir('[COLOR gold]**More TV Shows Coming Soon**[/COLOR]','none','tvcats',artwork +'merdbtv.jpg','','dir')
        
        main.AUTO_VIEW('')
  
def CARTOONCATS():
        main.addDir('[COLOR white]Chia-Anime[/COLOR]','none','chiacats',artwork +'chiaanime.jpg','','dir')
        main.addDir('[COLOR white]SuperToons[/COLOR]','none','supertoonscats',artwork +'supertoons.jpg','','dir')
        main.addDir('[COLOR gold]**More Cartoons Coming Soon**[/COLOR]','none','cartooncats',artwork +'comingsoon.jpg','','dir')
        
def SPORTCATS():
        main.addDir('[COLOR white]UFC[/COLOR]','none','chanufccats',artwork +'ufc.jpg','','dir')
        main.addDir('[COLOR gold]**More Sports Coming Soon** [/COLOR]','none','sportcats',artwork +'comingsoon.jpg','','dir')
        
def ADULTCATS():
        main.addDir('[COLOR white]Eporn[/COLOR]','none','epornikCategories',artwork +'eporn.jpg','','dir')
        main.addDir('[COLOR blue]Adult Streams [COLOR green]Online[/COLOR]','http://addonrepo.com/xbmchub/moviedb/streams/adultstreams.xml','livecatslist',artwork +'adult.jpg','','dir')
        #main.addDir('[COLOR gold]**More Sports Coming Soon** [/COLOR]','none','adultcats',artwork +'comingsoon.jpg','','dir')
        

        

def GENRES():
        genurl = 'http://www.merdb.ru/?genre='
        main.addDir('Action',genurl +'Action','movieindex',artwork +'action.jpg','','dir')
        main.addDir('Adventure',genurl +'Adventure','movieindex',artwork +'adventure.jpg','','dir')
        main.addDir('Animation',genurl +'Animation','movieindex',artwork +'animation.jpg','','dir')
        main.addDir('Biography',genurl +'Biography','movieindex',artwork +'biography.jpg','','dir')
        main.addDir('Comedy',genurl +'Comedy','movieindex',artwork +'comedy.jpg','','dir')
        main.addDir('Crime',genurl +'Crime','movieindex',artwork +'crime.jpg','','dir')
        main.addDir('Documentary',genurl +'Documentary','movieindex',artwork +'documentary.jpg','','dir')
        main.addDir('Drama',genurl +'Drama','movieindex',artwork +'drama.jpg','','dir')
        main.addDir('Family',genurl +'Family','movieindex',artwork +'family.jpg','','dir')
        main.addDir('Fantasy',genurl +'Fantasy','movieindex',artwork +'fantasy.jpg','','dir')
        main.addDir('History',genurl +'History','movieindex',artwork +'history.jpg','','dir')
        main.addDir('Horror',genurl +'Horror','movieindex',artwork +'horror.jpg','','dir')
        main.addDir('Music',genurl +'Music','movieindex',artwork +'music.jpg','','dir')
        main.addDir('Mystery',genurl +'Mystery','movieindex',artwork +'mystery.jpg','','dir')
        main.addDir('Romance',genurl +'Romance','movieindex',artwork +'romance.jpg','','dir')
        main.addDir('Sci-Fi',genurl +'Sci-Fi','movieindex',artwork +'scifi.jpg','','dir')
        main.addDir('Thriller',genurl +'Thriller','movieindex',artwork +'thriller.jpg','','dir')
        main.addDir('War',genurl +'War','movieindex',artwork +'western.jpg','','dir')
        
        main.AUTO_VIEW('')

             
def MOVIEINDEX(url):
        link = net.http_GET(url).content
        match=re.compile('<img src="(.+?)" class=".+?" alt=".+?"/></a><div class=".+?"><a href="(.+?)" title="Watch(.+?)">.+?</a>').findall(link)
        if len(match) > 0:
         for sitethumb,url,name in match:
                
                inc = 0
                movie_name = name[:-6]
                year = name[-6:]
                movie_name = movie_name.decode('UTF-8','ignore')
              
                data = main.GRABMETA(movie_name,year)
                thumb = data['cover_url']               
                yeargrab = data['year']
                year = str(yeargrab)               

                favtype = 'movie'
                main.addDir(name,base_url + url,'linkpage',thumb,data,favtype)
                
         nmatch=re.compile('<span class="currentpage">.+?</span></li><li><a href="(.+?)">(.+?)</a></li><li>').findall(link)
         if len(nmatch) > 0: 
          for pageurl,pageno in nmatch:
                     
                main.addDir('Page'+ pageno,base_url + pageurl,'movieindex',artwork +'nextpage.jpg','','dir')
             
        main.AUTO_VIEW('movies')

                 
def MOVIEINDEX1(url):
        link = net.http_GET(url).content
        link = net.http_GET(url).content
        match=re.compile('<img src="(.+?)" class=".+?" alt=".+?"/></a><div class=".+?"><a href="(.+?)" title="Watch(.+?)">.+?</a>').findall(link)
        if len(match) > 0:
         for sitethumb,url,name in match:
                 try:     
                         inc = 0
                         movie_name = name[:-6]
                         year = name[-6:]
                         movie_name = movie_name.decode('UTF-8','ignore')
              
                         data = main.GRABMETA(movie_name,year)
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
                   main.addDir(name,base_url + url,'linkpage',thumb,data,favtype)
         except:
                   pass
         nmatch=re.compile('<span class="currentpage">.+?</span></li><li><a href="(.+?)">(.+?)</a></li><li>').findall(link)
         if len(nmatch) > 0:
                for pageurl,pageno in nmatch:
                      main.addDir('Page'+ pageno,base_url + pageurl,'movieindex',artwork +'nextpage.jpg','','dir')
             
        main.AUTO_VIEW('movies')

             

def LINKPAGE(url,name):
        inc = 0
        movie_name = name[:-6]
        year = name[-6:]
        movie_name = movie_name.decode('UTF-8','ignore')
        dlfoldername = name
        link = net.http_GET(url).content
        match=re.compile('<span class="movie_version_link"> <a href="/(.+?)"').findall(link)
  
        for url in match:
         url = base_url + url
              
            
                   
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
	MOVIEINDEX(searchUrl)

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


#==============POP UP FUNCTION==================
def OPEN_URL(url):
  req=urllib2.Request(url)
  req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  response=urllib2.urlopen(req)
  link=response.read()
  response.close()
  return link

def POP():
     link=OPEN_URL('http://addonrepo.com/xbmchub/moviedb/controls/xmlcontrol.txt').replace('\n','').replace('\r','')
     match=re.compile('ame="(.+?)".+?ndroid="(.+?)"').findall(link)
     for xml,xmlone in match:       
                #status.ADDONSTATUS(url) 
    

    
      if xbmc.getCondVisibility('system.platform.ios'):
        if not xbmc.getCondVisibility('system.platform.atv'):
            popup = PUM(xmlone,'http://addonrepo.com/xbmchub/moviedb/','DefaultSkin')#,close_time=60,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%ADDON.getAddonInfo('path'))
      elif xbmc.getCondVisibility('system.platform.android'):
        popup = PUM(xmlone,'http://addonrepo.com/xbmchub/moviedb/','DefaultSkin')#,close_time=60,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%ADDON.getAddonInfo('path'))
      else:
        popup = PUM(xml,'http://addonrepo.com/xbmchub/moviedb/','DefaultSkin')#,close_time=60,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%ADDON.getAddonInfo('path'))

      popup.doModal()
      del popup
    
        #link=OPEN_URL('http://addonrepo.com/xbmchub/moviedb/messages/popupchoice.txt').replace('\n','').replace('\r','')
        #match=re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ype="(.+?)"').findall(link)
        #for name,url,iconimage,fanart,description,filetype in match:       
                #status.ADDONSTATUS(url) 
    
                
def CHECKDATE(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 1000) #force update


def CHECK_POPUP():
        if settings.getSetting('announce') == 'true':
                threshold = int(settings.getSetting('anno_int') ) - 1
                now   = datetime.datetime.today()
                prev  = CHECKDATE(settings.getSetting('pop_time'))
                delta = now - prev
                nDays = delta.days

                doUpdate = (nDays > threshold)
                if not doUpdate:
                        return

                settings.setSetting('pop_time', str(now).split('.')[0])
                            
                POP()
                           

class PUM( xbmcgui.WindowXMLDialog ): 
    #def __init__( self, *args, **kwargs ):
    def __init__( self, *args ):
        #self.shut = kwargs['close_time']   
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        xbmc.executebuiltin( "Skin.SetBool(AnimeWindowXMLDialogClose)" )
        
                
    def onFocus( self, controlID ): pass
    
    def onClick( self, controlID ): 
        if controlID == 12:
            xbmc.Player().stop()
            self._close_dialog()

    def onAction( self, action ):
        if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
            xbmc.Player().stop()
            self._close_dialog()

    def _close_dialog( self ):
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        time.sleep( .4 )
        self.close()


def RESETPOPUP():
        #now   = datetime.datetime.today()
        #now= str(now)
        #resetnow = now - 30
        settings.setSetting('pop_time', '2000-01-02 00:00:00')
        return

        
#==============END POP UP FUNCTION===============



              
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
        
elif mode=='merdbmovies':
        print ""
        MERDBMOVIES()  
        

elif mode=='tvcats':
        print ""
        TVCATS()

elif mode=='cartooncats':
        print ""
        CARTOONCATS()

elif mode=='sportcats':
        print ""
        SPORTCATS()

elif mode=='adultcats':
        print ""
        ADULTCATS()        

elif mode=='merdbtvcats':
        print ""
        tvshow.MERDBTVCATS()        


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


        
elif mode=='mazindex':
        print ""
        MAZINDEX() 
        

        
elif mode=='playyear':
        print ""+url
        PLAYYEAR(url)


elif mode=='tvindex':
        print ""+url
        tvshow.TVINDEX(url)

        

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


elif mode=='tvvidpage':
        print ""+url
        tvshow.TVVIDPAGE(url,name)



elif mode=='linkpage':
        print ""+url
        LINKPAGE(url,name)

elif mode=='azlinkpage':
        print ""+url
        tvshow.AZLINKPAGE(url,name)        

elif mode=='tvlinkpage':
        print ""+url
        tvshow.TVLINKPAGE(url,name,thumb,mainimg)

elif mode=='episodes':
        print ""+url
        tvshow.EPISODES(url,name,thumb)
       

elif mode=='resolve':
        print ""+url
        main.RESOLVE(url,name,iconimage)


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

    

#==================END DL=====================================

# ===============Movie DC=====================================

elif mode=='moviedclinkpage':
        print ""+url
        moviedc.MOVIEDCLINKPAGE(url,name,thumb,mainimg)

elif mode=='moviedcindex':
        print ""+url
        moviedc.MOVIEDCINDEX(url)
        
elif mode=='moviedcindexsec':
        print ""+url
        moviedc.MOVIEDCINDEXSEC(url)
        
elif mode=='moviedccats':
        print ""
        moviedc.MOVIEDCCATS()        

elif mode=='searchmoviedc':
        print ""+url
        moviedc.SEARCHMOVIEDC(url)

elif mode=='moviedcsearch':
        print ""+url
        moviedc.MOVIEDCSEARCH(url)

#==================SGATE======================================

elif mode=='sgcats':
        print ""
        sgate.SGCATS()

elif mode=='sgindex':
        print ""+url
        sgate.SGINDEX(url)

elif mode=='sgepisodes':
        print ""+url
        sgate.SGEPISODES(url,name,thumb)

elif mode=='sgepisodelist':
        print ""+url
        sgate.SGEPISODELIST(url,name,thumb)

elif mode=='sgtvlinkpage':
        print ""+url
        sgate.SGTVLINKPAGE(url,name,thumb,mainimg)

elif mode=='sgsearchindex':
        print ""+url
        sgate.SGSEARCHINDEX(url)

elif mode=='searchsgtv':
        print ""+url
        sgate.SEARCHSGTV(url)

#====================POP UP STUFF=============================
elif mode=='pop':POP()
elif mode=='resetpopup':RESETPOPUP()
        
        
        
#==================Start Status/Help==========================

        
elif mode=='addonlist': print""+url; items=status.ADDONLIST(url)
elif mode=='searchaddon': print""+url; status.SEARCHADDON(url)
elif mode=='addonindex': print""+url; status.ADDONINDEX(name,url,filetype)        
elif mode == "statuscategories": print""+url; items=status.STATUSCATEGORIES(url)
elif mode == "addonstatus": print""+url; items=status.ADDONSTATUS(url)
elif mode=='getrepolink': print""+url; items=status.GETREPOLINK(url)
elif mode=='getshorts': print""+url; items=status.GETSHORTS(url)
elif mode=='getrepo': status.GETREPO(name,url,description,filetype)
elif mode=='getvideolink': print""+url; items=status.GETVIDEOLINK(url)
elif mode=='getvideo': status.GETVIDEO(name,url,iconimage,description,filetype)
elif mode=='addoninstall': status.ADDONINSTALL(name,url,description,filetype,repourl)
elif mode=='addshortcuts': status.ADDSHORTCUTS(name,url,description,filetype)
elif mode=='addsource': status.ADDSOURCE(name,url,description,filetype)
elif mode=='playstream': status.PLAYSTREAM(name,url,iconimage,description)

#=======================Cia Anime===========================
elif mode=='chiacats':
        print ""
        chia.CHIACATS()

elif mode=='chiaalph':
        print ""
        chia.CHIAALPH()

elif mode=='chiadlvidpage':
        print ""+url
        chia.CHIADLVIDPAGE(url,name)

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
        
elif mode=='chiaepisodes':
        print ""+url
        chia.CHIAEPISODES(url,name,year,thumb)

elif mode=='chiaresolve':
        print ""+url
        chia.CHIARESOLVE(url,name,iconimage)

elif mode=='searchanime':
        print ""+url
        chia.SEARCHANIME(url)

elif mode=='chiasearch':
        print ""+url
        chia.CHIASEARCH(url)

elif mode=='chiaresolvedl':
        print ""+url
        chia.CHIARESOLVEDL(url,name,thumb,favetype)

#================SHUTDOWN=================

elif mode=='shutdownxbmc':
        print ""+url
        SHUTDOWNXBMC()
#===========TEST FUNCTIONS================
elif mode=='testfunction':
        print ""+url
        TESTFUNCTION()

#==========ChannelCut UFC================

elif mode=='chanufcindex':
        print ""+url
        chanufc.CHANUFCINDEX(url)

elif mode=='chanufccats':
        print ""+url
        chanufc.CHANUFCCATS()

elif mode=='ufclinkpage':
        print ""+url
        chanufc.UFCLINKPAGE(url,name)

elif mode=='dlsportvidpage':
        print ""+url
        chanufc.DLSPORTVIDPAGE(url,name)

#==========Eporn=========================

elif mode=='epornikCategories':
        print ""+url
        epornik.CATEGORIES()

elif mode=='epornikIndex':
        print ""+url
        epornik.INDEX(url)

elif mode=='epornikSearch':
        print ""+url
        epornik.SEARCH()

elif mode=='pornresolve':
        print ""+url
        epornik.PORNRESOLVE(name,url,thumb)

#==========LIVE Streams================

elif mode=='chanufcindex':
        print ""+url
        live.CHANUFCINDEX(url)

elif mode=='livecats':
        print ""+url
        live.LIVECATS(url)

elif mode=='commonstreams':
        print ""+url
        live.COMMONSTREAMS(url)

elif mode=='usersub':
        print ""+url
        live.USERSUB(url)        

elif mode=='livecatslist':
        print ""+url
        live.LIVECATSLIST(url)        

elif mode=='ufclinkpage':
        print ""+url
        live.UFCLINKPAGE(url,name)

elif mode=='liveresolve':
        print ""+url
        live.LIVERESOLVE(name,url,thumb)        


#=============END LIVE STREAMS

#===============SUPERTOONS=================

elif mode=='supertoonscats':
        print ""+url
        supertoons.SUPERTOONSCATS()

elif mode=='supertoonsindex':
        print ""+url
        supertoons.SUPERTOONSINDEX(url)

elif mode=='supertoonsdeep':
        print ""+url
        supertoons.SUPERTOONSDEEP(url)

elif mode=='supertoonsdirect':
        print ""+url
        supertoons.SUPERTOONSDIRECT(url)        

elif mode=='supertoonsresolve':
        print ""+url
        supertoons.SUPERTOONSRESOLVE(name,url,thumb)         
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))


CHECK_POPUP()


