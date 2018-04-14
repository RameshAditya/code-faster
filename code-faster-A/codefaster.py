import sublime
import sublime_plugin
import time
import random
import urllib
import json
from bs4 import BeautifulSoup
from collections import Counter
import sys

sys.path.insert(0, '/Users/Aditya/AppData/Local/Programs/Python/Python36-32/Lib/site-packages')
from selenium import webdriver

goto_link = ''

# quick fix to remove HTML Tags (if they show up in your questions, feel free to submit a pull request with a fix here!)
def prettify(raw_html):
	raw_html = raw_html.replace("\le","<=")
	raw_html = raw_html.replace("\lt","<")
	raw_html = raw_html.replace("&lt;", '<')
	raw_html = raw_html.replace("\ge",">=")
	raw_html = raw_html.replace("\gt",">")
	raw_html = raw_html.replace("\\times","x")
	raw_html = raw_html.replace("\dots","...")
	raw_html = raw_html.replace("~"," ")
	raw_html = raw_html.replace("\sqrt","sqrt")
	raw_html = raw_html.replace("\sum_","sum")
	raw_html = raw_html.replace("<p>","\n")
	raw_html = raw_html.replace("<i>","")
	raw_html = raw_html.replace("</i>","")
	raw_html = raw_html.replace('<div class="sample-tests">', '')
	raw_html = raw_html.replace('<span class="tex-font-style-underline">','')
	raw_html = raw_html.replace("</p>","")
	raw_html = raw_html.replace("<div>","\n")
	raw_html = raw_html.replace("</div>","\n")
	raw_html = raw_html.replace("</span>","")
	raw_html = raw_html.replace('<span class="tex-span">',"")
	raw_html = raw_html.replace('<div class="input-specification">', '')
	raw_html = raw_html.replace('<div class="section-title">', '\n')
	raw_html = raw_html.replace('<div class="problem-statement">', '')
	raw_html = raw_html.replace('<div class="header">','')
	raw_html = raw_html.replace('<div class="title">', '\n')
	raw_html = raw_html.replace('<div class="time-limit">','')
	raw_html = raw_html.replace('<div class="property-title">', '\n')
	raw_html = raw_html.replace('<div class="memory-limit">','')
	raw_html = raw_html.replace('<div class="property-title">', '\n')
	raw_html = raw_html.replace('<div class="input-file">','')
	raw_html = raw_html.replace('<div class="property-title">', '\n')
	raw_html = raw_html.replace('<div class="output-file">','')
	raw_html = raw_html.replace('<div class="property-title">', '\n')
	raw_html = raw_html.replace('<div class="output-specification">','')
	raw_html = raw_html.replace('<div class="section-title">', '\n')
	raw_html = raw_html.replace('<sup class="upper-index">', '^')
	raw_html = raw_html.replace('<span class="tex-font-style-tt">','')
	raw_html = raw_html.replace('</sup>','')
	raw_html = raw_html.replace('</sub>','')
	raw_html = raw_html.replace('<br/>','\n')
	raw_html = raw_html.replace('<pre>','')
	raw_html = raw_html.replace('<ol>','\n')
	raw_html = raw_html.replace('<ul>','\n')
	raw_html = raw_html.replace('</ol>','\n')
	raw_html = raw_html.replace('</ul>','\n')
	raw_html = raw_html.replace('<li>','\t')
	raw_html = raw_html.replace('</li>','\n')
	raw_html = raw_html.replace('</pre>' ,'')
	raw_html = raw_html.replace('<div class="sample-test">','')
	raw_html = raw_html.replace('<div class="input">','')
	raw_html = raw_html.replace('<div class="title">', '')
	raw_html = raw_html.replace('<div class="note">','')
	raw_html = raw_html.replace('<div class="output">', '')
	raw_html = raw_html.replace('<div class="section-title">', '')
	raw_html = raw_html.replace('<sub class="lower-index">' ,'')
	
	if '\n\n' in raw_html or '\n \n ':
		raw_html = raw_html.replace('\n\n','\n')
		raw_html = raw_html.replace('\n \n ','\n')
	return raw_html


class codefasteraCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global goto_link
		
		contestid = urllib.request.urlopen("http://codeforces.com/api/problemset.problems").read()
		data = json.loads(contestid.decode('utf-8'))
		value = [data['result']['problems'][j]['contestId'] for j in range(len(data['result']['problems']))]
		

		value = value[random.randint(0,len(value)-1)]
		# value = max(value) # comment the above line and un-comment this line to retrieve the most recent contest's questions 

		goto_link = "http://codeforces.com/problemset/problem/" + str(value) + "/A"
		
		route = 'Going to: ' + goto_link
		print(route)
		
		body = urllib.request.urlopen(goto_link).read()
		soup = BeautifulSoup(body)


		content = soup.find_all("div", class_ = "problem-statement")
		if len(content)==0:
			print('NOT REGISTERED')
			return 1
				
		ans = ''
		i=0
		content[0] = str(content[0]).replace("$","")
		content[0] = str(content[0])

		# Adding image support
		images = []
		ind = 0
		for i in range(len(content[0])):
			if content[0][i:i+len('src')] == 'src':
				print('FOUND AT INDEX i', i)
				ind = content[0][i:].index('"/')
				print('IMAGE START AT', ind+i)
				future = content[0][i+ind:].index('" ')
				
				images.append(content[0][i+ind+1:i+ind+future])
				ind = future+1
				i = future+1

		images = ['http://www.codeforces.com' + i for i in images]
		if len(images)>0:
			driver = webdriver.Firefox(executable_path=r'C:\Users\Aditya\Desktop\IIIT-H\code-faster\geckodriver-v0.20.1-win64\geckodriver.exe')
			driver.get(images[0])


		content[0] = prettify(content[0])
		print(content[0])
		ans = content[0]

		self.view.insert(edit, 0, "\n\n'''" + '\n' + route + '\n' + ans + "'''")

class codefasterbCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global goto_link
		
		contestid = urllib.request.urlopen("http://codeforces.com/api/problemset.problems").read()
		data = json.loads(contestid.decode('utf-8'))
		value = [data['result']['problems'][j]['contestId'] for j in range(len(data['result']['problems']))]
		

		value = value[random.randint(0,len(value)-1)]
		# value = max(value) # comment the above line and un-comment this line to retrieve the most recent contest's questions 

		goto_link = "http://codeforces.com/problemset/problem/" + str(value) + "/B"
		
		route = 'Going to: ' + goto_link
		print(route)
		
		body = urllib.request.urlopen(goto_link).read()
		soup = BeautifulSoup(body)


		content = soup.find_all("div", class_ = "problem-statement")
		if len(content)==0:
			print('NOT REGISTERED')
			return 1
				
		ans = ''
		i=0
		content[0] = str(content[0]).replace("$","")
		content[0] = str(content[0])

		# Adding image support
		images = []
		ind = 0
		for i in range(len(content[0])):
			if content[0][i:i+len('src')] == 'src':
				print('FOUND AT INDEX i', i)
				ind = content[0][i:].index('"/')
				print('IMAGE START AT', ind+i)
				future = content[0][i+ind:].index('" ')
				
				images.append(content[0][i+ind+1:i+ind+future])
				ind = future+1
				i = future+1

		images = ['http://www.codeforces.com' + i for i in images]
		if len(images)>0:
			driver = webdriver.Firefox(executable_path=r'C:\Users\Aditya\Desktop\IIIT-H\code-faster\geckodriver-v0.20.1-win64\geckodriver.exe')
			driver.get(images[0])

		content[0] = prettify(content[0])
		print(content[0])
		ans = content[0]

		self.view.insert(edit, 0, "\n\n'''" + '\n' + route + '\n' + ans + "'''")

class codefastercCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global goto_link
		
		contestid = urllib.request.urlopen("http://codeforces.com/api/problemset.problems").read()
		data = json.loads(contestid.decode('utf-8'))
		value = [data['result']['problems'][j]['contestId'] for j in range(len(data['result']['problems']))]
		

		value = value[random.randint(0,len(value)-1)]
		# value = max(value) # comment the above line and un-comment this line to retrieve the most recent contest's questions 

		goto_link = "http://codeforces.com/problemset/problem/" + str(value) + "/C"
		
		route = 'Going to: ' + goto_link
		print(route)
		
		body = urllib.request.urlopen(goto_link).read()
		soup = BeautifulSoup(body)


		content = soup.find_all("div", class_ = "problem-statement")
		if len(content)==0:
			print('NOT REGISTERED')
			return 1
				
		ans = ''
		i=0
		content[0] = str(content[0]).replace("$","")
		content[0] = str(content[0])

		# Adding image support
		images = []
		ind = 0
		for i in range(len(content[0])):
			if content[0][i:i+len('src')] == 'src':
				print('FOUND AT INDEX i', i)
				ind = content[0][i:].index('"/')
				print('IMAGE START AT', ind+i)
				future = content[0][i+ind:].index('" ')
				
				images.append(content[0][i+ind+1:i+ind+future])
				ind = future+1
				i = future+1

		images = ['http://www.codeforces.com' + i for i in images]
		if len(images)>0:
			driver = webdriver.Firefox(executable_path=r'C:\Users\Aditya\Desktop\IIIT-H\code-faster\geckodriver-v0.20.1-win64\geckodriver.exe')
			driver.get(images[0])


		content[0] = prettify(content[0])
		print(content[0])
		ans = content[0]

		self.view.insert(edit, 0, "\n\n'''" + '\n' + route + '\n' + ans + "'''")

class codefasterdCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global goto_link
		
		contestid = urllib.request.urlopen("http://codeforces.com/api/problemset.problems").read()
		data = json.loads(contestid.decode('utf-8'))
		value = [data['result']['problems'][j]['contestId'] for j in range(len(data['result']['problems']))]
		

		value = value[random.randint(0,len(value)-1)]
		# value = max(value) # comment the above line and un-comment this line to retrieve the most recent contest's questions 

		goto_link = "http://codeforces.com/problemset/problem/" + str(value) + "/D"
		
		route = 'Going to: ' + goto_link
		print(route)
		
		body = urllib.request.urlopen(goto_link).read()
		soup = BeautifulSoup(body)


		content = soup.find_all("div", class_ = "problem-statement")
		if len(content)==0:
			print('NOT REGISTERED')
			return 1
				
		ans = ''
		i=0
		content[0] = str(content[0]).replace("$","")
		content[0] = str(content[0])

		# Adding image support
		images = []
		ind = 0
		for i in range(len(content[0])):
			if content[0][i:i+len('src')] == 'src':
				print('FOUND AT INDEX i', i)
				ind = content[0][i:].index('"/')
				print('IMAGE START AT', ind+i)
				future = content[0][i+ind:].index('" ')
				
				images.append(content[0][i+ind+1:i+ind+future])
				ind = future+1
				i = future+1

		images = ['http://www.codeforces.com' + i for i in images]
		if len(images)>0:
			driver = webdriver.Firefox(executable_path=r'C:\Users\Aditya\Desktop\IIIT-H\code-faster\geckodriver-v0.20.1-win64\geckodriver.exe')
			driver.get(images[0])

		content[0] = prettify(content[0])
		print(content[0])
		ans = content[0]

		self.view.insert(edit, 0, "\n\n'''" + '\n' + route + '\n' + ans + "'''")

class codefastereCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global goto_link
		
		contestid = urllib.request.urlopen("http://codeforces.com/api/problemset.problems").read()
		data = json.loads(contestid.decode('utf-8'))
		value = [data['result']['problems'][j]['contestId'] for j in range(len(data['result']['problems']))]
		

		value = value[random.randint(0,len(value)-1)]
		# value = max(value) # comment the above line and un-comment this line to retrieve the most recent contest's questions 

		goto_link = "http://codeforces.com/problemset/problem/" + str(value) + "/E"
		
		route = 'Going to: ' + goto_link
		print(route)
		
		body = urllib.request.urlopen(goto_link).read()
		soup = BeautifulSoup(body)


		content = soup.find_all("div", class_ = "problem-statement")
		if len(content)==0:
			print('NOT REGISTERED')
			return 1
				
		ans = ''
		i=0
		content[0] = str(content[0]).replace("$","")
		content[0] = str(content[0])

		# Adding image support
		images = []
		ind = 0
		for i in range(len(content[0])):
			if content[0][i:i+len('src')] == 'src':
				print('FOUND AT INDEX i', i)
				ind = content[0][i:].index('"/')
				print('IMAGE START AT', ind+i)
				future = content[0][i+ind:].index('" ')
				
				images.append(content[0][i+ind+1:i+ind+future])
				ind = future+1
				i = future+1

		images = ['http://www.codeforces.com' + i for i in images]
		if len(images)>0:
			driver = webdriver.Firefox(executable_path=r'C:\Users\Aditya\Desktop\IIIT-H\code-faster\geckodriver-v0.20.1-win64\geckodriver.exe')
			driver.get(images[0])

		content[0] = prettify(content[0])
		print(content[0])
		ans = content[0]

		self.view.insert(edit, 0, "\n\n'''" + '\n' + route + '\n' + ans + "'''")
