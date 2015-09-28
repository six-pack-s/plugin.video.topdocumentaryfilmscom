import urllib, urllib2, sys, re, urlparse, xbmcplugin, xbmcgui, xbmcaddon, datetime, os, math

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
addon = xbmcaddon.Addon(id='plugin.video.topdocumentaryfilmscom')
xbmcplugin.setContent(addon_handle, 'movies')
mode = args.get('mode', None)
setting = xbmcaddon.Addon().getSetting


# styles menu item words
def style(w, c, b, i, cp='false'):
    retval = ''
    if len(w) < 1: return retval
    color = ''
    bold = ''
    italic = ''
    if cp == 'true': w = w.upper()
    if len(c) > 0: color = '[COLOR ' + c.lower() + ']'
    if b == 'true': bold = '[B]'
    if i == 'true': italic = '[I]'
    retval = color + bold + italic + w
    if i == 'true': retval = retval + '[/I]'
    if b == 'true': retval = retval + '[/B]'
    if len(c) > 0: retval = retval + '[/COLOR]'
    return retval

# interprets user settings for bld, itl, cap
def setStyle(s):
    r = []
    if s == '1' or s == '4' or s == '5' or s == '7':
        r.append('true')
    else:
        r.append('false')
    if s == '2' or s == '4' or s == '6' or s == '7':
        r.append('true')
    else:
        r.append('false')
    if s == '3' or s == '5' or s == '6' or s == '7':
        r.append('true')
    else:
        r.append('false')
    return r


def setStyle(s):
    r = []
    if s == '1' or s == '4' or s == '5' or s == '7':
        r.append('true')
    else:
        r.append('false')
    if s == '2' or s == '4' or s == '6' or s == '7':
        r.append('true')
    else:
        r.append('false')
    if s == '3' or s == '5' or s == '6' or s == '7':
        r.append('true')
    else:
        r.append('false')
    return r


# Standard Movie Menu Item Look
def buildMovieItem(name, rating, desc):
    mlc = setting('movie_list_color')
<<<<<<< HEAD
    sty = setStyle(setting('movie_list_style'))
=======
    sty = setStyle(setting('movie_list_color'))
>>>>>>> 4775f0693cec24c564768a282510999470be6982
    retval = style(name, mlc, sty[0], sty[1], sty[2])
    slc = setting('show_rating')
    if slc == 'true' and rating != 0: retval = retval + getStarRating(rating, 0)
    sdc = setting('show_description')
    if sdc == 'true': retval = retval + getMovieDesc(desc[0:100])
    return retval


# returns formatted star rating
def getStarRating(star, full):
    rlc = setting('rating_list_color')
    sty = setStyle('rating_list_style')
<<<<<<< HEAD

    if full == 0:
        return style('  -  ', rlc, sty[0], sty[1]) + style(star[0:4], rlc, sty[0], sty[1]) + \
                        style('  -  ', rlc, sty[0], sty[1])
    else:
        x = math.ceil(float(star))
        y = 0
        star_rating = ""
        if full == 1:
            while y < x:
                star_rating = star_rating + " *"
                y = y + 1
        rating = star[0:4] + " " + star_rating
        return style('  -    ', rlc, sty[0], sty[1]) + style(rating, rlc, sty[0], sty[1])


=======
    x = math.ceil(float(star))
    y = 0
    star_rating = ""
    if full == 1:
        while y < x:
            star_rating = star_rating + " *"
            y = y + 1
    rating = str(int(x)) + " " + star_rating
    return style('  -  ', rlc, sty[0], sty[1]) + style(rating, rlc, sty[0], sty[1]) + style('  -  ', rlc, sty[0],
                                                                                            sty[1])


>>>>>>> 4775f0693cec24c564768a282510999470be6982
# builds movie description
def getMovieDesc(desc):
    if len(desc) < 5: return ""
    dlc = setting('desc_list_color')
    sty = setStyle(setting('desc_list_style'))
    return style(desc + "...", dlc, sty[0], sty[1], sty[2])


# builds the pager
def getPager():
    pt = setting('pager_text')
    pc = setting('pager_color')
    sty = setStyle(setting('pager_style'))
    return style(pt, pc, sty[0], sty[1], sty[2])


# cleans strings for presentation
def sanitize(str):
    str = re.sub('<[^>]*>', '', str)
    str = re.sub('[[>]*..]', '', str)
    str = re.sub('&....;', '', str)
    return str




