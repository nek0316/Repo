# Status/Help Module By: Blazetamer 2013
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,sys,time,shutil
import downloader
import extract
from resources.modules import main
addon_id='plugin.video.twomovies'
from t0mm0.common.addon import Addon
addon=main.addon
from t0mm0.common.net import Net
net=Net()
settings=xbmcaddon.Addon(id='plugin.video.twomovies')

#==========================ADDON REPO=====================================================================================================
def STATUSCATEGORIES(url):
          link=OPEN_URL(url).replace('\n','').replace('\r','')
          match=re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ype="(.+?)"').findall(link)
          for name,url,iconimage,fanart,description,filetype in match:
              if 'status' in filetype:
                 main.addHELPDir(name,url,'addonstatus',iconimage,fanart,description,filetype)
              elif 'shortcuts' in filetype:
                 main.addHELPDir(name,url,'addshortcuts',iconimage,fanart,description,filetype) 
              elif 'main' in filetype:
                    main.addHELPDir(name,url,'addoninstall',iconimage,fanart,description,filetype)
              elif 'addon' in filetype:
                    main.addHELPDir(name,url,'addoninstall',iconimage,fanart,description,filetype)
              elif 'source' in filetype:
                    main.addHELPDir(name,url,'addsource',iconimage,fanart,description,filetype)      
                    main.AUTO_VIEW('movies')

def OPEN_URL(url):
  req=urllib2.Request(url)
  req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  response=urllib2.urlopen(req)
  link=response.read()
  response.close()
  return link

def ADDONINSTALL(name,url,description,filetype):
  path=xbmc.translatePath(os.path.join('special://home/addons','packages'))
  confirm=xbmcgui.Dialog().yesno("ATTENTION!!","                By Clicking 'YES' you agree to allow this Addon","                 Access to add repositories and other addons              ","                    ")
  
  if confirm: 
        dp=xbmcgui.DialogProgress()
        dp.create("ATTENTION:","Downloading ",'','Please Wait')
        lib=os.path.join(path,name+'.zip')
        try: os.remove(lib)
        except: pass
        downloader.download(url, lib, dp)
        if filetype == 'addon':
            addonfolder = xbmc.translatePath(os.path.join('special://','home/addons'))
        elif filetype == 'media':
             addonfolder = xbmc.translatePath(os.path.join('special://','home'))    
  ##attempt Shortcuts
        elif filetype == 'main':
             addonfolder = xbmc.translatePath(os.path.join('special://','home'))
        time.sleep(2)
        dp.update(0,"","Extracting Zip Please Wait")
        print '======================================='
        print addonfolder
        print '======================================='
        extract.all(lib,addonfolder,dp)
        dialog=xbmcgui.Dialog()
        dialog.ok("Success!","Please Reboot To Take Effect","   [COLOR gold]Brought To You By BLAZETAMER[/COLOR]")
  else:
      return
def ADDSHORTCUTS(name,url,description,filetype):
   confirm=xbmcgui.Dialog()
   if confirm.yesno("Shortcut Creation!!","                By Clicking 'YES' you agree to allow this Addon","                 Access to add Shortcuts to your pages.              ","                    "):

    link=OPEN_URL(url)
    proname=xbmc.getInfoLabel("System.ProfileName")
    shorts=re.compile('shortcut="(.+?)"').findall(link)
    for shortname in shorts: xbmc.executebuiltin("Skin.SetString(%s)" % shortname)
    time.sleep(2)
    xbmc.executebuiltin('UnloadSkin()')
    xbmc.executebuiltin('ReloadSkin()')
    xbmc.executebuiltin("LoadProfile(%s)" % proname)
    dialog=xbmcgui.Dialog()
    dialog.ok("Success!","Please Reboot To Take","Effect   [COLOR gold]Brought To You By BLAZETAMER[/COLOR]")

def ADDSOURCE(name,url,description,filetype):
   confirm=xbmcgui.Dialog()
   if confirm.yesno("Source Creation!!","                By Clicking 'YES' you agree to allow this Addon","                 Access to add Sources to your settings.              ","                    "):
       link=OPEN_URL(url)
       source=re.compile("source='(.+?)'").findall(link)
       for sourcename in source:
        newfile=re.compile("addfile='(.+?)'").findall(link)    
        for addfile in newfile:     
         newsource = os . path . join ( xbmc . translatePath ( 'special://home' ) , 'userdata' , 'sources.xml' )
         if not os . path . exists ( newsource ) :
          src = open ( newsource , mode = 'w' )
          src . write ( addfile )
          src . close ( )
          dialog=xbmcgui.Dialog()
          dialog.ok("Success!","Please Reboot To Take","Effect   [COLOR gold]Brought To You By BLAZETAMER[/COLOR]")
          return
       src = open ( newsource , mode = 'r' )
       str = src . read ( )
       src . close ( )
       #if not 'http://fusion.xbmchub.com' in str:
        #if '</files>' in str :
       str = str . replace ( '</files>' , sourcename )
       src = open ( newsource , mode = 'w' )
       src . write ( str )
       src . close ( )
    
       dialog=xbmcgui.Dialog()
       dialog.ok("Success!","Please Reboot To Take","Effect   [COLOR gold]Brought To You By BLAZETAMER[/COLOR]")

def ADDONSTATUS(url):
  link=OPEN_URL(url).replace('\n','').replace('\r','')
  match=re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ype="(.+?)"').findall(link)
  for name,url,iconimage,fanart,description,filetype in match:
    header="[B][COLOR gold]"+name+"[/B][/COLOR]"
    msg=(description)
    TextBoxes(header,msg)

def TextBoxes(heading,anounce):
  class TextBox():
    WINDOW=10147
    CONTROL_LABEL=1
    CONTROL_TEXTBOX=5
    def __init__(self,*args,**kwargs):
      xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
      self.win=xbmcgui.Window(self.WINDOW) # get window
      xbmc.sleep(500) # give window time to initialize
      self.setControls()
    def setControls(self):
      self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
      try: f=open(anounce); text=f.read()
      except: text=anounce
      self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
      return
  TextBox()

