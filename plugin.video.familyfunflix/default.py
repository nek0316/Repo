import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc, xbmcaddon, os, sys
import urlresolver
from metahandler import metahandlers

from addon.common.addon import Addon

from addon.common.net import Net


net = Net()

from resources.modules import status
from resources.modules import dlthreadmod
from resources.modules import main
import threading

try:
     import StorageServer
except:
     import storageserverdummy as StorageServer
import time

# Global Stuff
addon_id = 'plugin.video.familyfunflix'
net = Net()

# Cache  
cache = StorageServer.StorageServer("familyfunflix", 0)
#=====================NEW DL======================================
settings = xbmcaddon.Addon(id='plugin.video.familyfunflix')     
addon = Addon('plugin.video.familyfunflix', argv=sys.argv)
mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
ext = addon.queries.get('ext', '')
console = addon.queries.get('console', '')
dlfoldername = addon.queries.get('dlfoldername', '')
favtype = addon.queries.get('favtype', '')
mainimg = addon.queries.get('mainimg', '')

print 'Mode is: ' + mode
print 'Url is: ' + url
print 'Name is: ' + name
print 'Thumb is: ' + thumb
print 'Extension is: ' + ext
print 'File Type is: ' + console
print 'DL Folder is: ' + dlfoldername
print 'Favtype is: ' + favtype
print 'Main Image is: ' + mainimg


download_path = settings.getSetting('download_folder')


#Family Fun Flix - Blazetamer.
addon = xbmcaddon.Addon ('plugin.video.familyfunflix')
URL= 'http://familyfunflix.com'

addonPath = addon.getAddonInfo('path')
artPath = xbmc.translatePath(os.path.join('http://addonrepo.com/xbmchub/familyfunflix/images/', ''))
fanartPath = xbmc.translatePath(os.path.join('http://addonrepo.com/xbmchub/familyfunflix/images/fanart/', ''))


#HOOKS
settings = xbmcaddon.Addon(id='plugin.video.familyfunflix')






def CATEGORIES():
    
    main.addDir('[COLOR white]New Arrivals[/COLOR]','http://www.familyfunflix.com/New-Arrivals-movies','index',artPath+'newarrival.png','','movies')
    main.addDir('[COLOR white]Most Popular[/COLOR]','http://www.familyfunflix.com/most-popular-movies','index',artPath+'mostpopular.png','','movies')
    main.addDir('[COLOR white]Pop Kids[/COLOR]','http://www.familyfunflix.com/Pop Kids-movies','indexdeep',artPath+'popkids.png','','movies')
    main.addDir('[COLOR white]Pop Junior[/COLOR]','http://www.familyfunflix.com/Pop Junior-movies','indexdeep',artPath+'popkids.png','','movies')
    main.addDir('[COLOR white]Teen Zone[/COLOR]','http://www.familyfunflix.com/Teen Zone-movies','indexdeep',artPath+'teenzone.png','','movies')
    main.addDir('[COLOR white]Family Fun Movies[/COLOR]','http://www.familyfunflix.com/Fun For the Family-movies','indexdeep',artPath+'fun.png','','movies')
    main.addDir('[COLOR white]Wild Kingdom[/COLOR]','http://www.familyfunflix.com/Wild Kingdom-movies','indexdeep',artPath+'wildkingdom.png','','movies')
    main.addDir('[COLOR white]Fairy Tales[/COLOR]','http://www.familyfunflix.com/Fairy Tales-movies','indexdeep',artPath+'fairytales.png','','movies')
    main.addDir('[COLOR white]Cartoons[/COLOR]','http://www.familyfunflix.com/Cartoons-movies','indexdeep',artPath+'animated.png','','movies')
    main.addDir('[COLOR white]Musical[/COLOR]','http://www.familyfunflix.com/Musicals-movies','indexdeep',artPath+'musical.png','','movies')
    main.addDir('[COLOR white]Girl Power[/COLOR]','http://www.familyfunflix.com/Girl Power-movies','indexdeep',artPath+'girlpower.png','','movies')
    main.addDir('[COLOR white]Boys Rock[/COLOR]','http://www.familyfunflix.com/Boys Rock-movies','indexdeep',artPath+'boysrock.png','','movies')
    main.addDir('[COLOR red][B]Search[/B] >>>[/COLOR]','http://www.familyfunflix.com/search?query=','searchit',artPath+'search.png','','')
    main.addDir('[COLOR gold]Manage Downloads[/COLOR]','none','viewQueue',artPath +'downloads.png','','')
    main.addDir('[COLOR white]Help and Extras[/COLOR]','none','statuscats',artPath +'help.png','','')
    main.AUTO_VIEW('')
        
def INDEX(url,favtype):
          params = {'url':url, 'favtype':favtype}
          link = net.http_GET(url).content
          match=re.compile('<a href="(.+?)">\n\t\t  <img width="184" height="256" src="(.+?)" alt="(.+?)"/>').findall(link)
          for url,thumb,name in match:
               url = URL + url
               if settings.getSetting('metadata') == 'true':
                    data = main.GRABMETA(name,year)
                    thumb = data['cover_url'] 
                    #addDir(name,url,'videolinks',thumb)
                    main.addDir(name,url,'videolinks',thumb,data,favtype)
                    main.AUTO_VIEW('movies')
               else:
                    main.addDir(name,url,'videolinks',thumb,'',favtype)
                    main.AUTO_VIEW('movies')
                    

                
