import os
import lob
import json
import openai
import random
import pprint
from dotenv import load_dotenv
from flask import Flask, request, render_template

import scraper
from freq_add import freq_add_summarizer
from tf_idf import tf_idf_summarizer

load_dotenv()
lob.api_key = os.getenv('LOB_API_KEY')

MAX_TOKEN_COUNTS = 4096

# Inspiration for the template website came from the following sources:
# https://python.plainenglish.io/sentiment-analysis-flask-web-app-using-python-and-nltkintroduction-a45f893fb724
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def index_post():
    url = request.form["url"]
    passage = scraper.parse_website(url, "dyn")
    freq_summary = freq_add_summarizer(passage)
    tf_summary = tf_idf_summarizer(passage)
    sentences = passage.split('.')
    values = {}
    num_openai_summ = 3
    # Split into groups of 100 sentences in order to fit model token constraints
    openai_prompts = [" ".join(sentences[i:i+100]) for i in range(0, len(sentences), 100)]
    for i, prompt in enumerate(openai_prompts):
        openai_prompt = prompt + "\n\nTl;dr"
        openai_summary = openai.Completion.create(
            model="text-davinci-002",
            prompt=openai_prompt,
            n=num_openai_summ,
            temperature=0.7,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        values[f"openai_summ_group_{i}"] = [summ["text"] for summ in openai_summary["choices"]]
    openai_summaries = [value for key, value in values.items() if 'openai' in key.lower()]
    lob_front_summ = ""
    lob_back_summ = ""
    idx_3, idx_4 = random.sample(range(0, num_openai_summ), 2)
    if len(openai_summaries) > 1:
        idx_1, idx_2 = random.sample(range(0, len(openai_summaries)), 2)
        lob_front_summ = values[f"openai_summ_group_{idx_1}"][idx_3]
        lob_back_summ = values[f"openai_summ_group_{idx_2}"][idx_4]
    else:
        lob_front_summ = values[f"openai_summ_group_0"][idx_3]
        lob_back_summ = values[f"openai_summ_group_0"][idx_4]
    lob_front_html = "<html style='padding: 1in; font-size: 15;'>{{lob_front_summ}}</html>"
    lob_back_html = "<html style='padding: 1in; font-size: 8;'>{{lob_back_summ}}</html>"
    postcard = lob.Postcard.create(
        description = "First Postcard",
        to_address = {
            "name": "Josh Nkoy",
            "address_line1": "210 King Street",
            "address_city": "San Francisco",
            "address_state": "CA",
            "address_zip": "94107"
        },
        from_address = {
            "name": "Telecom Co.",
            "address_line1": "210 King Street",
            "address_city": "San Francisco",
            "address_state": "CA",
            "address_zip": "94107",
            "address_country": "US"
        },
        front = lob_front_html,
        back = lob_back_html,
        merge_variables = {
            "lob_front_summ": lob_front_summ,
            "lob_back_summ": lob_back_summ
        }
    )
    postcard_link = postcard["url"]
    print(postcard_link)
    return render_template(
        'index.html',
        passage = passage,
        freq_summary = freq_summary,
        tf_summary = tf_summary,
        openai_summaries=openai_summaries,
        postcard_link = postcard_link
    )

@app.route("/test-parse", methods=["POST"])
def test_parse():
    url = request.form["url"]
    dyn = request.form["dyn"]
    return scraper.parse_website(url, dyn)

@app.route("/summarize", methods=["POST"])
def summarize():
    url = request.form["url"]
    dyn = request.form["dyn"]
    num_openai_summ = int(request.form["summaries"])
    text = scraper.parse_website(url, dyn)
    freq_summary = freq_add_summarizer(text)
    tf_summary = tf_idf_summarizer(text)
    values = {}
    values['passage'] = text
    values['freq_summ'] = freq_summary
    values['tf_idf_summ'] = tf_summary
    sentences = text.split('.')
    # Split into groups of 100 sentences in order to fit model token constraints
    openai_prompts = [" ".join(sentences[i:i+100]) for i in range(0, len(sentences), 100)]
    for i, prompt in enumerate(openai_prompts):
        openai_prompt = prompt + "\n\nTl;dr"
        openai_summary = openai.Completion.create(
            model="text-davinci-002",
            prompt=openai_prompt,
            n=num_openai_summ,
            temperature=0.7,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        values[f"openai_summ_group_{i}"] = [summ["text"] for summ in openai_summary["choices"]]
    openai_summaries = [value for key, value in values.items() if 'openai' in key.lower()]
    lob_front_summ = ""
    lob_back_summ = ""
    idx_3, idx_4 = random.sample(range(0, num_openai_summ), 2)
    if len(openai_summaries) > 1:
        idx_1, idx_2 = random.sample(range(0, len(openai_summaries)), 2)
        lob_front_summ = values[f"openai_summ_group_{idx_1}"][idx_3]
        lob_back_summ = values[f"openai_summ_group_{idx_2}"][idx_4]
    else:
        lob_front_summ = values[f"openai_summ_group_0"][idx_3]
        lob_back_summ = values[f"openai_summ_group_0"][idx_4]
    lob_front_html = "<html style='padding: 1in; font-size: 15;'>{{lob_front_summ}}</html>"
    lob_back_html = "<html style='padding: 1in; font-size: 8;'>{{lob_back_summ}}</html>"
    postcard = lob.Postcard.create(
        description = "First Postcard",
        to_address = {
            "name": "Josh Nkoy",
            "address_line1": "210 King Street",
            "address_city": "San Francisco",
            "address_state": "CA",
            "address_zip": "94107"
        },
        from_address = {
            "name": "Telecom Co.",
            "address_line1": "210 King Street",
            "address_city": "San Francisco",
            "address_state": "CA",
            "address_zip": "94107",
            "address_country": "US"
        },
        front = lob_front_html,
        back = lob_back_html,
        merge_variables = {
            "lob_front_summ": lob_front_summ,
            "lob_back_summ": lob_back_summ
        }
    )
    values["postcard"] = postcard
    json_values = json.dumps(values)
    return json_values

if __name__ == "__main__":
    app.run()
