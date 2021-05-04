import requests

from Crypto.Cipher import AES

import threading

import os

def convert_ts_to_mp4(path, n):

	for i in range(n):

		ts = path + str(i) + ".ts"

		try:

			#print("[!] ready to convert " + str(i) + ".ts to mp4...")

			ts_data = (open(ts, 'rb')).read()

			#print("[!] ts_data prepare...")

			with open('movie.mp4', 'ab') as f:

				f.write(ts_data)

				#print("[!] " + str(i) + ".ts is finished...")

				f.close()

		except:

			if ( i % 2 == 0 ) and ( i > 5 ):

				print("[!] " + str(i) + ".ts is no exist or ERROR...")

				return 0

def download(url, i, crypt, key, path):

	with sem:

		if crypt == True:

			ts_file_name = str(i)

			iv = b'0000000000000000'

			#print("[!] Start downloading " + ts_file_name + ".ts from " + url + "...")

			#print("\n")

			try:

				movie = (requests.get(url, timeout = 30, verify = False)).content

				#print("[!] Start decrypt movie...")

				#print("\n")

				cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)

				movie_ts = cipher.decrypt(movie)

				#print("[!] Write movie into file ts...")

				#print("\n")

				f = open(path + ts_file_name + ".ts", 'wb')

				f.write(movie_ts)

				f.close()

				#print("ts " + str(i) + "finish...")

				#print("\n")

			except:

				print("[!] " + url + "("+ ts_file_name +".ts) Error...")

		elif crypt == False:

			ts_file_name = str(i)

			try:

				movie_ts = (requests.get(url, timeout = 30, verify = False)).content

				f = open(path + ts_file_name + ".ts", 'wb')

				f.write(movie_ts)

				f.close()

			except:

				print("[!] " + url + "("+ ts_file_name + ".ts) Error...")

		return

def main_control(main_url, file_name_index, crypt, key, path):

	print("[!] running main_control function...")

	with open(file_name_index, 'r') as f:

		url_list = f.readlines()

		f.close()

	for i in range(0, len(url_list)):

		if url_list[i][0] == '#':

			pass

		elif url_list[i][0] != '#':

			url = ""

			#url = main_url + str(url_list[i][0:41])

			url = main_url + str(url_list[i][0:11])
			
			(threading.Thread(target = download, args = (url, i, crypt, key, path))).start()

if __name__ =="__main__":

	os.system("cls")

	limit = 100

	sem = threading.Semaphore(limit)

	requests.packages.urllib3.disable_warnings()

	#main_url = "https://XXXXXXXXX.com"

	file_name_index = "index.txt"

	crypt = False

	key = "8213eefee98fec9a"

	path = "XXX/XXX/"

	n = 4945

	print(f" [] limit => {limit} \n [] main_url => {main_url} \n [] file_name_index => {file_name_index} \n [] crypt => {crypt} \n [] key => {key} \n [] path => {path} \n")

	con = input(" --------- \n [ 1 ] main_control \n [ 2 ] convert_ts_to_mp4 \n [ _ ] Exit \n:")

	if str(con) == "1":

		main_control(main_url, file_name_index, crypt, key, path)

	elif str(con) == "2":

		convert_ts_to_mp4(path ,n)
