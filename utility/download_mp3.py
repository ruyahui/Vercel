#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from pytube import YouTube, Playlist
import subprocess
from bs4 import BeautifulSoup
from pydub import AudioSegment

def youtube_download(url,source_folder):
	yt = YouTube(url)
	print("Title: ",yt.title)
	filename = list(yt.title)
	irr_symbols= ["~","!","@","#","$","%","^","&","(",")","{","}","\\","/",":","*","?",'"',"<",">","|"]
	for i in range(len(filename)-1):
		if filename[i] in irr_symbols :
			filename[i]="_"

	filename = ''.join(filename)
	print("File: ",filename)
	filename = source_folder + filename + ".mp3"
	print('download from url...')
	yt.streams.filter().get_audio_only().download(filename=filename)
	print(filename, 'mp3 download ok!')
	caption = yt.captions.get_by_language_code('a.en')
	xml = caption.xml_captions  
	srt_filename = filename.replace(".mp3",".srt")
	with open(srt_filename,'w+') as f1:
		f1.write(xml2srt(xml))    # 儲存為 srt
	print(srt_filename, 'Caption ok!') 

	return filename

def xml2srt(text):
    soup = BeautifulSoup(text)                     # 使用 BeautifulSoup 轉換 xml
    ps = soup.findAll('p')                         # 取出所有 p tag 內容

    output = ''                                    # 輸出的內容
    num = 0                                        # 每段字幕編號
    for i, p in enumerate(ps):
        try:
            a = p['a']                             # 如果是自動字幕，濾掉有 a 屬性的 p tag
        except:
            try:
                num = num + 1                      # 每段字幕編號加 1
                text = p.text                      # 取出每段文字
                t = int(p['t'])                    # 開始時間
                d = int(p['d'])                    # 持續時間

                h, tm = divmod(t,(60*60*1000))     # 轉換取得小時、剩下的毫秒數
                m, ts = divmod(tm,(60*1000))       # 轉換取得分鐘、剩下的毫秒數
                s, ms = divmod(ts,1000)            # 轉換取得秒數、毫秒

                t2 = t+d                           # 根據持續時間，計算結束時間
                if t2 > int(ps[i+1]['t']): t2 = int(ps[i+1]['t'])  # 如果時間算出來比下一段長，採用下一段的時間
                h2, tm = divmod(t2,(60*60*1000))   # 轉換取得小時、剩下的毫秒數
                m2, ts = divmod(tm,(60*1000))      # 轉換取得分鐘、剩下的毫秒數
                s2, ms2 = divmod(ts,1000)          # 轉換取得秒數、毫秒


                output = output + str(num) + '\n'  # 產生輸出的檔案，\n 表示換行
                output = output + f'{h:02d}:{m:02d}:{s:02d},{ms:03d} --> {h2:02d}:{m2:02d}:{s2:02d},{ms2:03d}' + '\n'
                output = output + text + '\n'
                output = output + '\n'
            except:
                pass

    return output

def mp3_to_wave(filename):
	output_file = filename.replace(".mp3",".wav")    
	# convert mp3 to wav file	
	print("mp32wav:", filename, output_file)
	subprocess.call(['ffmpeg', '-i', filename, output_file])
	print('mp3 to wave ok!')

def mp3_to_wave_bk(filename):
	output_file = filename.replace(".mp3",".wav") 
	print("mp32wav:", filename, output_file) 
	sound = AudioSegment.from_mp3(filename)
	sound.export(output_file, format="wav")
	print('mp3 to wave ok!')

def get_playlist(url):
	playlist=Playlist(url)
	url = playlist[0]
	yt = YouTube(url)
	print("Title: ",yt.title)
	source_folder = "/tmp/"
	audio_file = youtube_download(url, source_folder)
	audio_file = audio_file.replace(".mp3",".wav")
	if not os.path.isfile(audio_file):
		mp3_to_wave(audio_file)
	return [yt.title],os.listdir(source_folder)

'''
url='https://www.youtube.com/playlist?list=PLOB7G19x6JpPcNiPj7llUNQPrtbbcpVVN'
playlist = Playlist(url)
for url in playlist:
	print(url)
	path = "toeic\\"
	source_folder = path+"source\\"
	audio_file = youtube_download(url, source_folder)
	#audio_file="toeic.mp3"
	mp3_to_wave(audio_file)
	# convert mp3 file to wav file
'''





