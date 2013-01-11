#!/usr/bin/env python
from pyquery import PyQuery as pq
from lxml import etree
import urllib
import urllib2
import subprocess
import os
import sys
import getopt

def usage():
    print """
this tiny tool use for download you 163 open-course auto
it has only one needed param: the open-course web url at open.163 
it support:
    '-d' for output detail debug info
    '-h' for this usage info
    '-l' for if you just want get the url list of video, not to download it 
    '-n' for if you just want get the video list of video, not to download it 
example:
    ./main.py http://v.163.com/special/sp/singlevariablecalculus.html
    ./main.py -n http://v.163.com/special/sp/singlevariablecalculus.html
    ./main.py -l http://v.163.com/special/sp/singlevariablecalculus.html
    """

try:                                
    opts, args = getopt.getopt(sys.argv[1:], "hnld", ["help", "name-only", "list-only", "debug"])
except getopt.GetoptError:
    usage()
    sys.exit(2)                     

if len(args) == 1:
    course_url = args[0]
else:
    usage()
    sys.exit(2)                     

debug_flag = False
usage_flag = False
list_only_flag = False
list_name_flag = False
for opt, value in opts:
    if opt == '-d':
        debug_flag = True
    if opt == '-h':
        usage_flag = True
    if opt == '-l':
        list_only_flag = True
    if opt == '-n':
        list_name_flag = True


def get_page_html(page_url):
    user_agent = "Mozilla/4.0 (compatible;MSIE 5.5; Windows NT)"
    header = {'User-Agent':user_agent}
    req = urllib2.Request(url=page_url, headers=header)
    response = urllib2.urlopen(req)
    page = response.read()
    return page

if usage_flag:
    usage()
    sys.exit(2)

page_html = get_page_html(course_url) 
d = pq(page_html)
video_tag_object = d(".downbtn")
video_url_list = []
for index in range(len(video_tag_object)):
    video_url = video_tag_object.eq(index).attr("href")
    video_url_list.append(video_url)

def print_video_url_list():
    for video in video_url_list:
        print video

if list_only_flag:
    print_video_url_list()
    sys.exit(3)
if debug_flag:
    print_video_url_list()

video_name_list = []
video_tag_object = d(".u-ctitle")
for index in range(len(video_tag_object)):
    video_tag_object.eq(index).text()
    video_tag = video_tag_object.eq(index).text()
    video_name_list.append(video_tag) 

def print_video_name_list():
    for video in video_name_list:
        print video

if list_name_flag:
    print_video_name_list()
    sys.exit(3)
if debug_flag:
    print_video_name_list()

for index in range(len(video_tag_object)):
    video_url = video_url_list[index]
    _, file_extension = os.path.splitext(video_url)
    file_name = video_name_list[index] + file_extension
    wget_process_args = ["wget", video_url, "-O", file_name]
    if debug_flag:
        print wget_process_args
    return_code = subprocess.call(wget_process_args)
    if debug_flag:
        print return_code
