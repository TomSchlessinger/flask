from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from keybert import KeyBERT 
from requests_html import HTMLSession 
from bs4 import BeautifulSoup as bs
import urllib
import urllib.request
import json
import os

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

app = Flask(__name__)

def get_video_info(url):
    session = HTMLSession()
    response = session.get(url)
    soup = bs(response.html.html, "html.parser")
    soup.find_all("meta")
    response = session.get(url)
    soup = bs(response.html.html, "html.parser")
    result = {}
    desc = result["description"] = soup.find("meta", itemprop="description")['content']
    return desc

def getTitle(url):
    link = str.replace(url, "https://", '')
    if "youtu.be" in link:
        video_id = link.split("youtu.be/")[1]
    else:
        link = str.replace(link, "www.youtube.com/watch?v=", '')
        video_id = link.split("&ab_channel=")[0]

    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % video_id}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string
    #print(url)
    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        return data["title"] 

def getScript(link):
    link = str.replace(link, "https://", '')
    if "youtu.be" in link:
        video_id = link.split("youtu.be/")[1]
    else:
        link = str.replace(link, "www.youtube.com/watch?v=", '')
        video_id = link.split("&ab_channel=")[0]
    script = YouTubeTranscriptApi.get_transcript(video_id, ['en'])
    f_script = TextFormatter().format_transcript(script)
    f_script = str.replace(f_script,"\n", " ")
    title = getTitle(link)
    #print(f_script)
    return [f_script, title]

def getKeyWords(full_text,metadata,desc = ""):
    kw_model = KeyBERT(model='all-mpnet-base-v2')
    keywords = kw_model.extract_keywords(full_text, keyphrase_ngram_range=(1, 2), stop_words='english', highlight=False, top_n=50)
    #print(metadata)

    word_num = 0
    words = ""
    for k,w in keywords:
        if w>0.6:
            words+=k + ", "
            word_num+=1
    if(word_num < 5):
        keywords2 = kw_model.extract_keywords(metadata, keyphrase_ngram_range=(1, 2), stop_words='english', highlight=False, top_n=2)
        keywords3 = kw_model.extract_keywords(desc, keyphrase_ngram_range=(1, 2), stop_words='english', highlight=False, top_n=5)
        for word,key in keywords2:
            words+=word + ", "
        for wor,ke in keywords3:
            words+=wor + ", "
    return words

@app.route('/', methods=['GET', 'POST'])
def base_page():
    return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/faq', methods=['GET', 'POST'])
def faq():
    return render_template('faq.html')

@app.route('/projects', methods=['GET', 'POST'])
def projects():
    return render_template('projects.html')

@app.route('/ytrec', methods=['GET', 'POST'])
def ytrec():
    hasInfo = False
    if request.method == "POST" && not hasInfo:
        hasInfo = True
        out = ""
        g = request.form.get("input")
        info = getScript(g)
        script = info[0]
        data = info[1]
        desc = get_video_info(g)
        #print(desc)
        out = getKeyWords(script,data,desc)
        return render_template('ytrec.html', output=out)
    return render_template('ytrec.html')


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
