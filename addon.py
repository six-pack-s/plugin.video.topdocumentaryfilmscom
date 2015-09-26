import urllib, urllib2, sys, re, urlparse, re, xbmcplugin, xbmcgui, xbmcaddon, datetime, os, math

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
addon = xbmcaddon.Addon(id='plugin.video.topdocumentaryfilmscom')
xbmcplugin.setContent(addon_handle, 'movies')
mode = args.get('mode', None)
setting = xbmcaddon.Addon().getSetting


# styles menu item words
def style(w, c, b, i):
    retval = ''
    color = ''
    bold = ''
    italic = ''
    if i == 'true':
        i = 1
    else:
        i = 0
    if b == 'true':
        b = 1
    else:
        b = 0
    if len(w) < 1: return retval
    if len(c) > 0: color = '[COLOR ' + c.lower() + ']'
    if b > 0: bold = '[B]'
    if i > 0: italic = '[I]'
    retval = color + bold + italic + w
    if i > 0: retval = retval + '[/I]'
    if b > 0: retval = retval + '[/B]'
    if len(c) > 0: retval = retval + '[/COLOR]'
    return retval


# Standard Movie Menu Item Look
def buildMovieItem(name, rating, desc):
    retval = ''
    mlc = setting('movie_list_color')
    mlb = setting('movie_list_bold')
    mli = setting('movie_list_italic')
    retval = style(name, mlc, mlb, mli)

    slc = setting('show_rating')
    if slc == 'true': retval = retval + getStarRating(rating, 0)

    sdc = setting('show_description')
    if sdc == 'true': retval = retval + getMovieDesc(desc[0:100])

    return retval


# returns formatted star rating
def getStarRating(star, full):
    rlc = setting('rating_list_color')
    rlb = setting('rating_list_bold')
    rli = setting('rating_list_italic')
    x = math.ceil(float(star))
    y = 0
    star_rating = ""
    if full == 1:
        while y < x:
            star_rating = star_rating + " *"
            y = y + 1
    rating = str(int(x)) + " " + star_rating
    return style('  -  ', rlc, rlb, rli) + style(rating, rlc, rlb, rli) + style('  -  ', rlc, rlb, rli)

def getMovieDesc(desc):
    dlc = setting('desc_list_color')
    dlb = setting('desc_list_bold')
    dli = setting('desc_list_italic')
    return style(desc + "...", dlc, dlb, dli)

def getPager():
    pt = setting('pager_text')
    pc = setting('pager_color')
    pb = setting('pager_bold')
    pi = setting('pager_italic')
    return style(pt,pc,pb,pi)

def sanitize(str):
    str.replace('&#039;', '')
    str = re.sub('<[^>]*>', '', str)
    return str


# returns star and description for movie
def getDetails(url, full):
    retval = []
    # try:
    html = OpenURL('http://topdocumentaryfilms.com/' + url)
    rating = re.compile('<div class="star">(.+?)</div>', re.DOTALL).findall(html.replace("amp;", ''))[0]

    if len(rating) < 1:
        retval.append(" ")
    else:
        retval.append(rating)

    contents = re.compile('<div class=".+?contentpic">(.+?)</div>', re.DOTALL).findall(html.replace('amp;', ''))
    for content in contents:

        imgs = re.compile('http://cdn.topdocumentaryfilms.com/wp-content/uploads/(.+?)"', re.DOTALL).findall(
            content.replace('amp;', ''))
        for i in imgs:
            img = "http://cdn.topdocumentaryfilms.com/wp-content/uploads/" + i

        desc = re.compile('<p>(.+?)</p>', re.DOTALL).findall(content.replace('amp;', ''))[0]
        desc = re.sub('<[^>]*>', '', desc)
        words = desc.split()
        sentence = ''
        for word in words:
            sentence = sentence + " " + word
            if len(sentence) > 100:
                break

        if len(sentence) < 1:
            retval.append(" ")
        else:
            retval.append(sentence)
    return retval
    # except:
    #   print "Unexpected error:", sys.exc_info()[0]
    #   return " "


