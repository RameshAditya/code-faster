import sublime
import sublime_plugin
import time
import random
import urllib
import json
from bs4 import BeautifulSoup
from collections import Counter

class CodefasterCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		contestid = urllib.request.urlopen("http://codeforces.com/api/problemset.problems").read()
		data = json.loads(contestid.decode('utf-8'))
		
		value = [data['result']['problems'][j]['contestId'] for j in range(len(data['result']['problems']))]
		
		value = value[random.randint(0,len(value)-1)]

		#value = max(value) #comment the above line and un-comment this line to retrieve the most recent contest's questions 
		question_letter = ['A', 'B', 'C', 'D', 'E']
		goto_link = "http://codeforces.com/problemset/problem/" + str(value) + "/" + question_letter[random.randint(0,4)] #change this last letter to a constant to pull the corresponding question
		
		route = 'Going to: ' + goto_link
		#print(route)
		
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
		content[0] = content[0].replace("\le","<=")
		content[0] = content[0].replace("\lt","<")
		content[0] = content[0].replace("\ge",">=")
		content[0] = content[0].replace("\gt",">")
		content[0] = content[0].replace("\\times","x")
		content[0] = content[0].replace("\dots","...")
		content[0] = content[0].replace("~"," ")
		content[0] = content[0].replace("\sqrt","sqrt")
		content[0] = content[0].replace("\sum_","sum")
		content[0] = content[0].replace("<p>","\n")
		content[0] = content[0].replace("<i>","")
		content[0] = content[0].replace("</i>","")
		content[0] = content[0].replace('<div class="sample-tests">', '')
		content[0] = content[0].replace('<span class="tex-font-style-underline">','')
		content[0] = content[0].replace("</p>","")
		content[0] = content[0].replace("<div>","\n")
		content[0] = content[0].replace("</div>","\n")
		content[0] = content[0].replace("</span>","")
		content[0] = content[0].replace('<span class="tex-span">',"")
		content[0] = content[0].replace('<div class="input-specification">', '')
		content[0] = content[0].replace('<div class="section-title">', '\n')
		content[0] = content[0].replace('<div class="problem-statement">', '')
		content[0] = content[0].replace('<div class="header">','')
		content[0] = content[0].replace('<div class="title">', '\n')
		content[0] = content[0].replace('<div class="time-limit">','')
		content[0] = content[0].replace('<div class="property-title">', '\n')
		content[0] = content[0].replace('<div class="memory-limit">','')
		content[0] = content[0].replace('<div class="property-title">', '\n')
		content[0] = content[0].replace('<div class="input-file">','')
		content[0] = content[0].replace('<div class="property-title">', '\n')
		content[0] = content[0].replace('<div class="output-file">','')
		content[0] = content[0].replace('<div class="property-title">', '\n')
		content[0] = content[0].replace('<div class="output-specification">','')
		content[0] = content[0].replace('<div class="section-title">', '\n')
		content[0] = content[0].replace('<sup class="upper-index">', '^')
		content[0] = content[0].replace('<span class="tex-font-style-tt">','')
		content[0] = content[0].replace('</sup>','')
		content[0] = content[0].replace('</sub>','')
		content[0] = content[0].replace('<br/>','\n')
		content[0] = content[0].replace('<pre>','')
		content[0] = content[0].replace('<ol>','\n')
		content[0] = content[0].replace('<ul>','\n')
		content[0] = content[0].replace('</ol>','\n')
		content[0] = content[0].replace('</ul>','\n')
		content[0] = content[0].replace('<li>','\t')
		content[0] = content[0].replace('</li>','\n')
		content[0] = content[0].replace('</pre>' ,'')
		content[0] = content[0].replace('<div class="sample-test">','')
		content[0] = content[0].replace('<div class="input">','')
		content[0] = content[0].replace('<div class="title">', '')
		content[0] = content[0].replace('<div class="note">','')
		content[0] = content[0].replace('<div class="output">', '')
		content[0] = content[0].replace('<div class="section-title">', '')
		content[0] = content[0].replace('<sub class="lower-index">' ,'')
		
		if '\n\n' in content[0] or '\n \n ':
			content[0] = content[0].replace('\n\n','\n')
			content[0] = content[0].replace('\n \n ','\n')
		ans = content[0]
		self.view.insert(edit, 0, "\n\n'''" + '\n' + route + '\n' + ans + "'''")
