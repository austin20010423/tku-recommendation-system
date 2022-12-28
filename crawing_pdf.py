import urllib.request as urlre
import re
import os
import ssl
# open the url and read


def getHtml(url):
    ssl._create_default_https_context = ssl._create_unverified_context
    page = urlre.urlopen(url)
    html = page.read()
    page.close()
    return html

# compile the regular expressions and find
# all stuff we need


def getUrl(html):
    reg = r'(?:href|HREF)="?((?:http://)?.+?\.pdf)'
    url_re = re.compile(reg)
    html = html.decode('ISO-8859-1')
    url_lst = re.findall(url_re, html)
    return(url_lst)


def getFile(url):
    file_name = url.split('/')[-1]
    u = urlre.urlopen(url)
    f = open(file_name, 'wb')

    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        f.write(buffer)
    f.close()
    print("Successful to download" + " " + file_name)


def main(sem: str, course_front_num: str, num_start: int, num_end: int, file: str):
    # get tku courses selection system url
    root_url = 'http://ap09.emis.tku.edu.tw/'

    os.mkdir(file)
    os.chdir(os.path.join(os.getcwd(), file))

    for count in range(num_start, num_end):
        if count < 10:
            count = '0'+str(count)

        url = root_url + str(sem) + '/' + str(sem) + \
            '_' + course_front_num + str(count) + '.PDF'
        if url == None:
            continue
        getFile(url)


if __name__ == '__main__':
    sem = str(input('semester: '))
    course_front_num = str(input('front number: '))
    start = int(input('start number: '))
    end = int(input('end number: '))
    file = str(input('copy in file: '))

    main(sem, course_front_num, start, end, file)