# returns star and description for movie
def getDetails(url, full):
    retval = []
    html = OpenURL('http://topdocumentaryfilms.com/%s' % url)
    rating = re.compile('<div class="star">(.+?)</div>', re.DOTALL).findall(html.replace("amp;", ''))[0]
    if len(rating) < 1:
        retval.append(" ")
    else:
        retval.append(rating)

    contents = re.compile('<div class=".+?contentpic">(.+?)</div>', re.DOTALL).findall(html.replace('amp;', ''))
    for content in contents:
        desc = sanitize(re.compile('<p>(.+?)</p>', re.DOTALL).findall(content.replace('amp;', ''))[0])
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

        img = "http://cdn.topdocumentaryfilms.com/wp-content/uploads/%s" % \
              re.compile('http://cdn.topdocumentaryfilms.com/wp-content/uploads/(.+?)"', re.DOTALL).findall(
                  content.replace('amp;', ''))[0]
        retval.append(img)

    return retval


# Adds Menu Item to the List
def AddToMenu(name, url, mode, iconimage, description, subtitles_url, movie_url):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(
        name) + "&iconimage=" + urllib.quote_plus(iconimage) + "&description=" + urllib.quote_plus(
        description) + "&subtitles_url=" + urllib.quote_plus(subtitles_url) + "&movie_url=" + urllib.quote_plus(
        movie_url)
    liz = xbmcgui.ListItem(label=name, label2=description, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo("video",
                infoLabels={"title": name, "plot": description, "plotoutline": description, "date": "9/11/2015"})
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
        while 1:
            if xbmc.Player().isPlaying():
                break;
            else:
                xbmc.sleep(500)
        xbmc.Player().setSubtitles(subtitles_file)


# opens user ratings & comments
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
    sty = setStyle(setting('main_list_style'))
    mlb = sty[0]
    mli = sty[1]
    cap = sty[2]
    msf = setting('main_show_featured')
    sfd = setting('show_featured_dtl')

<<<<<<< HEAD

    splash = setting("splash_start")
    if splash == 'true':
        showSplash()
        xbmcaddon.Addon().setSetting("splash_start", "false")

=======
>>>>>>> 4775f0693cec24c564768a282510999470be6982
    AddToMenu(style('Documentary Categories', mlc, mlb, mli, cap), 'url', 9, addon.getAddonInfo('icon'), '', '',
              movie_url)
    AddToMenu(style('Recently Added', mlc, mlb, mli, cap), 'url', 5, addon.getAddonInfo('icon'), '', '', movie_url)
    AddToMenu(style('Highest Rated', mlc, mlb, mli, cap), 'url', 8, addon.getAddonInfo('icon'), '', '', movie_url)
    AddToMenu(style('Most Shared', mlc, mlb, mli, cap), 'url', 7, addon.getAddonInfo('icon'), '', '', movie_url)
    AddToMenu(style('Most Voted', mlc, mlb, mli, cap), 'url', 6, addon.getAddonInfo('icon'), '', '', movie_url)
    AddToMenu(style('By Year', mlc, mlb, mli, cap), 'url', 10, addon.getAddonInfo('icon'), '', '', movie_url)
    AddToMenu(style('Search', mlc, mlb, mli, cap), 'url', 12, addon.getAddonInfo('icon'), '', '', movie_url)

    if msf == 'true':
        AddToMenu(style('                                                  F  E  A  T  U  R  E  D', 'red', 1, 0, 1),
<<<<<<< HEAD
                  'url', 0, addon.getAddonInfo('icon'), '', '', 'url')
=======
            'url', 0, addon.getAddonInfo('icon'), '', '', 'url')
