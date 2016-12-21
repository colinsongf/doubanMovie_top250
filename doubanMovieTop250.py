# -*- coding: utf-8 -*-

import urllib, re, os, csv, codecs, time, timeit, platform, sys

# 拉取进度计算;
def DownloadProgress(now, end=250.0):
    downloadProgress = now / end * 100
    sys.stdout.write(u'\r正在拉取电影信息: %.1f%%' %downloadProgress)
    sys.stdout.flush()
    if now == end:
        sys.stdout.write(u'100.00%')
        sys.stdout.write(u'\r电影信息拉取完毕, ')
        sys.stdout.flush()

# 获取电影信息;
def getMovieInfo():
    if platform.system() == 'Windows':
        default_timer = time.clock
    else:
        default_timer = time.time
    start = timeit.default_timer()
    print u'开始拉取电影信息...'
    count = 0
    runcout = 0
    movie_info = []
    # 通过循环获取10页电影内容（25*10, 豆瓣top250）;
    while count <= 10:
        # 计算页数;
        page = str(count * 25)
        url = 'https://movie.douban.com/top250?start=%s&filter=' %page
        # 通过<em class="">标签切割网页内容进行分割, 分割成一部部电影;
        doubanMovie_list = urllib.urlopen(url).read().split('<em class="">')[1:]
        for line in doubanMovie_list:
            freePlay_scr = ''
            freePlay_url = ''
            runcout += 1
            DownloadProgress(runcout)
            # 通过正则匹配电影名字、得分、链接等属性, (.*|)括号内加竖杠,匹配内容仅显示括号内内容以竖杠结束;
            movie_url = re.findall( r'href="(.*|)"', line )[0]
            movie_name = re.findall( r'<span.*class="title">(.*|)</span>', line )[0]
            # print movie_name
            movie_score = re.findall( r'"v:average">(\d\W\d|)</span>', line )[0]
            getComment = re.findall( r'class="inq">(.*|)</span>', line )
            if len(getComment) != 0:
                movie_comment = getComment[0]
            else:
                movie_comment = '无'
            # 可播放的视频, 查找是否有免费播放的资源;
            if 'playable' in line:
                freePlay_scr_list = []
                freePlay_url_list = []
                playable = '可播放'
                doubanMovie = urllib.urlopen(movie_url).readlines()
                for index, team in enumerate(doubanMovie):
                    if '免费' in team:
                        freeMovie_scr_url = doubanMovie[index-4]
                        try:
                            find_src = re.findall('data-cn="(.*|)"\shref=', freeMovie_scr_url)[0]
                            find_url = re.findall('href="(.*|)"\s', freeMovie_scr_url)[0]
                            # 搜狐视频资源有问题, 部分资源链接有问题;
                            if '搜狐' not in find_src and 'http' in find_url:
                                freePlay_scr_list.append(find_src)
                                freePlay_url_list.append(find_url)
                        except:
                            pass
                if len(freePlay_scr_list) > 0:
                    freePlay_scr = freePlay_scr_list[0]
                    freePlay_url = freePlay_url_list[0]
                else:
                    freePlay_scr = '付费'
            else:
                playable = '不可播放'
            movie_num = str(runcout)
            movie_info.append([movie_num, movie_name, movie_score, movie_comment, playable, freePlay_scr, freePlay_url, movie_url])
        count += 1
    elapsed = round(timeit.default_timer() - start, 2)
    print u'共耗时%s秒。' %elapsed
    return movie_info

def writeFile():
    # 本地路径;
    currentPath = os.getcwd()
    # 电影资料文件路径;
    movieInfo_filePath = os.path.join(currentPath, 'doubanMovie_top250.csv')
    fileObject_open = open(movieInfo_filePath, 'wb')
    fileObject_open.write(codecs.BOM_UTF8)
    movieInfo_writeLines = csv.writer(fileObject_open, dialect='excel')
    movieInfo_writeLines.writerow(['序号', '电影名字', '电影评分', '电影短评', '播放状态', '免费播放资源', '播放链接','电影详细资料'])
    movieInfo = getMovieInfo()
    print u'正在写入本地文件...'
    for movieInfo_1st in movieInfo:
        movieInfo_writeLines.writerow(movieInfo_1st)
    fileObject_open.close()
    print u'写入完成, 文件路径: %s' %movieInfo_filePath

if __name__ == '__main__':
    writeFile()