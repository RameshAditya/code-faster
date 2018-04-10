<h1 align = "center">Code Faster</h1><br />

<p align="center"> 
<b> A sublime text 3 plugin by Aditya Ramesh </b>
</p>

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![MIT License](https://img.shields.io/github/license/dawnlabs/carbon.svg)](https://github.com/dawnlabs/carbon/blob/master/LICENSE)

## What Code Faster is
#### Code Faster is a Sublime Text 3 Plugin developed with the intent of fetching problem statements directly into the sublime text editor, without needing to open a browser.

<p align="center"> <img src = "https://github.com/RameshAditya/code-faster/blob/master/sample.gif"> </p>

## What it does
The problem statements are fetched from the Codeforces programming platform (www.codeforces.com) due to their reputation in the field of algorithmic contests. In addition, their API also lent itself well for the purpose of this plug-in.

## Set up instructions
Assuming you have Sublime Text 3 set up, head over to `C:/Users/{YOUR_USERNAME}/Appdata/Roaming/Sublime Text 3/Packages/`

and paste the folder 'Code-Faster-A' in this directory.

Now, open Sublime Text 3 and along the menu bar, to the right of the `Help` option, you should notice a new option `Codeforces for Adi`, and if you do, rejoice!

## How it works

####  How it identifies the contest
Codeforces has a standard template of contest information -> `Contest Number + Letter`

This pair uniquely defines every question on the platform. 

The codeforces API was used to find the current contest number, by requesting for the information of the problems available on the platform and then the ongoing or scheduled contest's number is determined.

The letter (which is usually 'A', 'B', 'C', 'D' or 'E'} is manually entered by the user due to the input restrictions on sublime text plug-ins.

An alternative is to manually hard code 5 separate plug-ins, each that retrieves questions corresponding to different letters of the same contest number. 

The advantage of using codeforces as the target platform is that the standard problem URL is - codeforces.com/contest_number/letter

####  How it retrieves the problem statement
The BeautifulSoup module in python, allows for web scraping. Consequently, after acquiring the correct link by leveraging the codeforces API, BeautifulSoup was used to scrape the problem statement off the webpage.

## Scope for improvements
* The parsing of the problem statements of the URL was tedious, and while an alternative would be to remove all the text between every `<` and `>` pair, a quick fix was implemented due to lack of time. 

* In addition, it's probably advisable to cache the requests being made as the JSON obtained in response is pretty large in size, and in runtime requires ~ 3-4 seconds to work.

* A creative fix instead of even calling all the current information of the problems on the platform, would be to use their API to call just the most recent submissions, as during a live contest, majority of the audience on the platform will actively be submitting solutions of the same contest.
