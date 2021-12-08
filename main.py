#!/usr/bin/env python
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from flask import Flask, render_template, request
import json, urllib
from wordcloud import WordCloud
import matplotlib.pyplot as plt

app = Flask("Final_Project")

def get_synonyms(word, key = "b218b944-89f2-4f6d-909e-37649d0fc5fa"):
    key_dict = {"key": key}
    keystr = urllib.parse.urlencode(key_dict)
    word = "-".join(word.split(" "))
    request_url = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/" + word + "?" + keystr
    request_str = urllib.request.urlopen(request_url).read()
    word_json = json.loads(request_str)
    syns_lists = word_json[-1]["meta"]["syns"]
    final_list = []
    for syns in syns_lists:
        for syn in syns:
            final_list.append(syn)
    return final_list

def get_synonyms_safe(word, key = "b218b944-89f2-4f6d-909e-37649d0fc5fa"):
    try:
        result = get_synonyms(word = word, key = key)
    except Exception as error:
        print("Error: " + str(error))
    return result

def get_frequency(word_list):
    new_list = []
    for word in word_list:
        new_list.append(word)
        syn_list = get_synonyms_safe(word)
        for new_word in syn_list:
            new_list.append(new_word)
    freq_dict = {}
    for word in new_list:
        if word not in freq_dict:
            freq_dict[word] = 0
        freq_dict[word] += 1
    return freq_dict

def make_word_cloud(freq_dict):
    cloud = WordCloud(background_color="Moccasin")
    cloud.generate_from_frequencies(freq_dict)
    plt.imshow(cloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

@app.route("/",methods=["GET","POST"])
def main_handler():
    app.logger.info("In MainHandler")
    word = request.form.get('word')
    if word:
        syn_list = get_synonyms_safe(word)
        syn_dict = get_frequency(syn_list)
        cloud_image = make_word_cloud(syn_dict)
        return render_template('project_template.html',
            word=word,
            cloud_image = cloud_image)
    else:
        return render_template('project_template.html',
            page_title="CROW - Error",
            prompt="We need a word")

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)