>>>>>>> 4775f0693cec24c564768a282510999470be6982

        html = OpenURL('http://topdocumentaryfilms.com/')
        main = re.compile('<main role="main" class="grid-2-3">(.+?)</main>', re.DOTALL).findall(
            html.replace('amp;', ''))
        for m in main:
            gallery = re.compile('<div class="module clear galery">(.+?)</div>', re.DOTALL).findall(
                m.replace('amp;', ''))
            for modules in gallery:
                url = ''
                name = ''
                gall = re.compile('\n\n(.+?).\n\n', re.DOTALL).findall(modules.replace('amp;', ''))
                try:
                    gall.append(re.compile('>.\n(.+?).\n<', re.DOTALL).findall(modules.replace('amp;', ''))[0])
                except:
                    pass

                for module in gall:
                    try:
                        img = "http://cdn.topdocumentaryfilms.com/wp-content/uploads/" + \
                              re.compile('http://cdn.topdocumentaryfilms.com/wp-content/uploads/(.+?)"',
                                         re.DOTALL).findall(
                                  module.replace('amp;', ''))[0]

                        info = re.compile(
                            '<a href="http://topdocumentaryfilms.com/(.+?)/" title="(.+?)">', re.DOTALL).findall(
                            module.replace('amp;', ''))
                        print info
                    except:
                        pass

                    for u, n in info:
                        url = u
                        name = sanitize(n)

                    if len(url) > 0 and len(name) > 0:
                        if sfd == 'true':
                            page_data = getDetails(url, 0)
                        try:
                            AddToMenu(buildMovieItem(name, page_data[0], sanitize(page_data[1])), url
                                      , 2, img, '', '', movie_url)
                        except:
                            AddToMenu(buildMovieItem(name, 0, ''), url, 2, img, '', '', movie_url)
                    else:
                        pass

            articles = re.compile('<article class="module">(.+?)</article>', re.DOTALL).findall(
                m.replace('amp;', ''))

            for article in articles:
<<<<<<< HEAD
=======
                print article
>>>>>>> 4775f0693cec24c564768a282510999470be6982
                try:
                    img = "http://cdn.topdocumentaryfilms.com/wp-content/uploads/" + \
                          re.compile('http://cdn.topdocumentaryfilms.com/wp-content/uploads/(.+?)"', re.DOTALL).findall(
                              article.replace('amp;', ''))[0]

                    info = re.compile('<h2><a href="http://topdocumentaryfilms.com/(.+?)/" title="(.+?)">.+?</a></h2>',
                                      re.DOTALL).findall(article.replace('amp;', ''))
                except:
                    pass

                if article.find('docu-text') < 0:
                    for u, n in info:
<<<<<<< HEAD
=======
                        print n
>>>>>>> 4775f0693cec24c564768a282510999470be6982
                        url = u
                        name = sanitize(n)

                        if len(url) > 0 and len(name) > 0:
                            if sfd == 'true':
                                page_data = getDetails(url, 0)
                            try:
                                AddToMenu(buildMovieItem(name, page_data[0], sanitize(page_data[1])), url
                                          , 2, img, '', '', movie_url)
                            except:
                                AddToMenu(buildMovieItem(name, 0, ''), url, 2, img, '', '', movie_url)
                        else:
                            pass


# By Year menu click
def TopLevelYears():
    dlc = setting('drill_list_color')
    sty = setStyle(setting('drill_list_style'))
    x = datetime.datetime.now().year
    while x > 1993:
        AddToMenu(style(str(x), dlc, sty[0], sty[1], sty[2]), str(x), 11, addon.getAddonInfo('icon'), '', '', movie_url)
        x = x - 1


# Documentary Categories home menu item click
def ListCategories():
    dlc = setting('drill_list_color')
    sty = setStyle(setting('drill_list_style'))
    html = OpenURL('http://topdocumentaryfilms.com/')
    match = re.compile('/category/(.+?)/" >(.+?)</a>', re.DOTALL).findall(html.replace('amp;', ''))
    for url, name in match:
        if len(url) > 50:
            url = "911"
            name = "911"
        AddToMenu(style(sanitize(name), dlc, sty[0], sty[1], sty[2]), url, 1, addon.getAddonInfo('icon'), '', '',
                  movie_url)


