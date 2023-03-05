import os
from flask import Flask,render_template,request,url_for
from textsummary import summarizer
# print(__name__)
app   = Flask(__name__,template_folder='template')
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/analyze', methods = ['GET','POST'])
def analyze():
    if request.method == 'POST':
        rawtext = request.form['rawdata']
        summary,original_txt,len_orig,len_summary = summarizer(rawtext)
    return render_template("summary.html",summary = summary, original_txt = original_txt,len_orig = len_orig,len_summary = len_summary)
    
if __name__ == "__main__":
    app.debug  = True
    app.run(port = 5000)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
