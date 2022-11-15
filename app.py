import json
import openai
from dotenv import load_dotenv
from flask import Flask, request, render_template

import scraper
from freq_add import freq_add_summarizer
from tf_idf import tf_idf_summarizer

load_dotenv()
MAX_TOKEN_COUNTS = 4096

app = Flask(__name__)

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
    # Split into groups of 100 sentences in order to fit model token constraints
    openai_prompts = [" ".join(sentences[i:i+100]) for i in range(0, len(sentences), 100)]
    for i, prompt in enumerate(openai_prompts):
        openai_prompt = prompt + "\n\nTl;dr"
        openai_summary = openai.Completion.create(
            model="text-davinci-002",
            prompt=openai_prompt,
            n=3,
            temperature=0.7,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        values[f"openai_summ_group_{i}"] = [summ["text"] for summ in openai_summary["choices"]]
    openai_summaries = [value for key, value in values.items() if 'openai' in key.lower()]
    return render_template(
        'index.html',
        passage = passage,
        freq_summary = freq_summary,
        tf_summary = tf_summary,
        openai_summaries=openai_summaries
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
    json_values = json.dumps(values)
    return json_values

if __name__ == "__main__":
    app.run()