# Movie Listing right before play
def AddVideoEntry(video, name):
    mlc = setting('movie_list_color')
    sty = setStyle(setting('movie_list_style'))
    dlc = setting('desc_list_color')
    stx = setStyle(setting('desc_list_style'))
    url = ''
    img = ''
    desc = ''
    html = OpenURL('http://topdocumentaryfilms.com/%s' % video)

    contents = re.compile('<div class=".+?contentpic">(.+?)</div>', re.DOTALL).findall(html.replace('amp;', ''))
    for content in contents:

        imgs = re.compile('http://cdn.topdocumentaryfilms.com/wp-content/uploads/(.+?)"', re.DOTALL).findall(
            content.replace('amp;', ''))
        for i in imgs:
            img = "http://cdn.topdocumentaryfilms.com/wp-content/uploads/%s" % i

        descs = re.compile('<p>(.+?)</p>', re.DOTALL).findall(content.replace('amp;', ''))
        words = []
        for desc in descs:
            desc = re.sub('<[^>]*>', '', desc)
            words.append(desc.split())

    rating = re.compile('<div class="star">(.+?)</div>', re.DOTALL).findall(html.replace("amp;", ''))[0]

    iconimage = xbmc.translatePath(
        os.path.join('special://home/addons/plugin.video.topdocumentaryfilmscom/resources/media/serveimage.jpg'))

    # full length youtube video
    urls = re.compile('<meta itemprop="embedUrl" content="https://www.youtube.com/embed/(.+?)">',
                      re.DOTALL).findall(html.replace('amp;', ''))
    if len(urls) > 0:
        url = 'plugin://plugin.video.youtube/play/?video_id=%s' % urls[0][0:11]

    # viemo video
    if len(url) < 1:
        # <meta itemprop="embedUrl" content="https://player.vimeo.com/video/124682831" />
        urls = re.compile('<meta itemprop="embedUrl" content="https://player.vimeo.com/video/(.+?)" />',
                          re.DOTALL).findall(html.replace('amp;', ''))
        if len(urls) > 0:
            url = "plugin://plugin.video.vimeo/play/?video_id=%s" % urls[0]

    # youtube playlist
    if len(url) < 1:
        # <iframe width="100%" height="325" src="http://www.youtube.com/embed/videoseries?list=PLEDAAA3B8EF7543C4" frameborder="0" allowfullscreen=""></iframe>
        urls = re.compile('http://www.youtube.com/embed/videoseries\?list=(.+?) ', re.DOTALL).findall(
            html.replace('amp;', ''))
        if len(urls) > 0:
            url = "plugin://plugin.video.youtube/play/?playlist_id=%s" % urls[0][0:18]

    if len(url) < 1:
        # //www.youtube.com/embed/videoseries?list=PL_IlIlrxhtPMXcWCd_z_UZ6pn8GYPGGlo&iv_load_policy=3&showinfo=0&autohide=1
        urls = re.compile('list=PL_(.+?)_z_', re.DOTALL).findall(html.replace('amp;', ''))
        if len(urls) > 0:
            url = "plugin://plugin.video.youtube/play/?playlist_id=%s" % urls[0]

    # full length youtube video
    if len(urls) < 1:
        html = OpenURL('https://startpage.com/do/search?query=' + video + '&cat=web&pl=chrome&language=english')
        vids = re.compile('www.youtube.com/watch\?v=(.+?) ', re.DOTALL).findall(html.replace('amp;', ''))
        if len(vids) > 0:
            url = 'plugin://plugin.video.youtube/play/?video_id=' + vids[0][0:11]
<<<<<<< HEAD


    try:
        ex = sanitize(re.compile('\[COLOR .+?\](.+?)\[/COLOR\]', re.DOTALL).findall(name.replace('amp;', ''))[0])
=======

    try:
        ex = sanitize(re.compile('\[COLOR .+?\](.+?)\[/COLOR\].+?', re.DOTALL).findall(name.replace('amp;', ''))[0])
>>>>>>> 4775f0693cec24c564768a282510999470be6982

    except:
        ex = name

    AddToMenu(style('     ' + ex, mlc, sty[0], sty[1], sty[2]), url, 3, img, desc, '', video)
    AddToMenu(style('User Rating:   ', 'white', 0, 0) + getStarRating(rating, 1), url, 3, iconimage, '', '', video)
    AddToMenu(style('Comments & User Reviews', 'white', 0, 0), ex.replace(' ', '-').replace('[B]', ''), 13, iconimage,
              '', '', video)

