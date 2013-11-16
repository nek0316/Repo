# Login Module by : Blazetamer


"""
  USAGE:
 in your default.py put:

 import weblogin
 logged_in = weblogin.doLogin('a-path-to-save-the-cookie-to','the-username','the-password')

 logged_in will then be either True or False depending on whether the login was successful.
"""
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc, xbmcaddon, os, sys

import cookielib
settings = xbmcaddon.Addon(id='plugin.video.twomovies')
### TESTING SETTINGS (will only be used when running this file independent of your addon)
# Remember to clear these after you are finished testing,
# These are only used in the:  if __name__ == "__main__"   thing at the bottom of this script.
#username = settings.getSetting('tmovies_user')
#password = settings.getSetting('tmovies_pass')

#note, the cookie will be saved to the same directory as weblogin.py when testing


def check_login(source,username):
    
    #the string you will use to check if the login is successful.
    #you may want to set it to:    username     (no quotes)
    logged_in_string = username

    #search for the string in the html, without caring about upper or lower case
    if re.search(logged_in_string,source,re.IGNORECASE):
        return True
    else:
        return False


def doLogin(cookiepath,username,password):

    #check if user has supplied only a folder path, or a full path
    if not os.path.isfile(cookiepath):
        #if the user supplied only a folder path, append on to the end of the path a filename.
        cookiepath = os.path.join(cookiepath,'cookies.lwp')
        
    #delete any old version of the cookie file
    try:
        os.remove(cookiepath)
    except:
        pass

    if username and password:

        #the url you will request to.
        login_url = 'http://twomovies.name/go_login'

        #the header used to pretend you are a browser
        header_string = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'

	#build the form data necessary for the login
        login_data = urllib.urlencode({'user':username, 'pass':password,'submit_login':'Login', 'submit_login':''})

        #build the request we will make
        req = urllib2.Request(login_url, login_data)
        req.add_header('User-Agent',header_string)

        #initiate the cookielib class
        cj = cookielib.LWPCookieJar()

        #install cookielib into the url opener, so that cookies are handled
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

        #do the login and get the response
        response = opener.open(req)
        source = response.read()
        response.close()

        #check the received html for a string that will tell us if the user is logged in
        #pass the username, which can be used to do this.
        login = check_login(source,username)

        #if login suceeded, save the cookiejar to disk
        if login == True:
            cj.save(cookiepath)

        #return whether we are logged in or not
        return login
    
    else:
        return False

#code to enable running the .py independent of addon for testing
if __name__ == "__main__":
    if username is '' or password is '':
        print 'YOU HAVE NOT SET THE USERNAME OR PASSWORD!'
    else:
        logged_in = doLogin(os.getcwd(),username,password)
        print 'LOGGED IN:',logged_in
