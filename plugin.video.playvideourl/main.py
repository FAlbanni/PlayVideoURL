import sys
import xbmcgui
import xbmcplugin
import xbmcaddon
from urlparse import parse_qsl
import urllib2

_handle = int(sys.argv[1])
storedPastebinurl = xbmcaddon.Addon().getSetting('pastebinurl')
dialog = xbmcgui.Dialog()

def storedPastebinurlRetrieve():
    storedPastebinurl = xbmcaddon.Addon().getSetting('pastebinurl')
    return storedPastebinurl

def parse_links():
    if storedPastebinurlRetrieve() is '':
        pastebinurl = dialog.input('Enter Pastebin raw address', defaultt='https://pastebin.com/raw/', type=xbmcgui.INPUT_ALPHANUM)
        xbmcaddon.Addon().setSetting(id='pastebinurl', value=pastebinurl)
    else:
        pastebinurl = dialog.input('Enter Pastebin raw address', defaultt=storedPastebinurlRetrieve(), type=xbmcgui.INPUT_ALPHANUM)
        xbmcaddon.Addon().setSetting(id='pastebinurl', value=pastebinurl)

    linksource = storedPastebinurlRetrieve()

    if 'pastebin' in linksource:
        source = urllib2.urlopen(linksource).read()
        links = source.split('\n')
        for link in links:
            if link.startswith('http'):
                continue
            else:
                return 0
        return links
    else:
        dialog.ok('PlayVideoURL', 'You must enter a valid pastebin address.')
        sys.exit()


def list_videos():
    videos = parse_links()
    if isinstance(videos, int):
        dialog.ok('PlayVideoURL', 'URLs are bad formatted, they must start with http or https, check your pastebin.')
        sys.exit()
    xbmcplugin.setContent(_handle, 'videos')
    listing = []
    for video in videos:
        list_item = xbmcgui.ListItem(label=video.split('/')[-1])
        list_item.setInfo('video', {'title': video.split('/')[-1],'mediatype':'video'})
        list_item.setProperty('IsPlayable', 'true')
        url = '{0}?action=play&video={1}'.format(sys.argv[0], video)
        listing.append((url, list_item, False))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def play_video(vidurl):
    xbmcplugin.setResolvedUrl(_handle, True, listitem=xbmcgui.ListItem(path=vidurl.rstrip()))


def router(paramstring):
    params = dict(parse_qsl(paramstring[1:]))
    if params:
        if params['action'] == 'play':
            play_video(params['video'])
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        list_videos()


if __name__ == '__main__':
    router(sys.argv[2])
