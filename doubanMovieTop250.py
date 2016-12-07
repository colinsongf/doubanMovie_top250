# -*- coding: utf-8 -*-

import urllib, re, os, csv, codecs, time, timeit, platform

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
            runcout += 1
            # 通过正则匹配电影名字、得分、链接等属性, (.*|)括号内加竖杠,匹配内容仅显示括号内内容以竖杠结束;
            movie_url = re.findall( r'href="(.*|)"', line )[0]
            movie_name = re.findall( r'<span.*class="title">(.*|)</span>', line )[0]
            movie_score = re.findall( r'"v:average">(\d\W\d|)</span>', line )[0]
            getComment = re.findall( r'class="inq">(.*|)</span>', line )
            if len(getComment) != 0:
                movie_comment = getComment[0]
            else:
                movie_comment = '无'
            if 'playable' in line:
                playable = '可播放'
            else:
                playable = '不可播放'
            movie_num = str(runcout)
            movie_info.append([movie_num, movie_name, movie_score, movie_comment, playable, movie_url])
        count += 1
    elapsed = round(timeit.default_timer() - start, 2)
    print u'拉取完毕, 共耗时%s秒。' %elapsed
    return movie_info

def writeFile():
    # 本地路径;
    currentPath = os.getcwd()
    # 电影资料文件路径;
    movieInfo_filePath = os.path.join(currentPath, 'doubanMovie_top250.csv')
    fileObject_open = open(movieInfo_filePath, 'wb')
    fileObject_open.write(codecs.BOM_UTF8)
    movieInfo_writeLines = csv.writer(fileObject_open, dialect='excel')
    movieInfo_writeLines.writerow(['序号', '电影名字', '电影评分', '电影短评', '播放状态', '链接'])
    movieInfo = getMovieInfo()
    print u'正在写入本地文件...'
    for movieInfo_1st in movieInfo:
        # print movieInfo_1st
        movieInfo_writeLines.writerow(movieInfo_1st)
    fileObject_open.close()
    print u'写入完成, 文件路径: %s' %movieInfo_filePath

if __name__ == '__main__':
    writeFile()