# Addds Menu Item to the List
def AddToMenu(name, url, mode, iconimage, description, subtitles_url, movie_url):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(
        name) + "&iconimage=" + urllib.quote_plus(iconimage) + "&description=" + urllib.quote_plus(
        description) + "&subtitles_url=" + urllib.quote_plus(subtitles_url) + "&movie_url=" + urllib.quote_plus(
        movie_url)

    liz = xbmcgui.ListItem(label=name, label2=description, iconImage="DefaultFolder.png", thumbnailImage=iconimage)

    date_string = "09.22.2015"
    liz.setInfo("video",
                infoLabels={"title": name, "plot": description, "plotoutline": description, "date": date_string})
    if mode == 3:
        liz.setProperty("IsPlayable", "true")
        liz.setProperty("IsFolder", "false")
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    else:
        liz.setProperty("IsPlayable", "false")
        liz.setProperty("IsFolder", "true")
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)

    liz.setProperty("Property(Addon.Name)", "Top Documentary Films")
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    return True


# Sends URL Request to website for return
def OpenURL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:38.0) Gecko/20100101 Firefox/38.0')
    response = urllib2.urlopen(req)
    html = response.read()
    response.close()
    return html


# Plays the video
def PlayVideo(name, url, iconimage, description, subtitles_url):
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title': name})
    liz.setProperty("IsPlayable", "true")
    liz.setPath(url)
    if subtitles_url and ADDON.getSetting('subtitles') == 'true':
        subtitles_file = download_subtitles(subtitles_url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    if subtitles_url and ADDON.getSetting('subtitles') == 'true':
        # Successfully started playing something?
        while 1:
            if xbmc.Player().isPlaying():
                break;
            else:
                xbmc.sleep(500)
        xbmc.Player().setSubtitles(subtitles_file)


def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            return
        except:
            pass


# Home - Add-on Start
def TopLevelCategories():
    mlc = setting('main_list_color')
    mlb = setting('main_list_bold')
    mli = setting('main_list_italic')
    msf = setting('main_show_featured')
    AddToMenu(style('Documentary Categories', mlc, mlb, mli), 'url', 9, addon.getAddonInfo('icon'), '', '', movie_url)
    AddToMenu(style('Recently Added', mlc, mlb, mli), 'url', 5, addon.getAddonInfo('icon'), '', '', movie_url)
    AddToMenu(style('Highest Rated', mlc, mlb, mli), 'url', 8, addon.getAddonInfo('icon'), '', '', movie_url)
    AddToMenu(style('Most Shared', mlc, mlb, mli), 'url', 7, addon.getAddonInfo('icon'), '', '', movie_url)
    AddToMenu(style('Most Voted', mlc, mlb, mli), 'url', 6, addon.getAddonInfo('icon'), '', '', movie_url)
    AddToMenu(style('By Year', mlc, mlb, mli), 'url', 10, addon.getAddonInfo('icon'), '', '', movie_url)
    AddToMenu(style('Search', mlc, mlb, mli), 'url', 12, addon.getAddonInfo('icon'), '', '', movie_url)

    if msf == 'true':
        AddToMenu(style('  ---        ', 'green', 0, 0) +
                  style('---        ', 'red', 0, 0) +
                  style('---        ', 'yellow', 0, 0) +
                  style('         FEATURED         ', 'red', 1, 0) +
                  style('        ---', 'yellow', 0, 0) +
                  style('        ---', 'red', 0, 0) +
                  style('        ---  ', 'green', 0, 0),
                  'url', 0, addon.getAddonInfo('icon'), '', '', movie_url)

        html = OpenURL('http://topdocumentaryfilms.com/')
        main = re.compile('<main role="main" class="grid-2-3">(.+?)</main>', re.DOTALL).findall(
            html.replace('amp;', ''))
        for m in main:
            gallery = re.compile('<div class="module clear galery">(.+?)</div>', re.DOTALL).findall(
                m.replace('amp;', ''))
            for modules in gallery:
                url = ''
                name = ''
                gall = re.compile('\n\n(.+?)\n', re.DOTALL).findall(modules.replace('amp;', ''))
                for module in gall:

                    img = "http://cdn.topdocumentaryfilms.com/wp-content/uploads/" + \
                          re.compile('http://cdn.topdocumentaryfilms.com/wp-content/uploads/(.+?)"', re.DOTALL).findall(
                              module.replace('amp;', ''))[0]

                    info = re.compile(
                        '<a href="http://topdocumentaryfilms.com/(.+?)/" title="(.+?)">', re.DOTALL).findall(
                        module.replace('amp;', ''))
                    for u, n in info:
                        url = u
                        name = n.replace('&#039;', '')

                    page_data = getDetails(url, 0)
                    try:
                        AddToMenu(buildMovieItem(name, page_data[0], page_data[1].replace('&#039;', '')), url, 2, img,
                                  '',
                                  '', movie_url)
                    except:
                        AddToMenu(name.replace('&#039;', ''), url, 2, img, '', '', movie_url)

            articles = re.compile('<article class="module">(.+?)</article>', re.DOTALL).findall(
                m.replace('amp;', ''))

            for article in articles:
                url = ''
                name = ''
                img = "http://cdn.topdocumentaryfilms.com/wp-content/uploads/" + \
                      re.compile('http://cdn.topdocumentaryfilms.com/wp-content/uploads/(.+?)"', re.DOTALL).findall(
                          module.replace('amp;', ''))[0]

                info = re.compile('<h2><a href="http://topdocumentaryfilms.com/(.+?)/" title="(.+?)">.+?</a></h2>',
                                  re.DOTALL).findall(article.replace('amp;', ''))

                for u, n in info:
                    url = u
                    name = n.replace('&#039;', '')
                if len(url) > 0 and len(name) > 0:
                    page_data = getDetails(url, 0)
                    try:
                        AddToMenu(buildMovieItem(name, page_data[0], page_data[1].replace('&#039;', '')), url
                                  , 2, img, '', '', movie_url)
                    except:
                        AddToMenu(name.replace('&#039;', ''), url, 2, img, '', '', movie_url)


# By Year menu click
def TopLevelYears():
    dlc = setting('drill_list_color')
    dlb = setting('drill_list_bold')
    dli = setting('drill_list_italic')
    x = datetime.datetime.now().year
    while x > 1993:
        AddToMenu(style(str(x), dlc, dlb, dli), str(x), 11, addon.getAddonInfo('icon'), '', '', movie_url)
        x = x - 1

# Documentary Categories home menu item click
def ListCategories():
    dlc = setting('drill_list_color')
    dlb = setting('drill_list_bold')
    dli = setting('drill_list_italic')
    html = OpenURL('http://topdocumentaryfilms.com/')
    match = re.compile('/category/(.+?)/" >(.+?)</a>', re.DOTALL).findall(html.replace('amp;', ''))
    for url, name in match:
        if len(url) > 50:
            url = "911"
            name = "911"
        AddToMenu(style(sanitize(name), dlc, dlb, dli), url, 1, addon.getAddonInfo('icon'), '', '',movie_url)


# Movie Listing right before play
def AddVideoEntry(video, name):
    mlc = setting('movie_list_color')
    mlb = setting('movie_list_bold')
    mli = setting('movie_list_italic')
    dlc = setting('desc_list_color')
    dlb = setting('desc_list_bold')
    dli = setting('desc_list_italic')
    url = ''
    img = ''
    desc = ''
    html = OpenURL('http://topdocumentaryfilms.com/' + video)

    contents = re.compile('<div class=".+?contentpic">(.+?)</div>', re.DOTALL).findall(html.replace('amp;', ''))
    for content in contents:

        imgs = re.compile('http://cdn.topdocumentaryfilms.com/wp-content/uploads/(.+?)"', re.DOTALL).findall(
            content.replace('amp;', ''))
        for i in imgs:
            img = "http://cdn.topdocumentaryfilms.com/wp-content/uploads/" + i
        desc = re.compile('<p>(.+?)</p>', re.DOTALL).findall(content.replace('amp;', ''))[0]
        desc = re.sub('<[^>]*>', '', desc)
        words = desc.split()
    rating = re.compile('<div class="star">(.+?)</div>', re.DOTALL).findall(html.replace("amp;", ''))[0]

    iconimage = xbmc.translatePath(
        os.path.join('special://home/addons/plugin.video.topdocumentaryfilmscom/resources/media/serveimage.jpg'))

    urls = re.compile('<meta itemprop="embedUrl" content="https://www.youtube.com/embed/(.+?)">',
                      re.DOTALL).findall(html.replace('amp;', ''))
    # full length youtube video
    if len(urls) > 0:
        for u in urls:
            url = 'plugin://plugin.video.youtube/play/?video_id=' + u[0:11]

    # viemo video
    if len(url) < 1:
        # <meta itemprop="embedUrl" content="https://player.vimeo.com/video/124682831" />
        urls = re.compile('<meta itemprop="embedUrl" content="https://player.vimeo.com/video/(.+?)" />',
                          re.DOTALL).findall(html.replace('amp;', ''))
        for u in urls:
            url = "plugin://plugin.video.vimeo/play/?video_id=" + u

    # youtube playlist
    if len(url) < 1:
        # <iframe width="100%" height="325" src="http://www.youtube.com/embed/videoseries?list=PLEDAAA3B8EF7543C4" frameborder="0" allowfullscreen=""></iframe>
        urls = re.compile('http://www.youtube.com/embed/videoseries\?list=(.+?) ', re.DOTALL).findall(
            html.replace('amp;', ''))

        for u in urls:
            url = "plugin://plugin.video.youtube/play/?playlist_id=" + u[0:18]

    if len(url) < 1:
        # //www.youtube.com/embed/videoseries?list=PL_IlIlrxhtPMXcWCd_z_UZ6pn8GYPGGlo&iv_load_policy=3&showinfo=0&autohide=1
        urls = re.compile('list=PL_(.+?)_z_', re.DOTALL).findall(
            html.replace('amp;', ''))
        for u in urls:
            url = "plugin://plugin.video.youtube/play/?playlist_id=" + u

    # full length youtube video
    if len(urls) < 1:
        html = OpenURL('https://startpage.com/do/search?query=' + video + '&cat=web&pl=chrome&language=english')
        vids = re.compile('www.youtube.com/watch\?v=(.+?) ', re.DOTALL).findall(html.replace('amp;', ''))
        for vid in vids:
            url = 'plugin://plugin.video.youtube/play/?video_id=' + vid[0:11]
            break

    try:
        ex = re.compile('\[COLOR .+?\](.+?)\[/COLOR\].+?', re.DOTALL).findall(name.replace('amp;', ''))[0]\
                        .replace('[/B]','').replace('[B]','').replace('[/I]','').replace('[I]','')
    except:
        ex = name

    AddToMenu(style('     ' + ex, mlc,mlb,mli), url, 3, img, desc, '', video)

    # try:  # trying to add some additional data from the page about the movie
    AddToMenu(style('User Rating:   ', 'white', 0, 0) + getStarRating(rating,1), url, 3, iconimage, '', '', video)
    AddToMenu(style('Comments & User Reviews', 'white', 0, 0), ex.replace(' ', '-').replace('[B]', ''), 13, iconimage,
              '', '', video)
    sentence = ''
    AddToMenu(style('  ---        ', 'green', 0, 0) +
              style('---        ', 'red', 0, 0) +
              style('---        ', 'yellow', 0, 0) +
              style('         MOVIE SUMMARY         ', 'red', 1, 0) +
              style('        ---', 'yellow', 0, 0) +
              style('        ---', 'red', 0, 0) +
              style('        ---  ', 'green', 0, 0),
              url, 3, addon.getAddonInfo('icon'), '', '', video)

    for word in words:
        sentence = sentence + " " + word
        if len(sentence) > 58:
            AddToMenu(style(sentence, dlc,dlb,dli), url, 3, img, '', '', video)
            sentence = ''
            # except:
            #   print "Unexpected error:", sys.exc_info()[0]


# builds category and year movie listings
def buildListPage(html):
    name = ''
    img = addon.getAddonInfo('icon')
    articles = re.compile('<article class="module">(.+?)</article>', re.DOTALL).findall(html.replace('amp;', ''))
    for article in articles:
        name = ''
        url = ''
        imgs = re.compile('<img width="95" height="125" src="(.+?)"', re.DOTALL).findall(article.replace('amp;', ''))
        for i in imgs:
            img = i
        descs = re.compile('<p>(.+?)</p>', re.DOTALL).findall(article.replace('amp;', ''))
        for d in descs:
            desc = d
        names = re.compile(
            '<div><a title="(.+?)" href="http://topdocumentaryfilms.com/.+?/">Watch now &rarr;</a></div>',
            re.DOTALL).findall(article.replace('amp;', ''))
        for n in names:
            name = n.replace('&#039;', '')
        urls = re.compile('<div><a title=".+?" href="http://topdocumentaryfilms.com/(.+?)/">Watch now &rarr;</a></div>',
                          re.DOTALL).findall(article.replace('amp;', ''))
        for u in urls:
            url = u

        rating = re.compile('<span class="archive_rating"><span class="star_color">.+?</span>(.+?)</span>',
                            re.DOTALL).findall(article.replace("amp;", ''))[0]

        if len(url) > 0 and len(name) > 0:
            AddToMenu(buildMovieItem(name, rating, desc), url, 2, img, desc, '', movie_url)

    page = re.compile('<div class="pagination module">(.+?)</div>',
                      re.DOTALL).findall(html.replace('amp;', ''))

    for inner_code in page:
        pageno = re.compile('<a href="http://topdocumentaryfilms.com/category/(.+?)/page/(.+?)/">Next</a>',
                            re.DOTALL).findall(inner_code.replace('amp;', ''))

    for pname, purl in pageno:
        if purl == '9/11': purl = '911'
        AddToMenu(getPager(), pname + "/page/" + purl, 1, addon.getAddonInfo('icon'), '', '',
                  movie_url)

# Main Category Listing menu click
def AddCategoryEntry(url):
    html = OpenURL('http://topdocumentaryfilms.com/category/' + url)
    buildListPage(html)


# By Year home menu click
def AddByYear(url):
    html = OpenURL('http://topdocumentaryfilms.com/release/' + url)
    buildListPage(html)


# processes page listing for highest rated, recently added, most voted, most shared
def buildQuickPage(match):
    for inner_code in match:
        uls = re.compile('<ul class="side-wrap clear">(.+?)</ul>', re.DOTALL).findall(inner_code.replace('amp;', ''))
        for ul in uls:
            lis = re.compile('<li>(.+?)</li>', re.DOTALL).findall(ul.replace('amp;', ''))
            for li in lis:
                try:
                    img = ''
                    desc = ''
                    img = "http://cdn.topdocumentaryfilms.com/wp-content/uploads/" + \
                          re.compile('src="http://cdn.topdocumentaryfilms.com/wp-content/uploads/(.+?)"',
                                     re.DOTALL).findall(li.replace('amp;', ''))[0]
                    desc = sanitize(
                        re.compile('<span class="side-desc">(.+?)</span>',
                                   re.DOTALL).findall(li.replace('amp;', ''))[0])
                except:
                    pass

                entries = re.compile('<a href="http://topdocumentaryfilms.com/(.+?)/" title="(.+?)">',
                                     re.DOTALL).findall(li.replace('amp;', ''))
                for u, n in entries:
                    name = sanitize(n)
                    url = u

                desc_details = getDetails(url, 0)
                AddToMenu(buildMovieItem(name, desc_details[0], " "), url, 2, img, desc, '', movie_url)
                AddToMenu(getMovieDesc(desc), url, 2, img, desc, '', movie_url)


# Recently Added menu click
def AddRecentlyAdded():
    html = OpenURL('http://topdocumentaryfilms.com/')
    match = re.compile('<section class="module">\r\n\t<h3>Recently Added</h3>\r\n\t(.+?)</section>', re.DOTALL).findall(
        html.replace('amp;', ''))
    buildQuickPage(match)


# Highest Rated menu click
def AddHighestRated():
    html = OpenURL('http://topdocumentaryfilms.com/')
    match = re.compile('<section class="module">\r\n\t<h3>Highest Rated</h3>\r\n\t(.+?)</section>', re.DOTALL).findall(
        html.replace('amp;', ''))
    buildQuickPage(match)


# Most Voted menu click
def AddMostVoted():
    html = OpenURL('http://topdocumentaryfilms.com/')
    match = re.compile('<section class="module">\r\n\t<h3>Most Voted</h3>\r\n\t(.+?)</section>', re.DOTALL).findall(
        html.replace('amp;', ''))
    buildQuickPage(match)


# Most Shared menu click
def AddMostShared():
    html = OpenURL('http://topdocumentaryfilms.com/')
    match = re.compile('<section class="module">\r\n\t<h3>Most Shared</h3>\r\n\t(.+?)</section>', re.DOTALL).findall(
        html.replace('amp;', ''))
    buildQuickPage(match)


# Done has been clicked in the search box
def buildSearch(url):
    html = OpenURL(url)

    table = re.compile('<h3 class=\'clk\'><a href=\'http://topdocumentaryfilms.com/(.+?)/\'.+?</h3>',
                       re.DOTALL).findall(html.replace('amp;', ''))
    for tr in table:
        name = ''
        url = tr
        n = tr.replace("-", ' ').split()
        for na in n:
            name = name.replace('&#039;', '') + " " + na.capitalize()
        AddToMenu(style(name, 'white', 0, 0), url, 2, '', '', '', movie_url)


# Search menu click
def OpenSearch():
    search_entered = ''
    keyboard = xbmc.Keyboard(search_entered, 'Search iPlayer')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ', '%20')
        if search_entered == None:
            return False
    NEW_URL = 'https://startpage.com/do/search?query=Top+Documentary+Films+' + search_entered + '&cat=web&pl=chrome&language=english'
    buildSearch(NEW_URL)


# processes inbound parameters
def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param


def ShowComments(url):
    print 'http://topdocumentaryfilms.com/' + url.lower()
    html = OpenURL('http://topdocumentaryfilms.com/' + url.lower())
    section = re.compile('<section id="comments" class="comment module single-h2-title">(.+?)</section>',
                         re.DOTALL).findall(html.replace('amp;', ''))

    try:
        number = re.compile('<h2>\n\t\t\t(.+?)</a>\n\t\t</h2>', re.DOTALL).findall(section[0].replace('amp;', ''))[0]

        ols = re.compile('<ol class="commentlist">(.+?)</ol>', re.DOTALL).findall(html.replace('amp;', ''))
        page = ''

        for ol in ols:
            lis = re.compile('<li class=".+?" id="li-comment-.+?">(.+?)</li>', re.DOTALL).findall(
                ol.replace('amp;', ''))
            for li in lis:
                comment = ''
                author = \
                    re.compile('<div class="comment-author"><cite>(.+?)</cite>', re.DOTALL).findall(
                        li.replace('amp;', ''))[
                        0]
                lines = re.compile('<p>(.+?)</p>', re.DOTALL).findall(li.replace('amp;', ''))
                for line in lines:
                    comment = comment + sanitize(line) + '\n\n'

                page = page + style(author, 'yellow', 1, 0) + ' - ' + comment
    except:
        number = ("Zero User Comments or Reviews")
        page = ' '

    showText(number, page)


params = get_params()
url = None
name = None
mode = None
iconimage = None
description = None
subtitles_url = None
movie_url = ''

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    iconimage = urllib.unquote_plus(params["iconimage"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass
try:
    description = urllib.unquote_plus(params["description"])
except:
    pass
try:
    subtitles_url = urllib.unquote_plus(params["subtitles_url"])
except:
    pass
try:
    movie_url = urllib.unquote_plus(params["movie_url"])
except:
    pass

if mode == None or mode == 0 or url == None or len(url) < 1:
    TopLevelCategories()
elif mode == 1:
    AddCategoryEntry(url)
elif mode == 2:
    AddVideoEntry(url, name)
elif mode == 3:
    PlayVideo(name, url, iconimage, description, subtitles_url)
elif mode == 5:
    AddRecentlyAdded()
elif mode == 6:
    AddMostVoted()
elif mode == 7:
    AddMostShared()
elif mode == 8:
    AddHighestRated()
elif mode == 9:
    ListCategories()
elif mode == 10:
    TopLevelYears()
elif mode == 11:
    AddByYear(url)
elif mode == 12:
    OpenSearch()
elif mode == 13:
    ShowComments(movie_url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
