# -*- coding:UTF-8 -*-

# 这个程序用来爬去b站视频中播放量过10w的av号

from pymongo import MongoClient

import Math
import files
import time

import requests

# 数据库的连接
client = MongoClient('localhost', 27017)
db = client.bilibili
bilibili_video = db.video  # collection

VIDEO_NOT_EXIST = -1
REQUEST_ERROR = -999


def get_video_views(video_id):
    # b站视频信息api

    url = "http://api.bilibili.com/archive_stat/stat?aid=" + video_id
    response = requests.get(url=url).json()

    video_views = VIDEO_NOT_EXIST
    if (response["message"] == "0"):
        view = response["data"]["view"]
        if view != "--":
            video_views = view

    return video_views


def get_video_info(video_id):
    url = "http://api.bilibili.com/archive_stat/stat?aid=" + str(video_id)
    response = requests.get(url=url).json()
    try:
        if (response["message"] == "0"):
            view = response["data"]
            return view
        else:
            return None
    except Exception, e:
        print e
        return REQUEST_ERROR


def insert_2_db(videos):
    bilibili_video.insert(videos)


BUFFER_SIZE = 100  # 缓存大小
REQUEST_LENGTH = 201


def main():
    start_time = time.time()
    local_index = files.read('index.txt')
    cur_index = int(0 if local_index == '' else local_index)

    video_buffer = []  # 缓存列表
    start_index = 0 + cur_index  # 每次索引起始点
    end_ind = REQUEST_LENGTH + cur_index + 1  # 每次索引结束点，循环不包括最后一个值，这里手动加上

    for video_id in range(start_index, end_ind):
        video_info = get_video_info(video_id)

        if video_info == None:  # 为空，请求错误
            # print "当前视频为:av" + str(video_id) + " 视频不存在"
            ""
        elif video_info == REQUEST_ERROR:  # 请求错误，应该被 bilibili 请求所 ban
            # print "请求被拒"
            ""
        else:  # 请求成功
            # print "当前视频为:av" + str(video_id) + " 视频播放量为: " + str(video_info['view'])
            video_buffer.append(video_info)

            if len(video_buffer) >= BUFFER_SIZE:
                insert_2_db(video_buffer)
                video_buffer = []

        current_progress = video_id - start_index
        show_current_progress(current_progress)

        cur_index = video_id

    # 最后一次不满缓存列表时，进行数据缓存。
    if (len(video_buffer) > 0):
        insert_2_db(video_buffer)  # 将结束循环时没有插入数据库的数据插入数据库
        video_buffer = []  # 清空缓存列表

    files.save('index.txt', str(cur_index))
    end_time = time.time()
    time_coast = end_time - start_time
    print "%s条数据共耗时 %d s" % (REQUEST_LENGTH, time_coast)


def show_current_progress(current_progress):
    progress = Math.divide(current_progress, REQUEST_LENGTH, 4) * 100.0
    p_format = format(progress, '.2f')
    print "\r当前进度%s%%" % (p_format),


if __name__ == "__main__":
    main()