<<<<<<< HEAD
    AddToMenu('                                             ' + style('M O V I E   S U M M A R Y', 'red', 1, 0, 1),
=======
    AddToMenu('                                                  ' + style('M O V I E   S U M M A R Y', 'red', 1, 0, 1),
>>>>>>> 4775f0693cec24c564768a282510999470be6982
              url, 3, addon.getAddonInfo('icon'), '', '', video)

    sentence = ''
    for word in words:
<<<<<<< HEAD
        for e in word:
            sentence = sentence + " " + e
            if len(sentence) > 58:
                AddToMenu(style(sentence, dlc, stx[0], stx[1], stx[2]), url, 3, img, '', '', video)
                sentence = ''
=======
        sentence = sentence + " " + word
        if len(sentence) > 58:
            print sentence
            AddToMenu(style(sentence, dlc, stx[0], stx[1], stx[2]), url, 3, img, '', '', video)
            sentence = ''
>>>>>>> 4775f0693cec24c564768a282510999470be6982


# builds category and year movie listings
def buildListPage(html):
    img = addon.getAddonInfo('icon')
    articles = re.compile('<article class="module">(.+?)</article>', re.DOTALL).findall(html.replace('amp;', ''))
    for article in articles:
        print article
        name = ''
        url = ''
        img = ''
        imgs = re.compile('src="http://cdn.topdocumentaryfilms.com/wp-content/uploads/(.+?)"', re.DOTALL).findall(article.replace('amp;', ''))
        for i in imgs:
<<<<<<< HEAD
            img = "http://cdn.topdocumentaryfilms.com/wp-content/uploads/%s" % i
=======
            img = i
>>>>>>> 4775f0693cec24c564768a282510999470be6982
        desc = sanitize(re.compile('<p>(.+?)</p>', re.DOTALL).findall(article.replace('amp;', ''))[0])
        if article.find('Watch now') > 0:
            names = re.compile(
                '<a title="(.+?)" href="http://topdocumentaryfilms.com/.+?/">Watch now &rarr;</a>',
                re.DOTALL).findall(article.replace('amp;', ''))
            if len(names) > 0:
                for n in names:
<<<<<<< HEAD
=======
                    print n
>>>>>>> 4775f0693cec24c564768a282510999470be6982
                    name = sanitize(n)

            urls = re.compile(
                '<div><a title=".+?" href="http://topdocumentaryfilms.com/(.+?)/">Watch now &rarr;</a></div>',
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
    sqd = setting('show_quick_dtl')
    for inner_code in match:
        uls = re.compile('<ul class="side-wrap clear">(.+?)</ul>', re.DOTALL).findall(inner_code.replace('amp;', ''))
        for ul in uls:
            lis = re.compile('<li>(.+?)</li>', re.DOTALL).findall(ul.replace('amp;', ''))
            for li in lis:
                try:
                    img = ''
                    desc = ''
                    img = "http://cdn.topdocumentaryfilms.com/wp-content/uploads/%s" % \
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

                if sqd == 'true':
                    desc_details = getDetails(url, 0)
                    AddToMenu(buildMovieItem(name, desc_details[0], " "), url, 2, img, desc, '', movie_url)
                else:
                    AddToMenu(buildMovieItem(name, 0, " "), url, 2, img, desc, '', movie_url)
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
            name = sanitize(name) + " " + na.capitalize()
        AddToMenu(style(name, 'white', 0, 0), url, 2, '', '', '', movie_url)


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


# handles comments click on movie details
def ShowComments(url):
    html = OpenURL('http://topdocumentaryfilms.com/%s' % url.lower())
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


# Search menu click
def OpenSearch():
    search_entered = ''
<<<<<<< HEAD
    keyboard = xbmc.Keyboard(search_entered, 'Search Top Documentary Films')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ', '%20')
        if len(search_entered) > 0:
            NEW_URL = 'https://startpage.com/do/search?query=Top+Documentary+Films+%s' % search_entered + '&cat=web&pl=chrome&language=english'
            buildSearch(NEW_URL)
        else:
            return False

# opens user ratings & comments
def showSplash():
    xbmc.sleep(500)
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)
    win = xbmcgui.Window(id)
    retry = 50
    head = style("T O P   D O C U M E N T A R Y   F I L M S   K O D I   A D D O N", 'white', 1,1,1)
    text = style("\nCurrent Version is 0.1.1\n\n", 'white', 1,0,1)
    text = text + style("Lastest Updates:\n\nAdded Splash Screen\n\nFixed long descriptions\n\n\n", 'white', 1,0,1)
    text = text + style("Be sure to visit the add on settings to optimize your experience\n\n", 'white', 1,0,1)
    text = text + style("Visit: http://forum.kodi.tv/showthread.php?tid=240005  for support", 'white', 1,0,1)
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel(head)
            win.getControl(5).setText(text)
            return
        except:
            pass

=======
    keyboard = xbmc.Keyboard(search_entered, 'Search iPlayer')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ', '%20')
        if search_entered == None:
            return False
    NEW_URL = 'https://startpage.com/do/search?query=Top+Documentary+Films+' + search_entered + '&cat=web&pl=chrome&language=english'
    buildSearch(NEW_URL)
>>>>>>> 4775f0693cec24c564768a282510999470be6982


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
