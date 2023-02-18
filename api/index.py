#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, Response,render_template
from utility.download_mp3 import *
import wave
import os

app = Flask(__name__)

def genHeader(sampleRate, bitsPerSample, channels):
	datasize = 2000*10**6
	o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
	o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
	o += bytes("WAVE",'ascii')                                              # (4byte) File type
	o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
	o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
	o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
	o += (channels).to_bytes(2,'little')                                    # (2byte)
	o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
	o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
	o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
	o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
	o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
	o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
	return o

@app.route('/youtube')
def youtube():
	url='https://www.youtube.com/playlist?list=PLOB7G19x6JpPcNiPj7llUNQPrtbbcpVVN'
	playlist,wave_file = get_playlist(url)
	global audio_file
	audio_file = wave_file
	return render_template('index2.html', files=[audio_file,"Is file:"+str(os.path.isfile(audio_file)) ,os.listdir('/tmp')])

@app.route('/about')
def about():
    return 'About'

@app.route('/mp3')
def mp3():
	def generate():
		global audio_file
		with open(audio_file, 'rb') as video:
			data = video.read()
			'''
			while data:
				yield data
				data = video.read(1024)
			'''
			return data
	return Response(generate())


@app.route('/audio')
def audio():
	# start Recording
	'''
    def sound():

        CHUNK = 1024
        sampleRate = 44100
        bitsPerSample = 16
        channels = 2
        wav_header = genHeader(sampleRate, bitsPerSample, channels)

        stream = audio1.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,input_device_index=1,
                        frames_per_buffer=CHUNK)
        print("recording...")
        #frames = []
        first_run = True
        while True:
           if first_run:
               data = wav_header + stream.read(CHUNK)
               first_run = False
           else:
               data = stream.read(CHUNK)
           yield(data)
	'''
	def play_sound():
		CHUNK = 65536
		sampleRate = 44100
		bitsPerSample = 16
		channels = 2
		wav_header = genHeader(sampleRate, bitsPerSample, channels)
		global audio_file
		with wave.open(audio_file, "rb") as wf:
			params = wf.getparams()
			nchannels, sampwidth, framerate, nframes = params[:4]
			print(nchannels, sampwidth, framerate, nframes)
			wav_header = genHeader(framerate, sampwidth*8, nchannels)
			first_run =True
			data = wav_header + wf.readframes(nframes) # One batch transfer
			'''
			# Cut to many chunks to transfer
			while True:
				if first_run:
					data = wav_header + wf.readframes(CHUNK)
					first_run = False
				else:
					data = wf.readframes(CHUNK)
				if data == b'':
					break
				yield(data)
			'''
			return data
	return Response(play_sound())

@app.route('/')
def index():
	files=os.listdir('/tmp')
	global audio_file
	audio_file = "media/audio_tmp.wav"
	return render_template('index.html', files=[files])

audio_file = "media/audio_tmp.wav"     
if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True, threaded=True,port=5000)

