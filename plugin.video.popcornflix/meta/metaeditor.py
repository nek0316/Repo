'''
Created on 6 feb 2012

@author: Batch
'''
import os
from common import create_directory, write_to_file, read_from_file
from meta import TMDBInfo, TheTVDBInfo, TheTVDBEpisode
import urllib


def set_movie_meta(listitem, imdb_id, path):
    (data_file, poster_file, fanart_file, poster_missing, fanart_missing) = _get_meta_paths(imdb_id, path)
    if os.path.isfile(data_file):
        try:
            content = read_from_file(data_file)
            data = content.split('\n')
            title = data[0]
            year = data[1]
            genre = data[2]
            tagline = data[3]
            overview = data[4]
            duration = data[5]
            rating = data[6]
            votes = data[7]
            premiered = data[8]
            mpaa = data[9]

            listitem.setProperty("Video", "true")
            listitem.setProperty("IsPlayable", "true")
            listitem.setInfo(type='Video', infoLabels={'title': title,
                               'year': int(year),
                               'genre': genre,
                               'tagline': tagline,
                               'plot': overview,
                               'duration': duration,
                               'rating': float(rating),
                               'votes': votes,
                               'premiered': premiered,
                               'mpaa': mpaa,
                               'code': imdb_id})
        except:
            pass
            #print "Couldn't add meta for %s" % (imdb_id)
            
    if os.path.isfile(poster_file) and USE_POSTERS:
        listitem.setThumbnailImage(poster_file)
    if os.path.isfile(fanart_file) and USE_FANART:
        listitem.setProperty('fanart_image', fanart_file)
        
    return listitem
    
def meta_exist(imdb_id, path):
    (data_file, poster_file, fanart_file, poster_missing, fanart_missing) = _get_meta_paths(imdb_id, path)
    
    if not os.path.isfile(data_file):
        return False
    if not os.path.isfile(poster_file) and not os.path.isfile(poster_missing):
        return False
    if not os.path.isfile(fanart_file) and not os.path.isfile(fanart_missing):
        return False

    return True
    
def _get_meta_paths(imdb_id, path):
    data_file = os.path.join(path, "%s.dat" % (imdb_id))
    poster_path = create_directory(path, META_QUALITY)
    fanart_path = create_directory(path, META_QUALITY)
    poster_file = os.path.join(poster_path, "%s_poster.jpg" % (imdb_id))
    fanart_file = os.path.join(fanart_path, "%s_fanart.jpg" % (imdb_id))
    poster_missing = os.path.join(poster_path, "%s_poster.missing" % (imdb_id))
    fanart_missing = os.path.join(fanart_path, "%s_fanart.missing" % (imdb_id))
    return (data_file, poster_file, fanart_file, poster_missing, fanart_missing)

def download_movie_meta(imdb_id, path):
    (data_file, poster_file, fanart_file, poster_missing, fanart_missing) = _get_meta_paths(imdb_id, path)
    if not os.path.isfile(data_file) or not os.path.isfile(poster_file) or not os.path.isfile(fanart_file):
            info = TMDBInfo(imdb_id=imdb_id)
            title = info.name()
            try:
                year = info.released().split('-')[0]
            except:
                year = ""
            
            genre = ""
            try:
                for category in info.categories():
                    genre += category + ","
                genre = genre[:-1]
            except:
                genre = ""
    
            tagline = info.tagline()
            overview = info.overview()
    
            try:
                duration = int(info.runtime())#"%d:%02d" % (int(info.runtime()) / 60, int(info.runtime()) % 60)
            except:
                duration = ""
            
            rating = info.rating()
            votes = info.votes()
            premiered = info.released()
            mpaa = info.certification()
    
            content = '%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s' % (title, year, genre, tagline, overview, duration, rating, votes, premiered, mpaa)
            write_to_file(data_file, content)
            
            poster_url = info.poster()
            
            if not os.path.isfile(poster_file) or not os.path.isfile(poster_missing):
                if USE_POSTERS:
                    try:
                        urllib.urlretrieve(poster_url, poster_file)
                    except:
                        write_to_file(poster_missing, '')

            
            fanart_url = info.fanart()
            
            if not os.path.isfile(fanart_file) or not os.path.isfile(fanart_missing):
                if USE_FANART:
                    try:
                        urllib.urlretrieve(fanart_url, fanart_file)
                    except:
                        write_to_file(fanart_missing, '')

def set_tv_show_meta(listitem, imdb_id, path):
    (data_file, poster_file, fanart_file, poster_missing, fanart_missing) = _get_meta_paths(imdb_id, path)
    if os.path.isfile(data_file):
        try:
            content = read_from_file(data_file)
            data = content.split('\n')
            title = data[0]
            year = data[1]
            genre = data[2]
            overview = data[3]
            rating = data[4]
            votes = data[5]
            premiered = data[6]
            mpaa = data[7]  

            listitem.setProperty("Video", "true")
            listitem.setProperty("IsPlayable", "true")
            listitem.setInfo(type='Video', infoLabels={'title': title,
                               'year': int(year),
                               'genre': genre,
                               'plot': overview,
                               'rating': float(rating),
                               'votes': votes,
                               'premiered': premiered,
                               'mpaa': mpaa,
                               'code': imdb_id})
        except:
            pass
        
    if os.path.isfile(poster_file) and USE_POSTERS:
        listitem.setThumbnailImage(poster_file)
    if os.path.isfile(fanart_file) and USE_FANART:
        listitem.setProperty('fanart_image', fanart_file)
    
    return listitem

def download_tv_show_meta(imdb_id, path):
    (data_file, poster_file, fanart_file, poster_missing, fanart_missing) = _get_meta_paths(imdb_id, path)
    if not os.path.isfile(data_file) or not os.path.isfile(poster_file) or not os.path.isfile(fanart_file):
            info = TheTVDBInfo(imdb_id)
            title = info.SeriesName()
            year = info.FirstAired().split('-')[0]
            genre = info.Genre()
            overview = info.Overview()
            rating = info.Rating()
            votes = info.RatingCount()
            premiered = info.FirstAired()
            mpaa = info.ContentRating()
    
            content = '%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s' % (title, year, genre, overview, rating, votes, premiered, mpaa)
            write_to_file(data_file, content)
            
            if not os.path.isfile(poster_file) or not os.path.isfile(poster_missing):
                if USE_POSTERS:
                    if META_QUALITY == 'low':
                        image_base_url = 'http://thetvdb.com/banners/_cache/'
                    else:
                        image_base_url = 'http://thetvdb.com/banners/'
                    poster_href = info.poster()
                    if len(poster_href) > 0:
                        poster = '%s%s' % (image_base_url, poster_href)
                        try:
                            urllib.urlretrieve(poster, poster_file)
                        except:
                            pass    
                    else:
                        write_to_file(poster_missing, '')
            
            if not os.path.isfile(fanart_file) or not os.path.isfile(fanart_missing):
                if USE_FANART:
                    if META_QUALITY == 'low':
                        image_base_url = 'http://thetvdb.com/banners/_cache/'
                    else:
                        image_base_url = 'http://thetvdb.com/banners/'
                    fanart_href = info.fanart()
                    if len(fanart_href) > 0:
                        fanart = '%s%s' % (image_base_url, fanart_href)
                        try:
                            urllib.urlretrieve(fanart, fanart_file)
                        except:
                            pass
                    else:
                        write_to_file(fanart_missing, '')
						