def VIDEOLINKS(name,url,thumb,favtype):
        params = {'url':url, 'name':name, 'thumb':thumb, 'favtype':favtype}  
        link = net.http_GET(url).content
        match=re.compile('id="flashContent" data-videosrc="(.+?)" data-videodata="(.+?)"></div>').findall(link)
        matchyear=re.compile('<span class="year">(.+?)</span>').findall(link)
        for url,url2 in match:
                     url = url2
                     for year in matchyear:
                       link = net.http_GET(url).content
                       url = URL + url
                       match4=re.compile('"poster":"(.+?)","slider":".+?","duration":.+?,"rating":"(.+?)","language":".+?","cuepoints":".+?","urls":{".+?":"(.+?)"}').findall(link)
                       for thumb,rating,url in match4:
                              #replace odd strings
                              thumb = thumb.replace("\/","/")
                              url = url.replace("\/","/")
                              mainimg = thumb
                              
                              link = net.http_GET(url).content
                              match3=re.compile('RESOLUTION=864x480\r\n(.+?)\r\n#').findall(link)
                              for url in match3:
                                   print 'Thumb is' +thumb
                                   print 'Playurl is' +url
                                   print 'Name is' +name
                                   #addLink(name,url,thumb)
                                   #addlinkDir(name + year,url,'addlink',thumb)
                                   main.addDLDir(name + year + ' Rated- ' +rating,url,'addlink',thumb,'',name + year,favtype,mainimg)
                                   main.AUTO_VIEW('movies')

            
           
                     



                     
def _SaveFile(path,data):
	file=open(path,'w')
	file.write(data)
	file.close()
             
def OPEN_URL(url):
  req=urllib2.Request(url)
  req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  response=urllib2.urlopen(req)
  link=response.read()
  response.close()
  return link



def INDEX_DEEP(url,favtype):
        params = {'url':url,'favtype':favtype}  
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)"><img width="184" height="256" src="(.+?)" alt="(.+?)"></a>').findall(link)
        for url,thumb,name in match:
               url = URL + url
               if settings.getSetting('metadata') == 'true':
                    data = main.GRABMETA(name,year)
                    thumb = data['cover_url'] 
                    #addDir(name,url,'videolinks',thumb)
                    main.addDir(name,url,'videolinks',thumb,data,favtype)
                    #addDir(name,url,'videolinks',thumb)
                    main.AUTO_VIEW('movies')
               else:
                    main.addDir(name,url,'videolinks',thumb,'',favtype)
                    main.AUTO_VIEW('movies')

	
#Start Ketboard Function                
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default


#Start Search Function
def SEARCH(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching  FamilyFunFlix" )
	# if blank or the user cancelled the keyboard, return
	if ( not vq ): return False, 0
	# we need to set the title to our query
	title = urllib.quote_plus(vq)
	searchUrl += title 
	print "Searching URL: " + searchUrl 
	INDEX,INDEX_DEEP(searchUrl,'')
        

                
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

def addLink(name,url,thumb):
         #params = {'url':url, 'name':name, 'thumb':thumb}      
         url= url
         ok=True
         liz=xbmcgui.ListItem(name, iconImage=thumb,thumbnailImage=thumb); liz.setInfo( type="Video", infoLabels={ "Title": name } )
         ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
         xbmc.executebuiltin("XBMC.Notification(Building Video File!,Please Wait,3000)")
         xbmc.sleep(1000)
         xbmc.Player ().play(url, liz, False)

         
             

def addDir(name,url,mode,thumb):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


def addlinkDir(name,url,mode,thumb):
     u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(thumb)
     liz = xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
     liz.setProperty("IsPlayable","true")
     xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = False)

     
              
params=get_params()
url=None
name=None
mode=None
year=None
imdb_id=None

#------added for Help Section
try:        
        favtype=urllib.unquote_plus(params["favtype"])
except:
        pass

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
        CATEGORIES()
       
elif mode=='index':
        print ""+url
        INDEX(url,favtype)
        

elif mode=='videolinks':
        print ""+url
        VIDEOLINKS(name,url,thumb,favtype)

elif mode=='addlink':
        print ""+url
        addLink(name,url,thumb)                                   


elif mode=='indexdeep':
        print ""+url
        INDEX_DEEP(url,favtype)
       
#For Search Function
elif mode=='searchit':
        print ""+url
        SEARCH(url)
#****************DL FUNCTIONS******************
if mode=='viewQueue':
        print ""+url
        dlthreadmod.viewQueue()

elif mode=='download':
        print ""+url
        dlthreadmod.download()

elif mode=='removeFromQueue':
        print ""+url
        dlthreadmod.removeFromQueue(name,url,thumb,ext,console)

elif mode=='killsleep':
        print ""+url
        dlthreadmod.KILLSLEEP()

elif mode=='resolvedl':
        print ""+url
        dlthreadmod.RESOLVEDL(url,name,thumb,favtype)
        
elif mode=='resolvetvdl':
        print ""+url
        dlthreadmod.RESOLVETVDL(url,name,thumb)

elif mode=='resolve2':
        print ""+url
        main.RESOLVE2(name,url,thumb)

elif mode=='resolve':
        print ""+url
        main.RESOLVE(name,url,thumb)        

elif mode=='directresolvedl':
        print ""+url
        dlthreadmod.DIRECTRESOLVEDL(name,url,thumb,favtype)


#==================Start Status/Help==========================
        
elif mode == "statuscats": print""; items=status.STATUSCATS()
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


