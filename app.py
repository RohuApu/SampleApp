import flask
import pandas as pd
import numpy as np
import pickle
import nltk
import logging
import sys

nltk.download('punkt')
app = flask.Flask(__name__, template_folder='templates')

with open('model/bagofwordsdtree.pkl', 'rb') as f:
    print("MODEL LOADED--------------")
    dtree = pickle.load(f)

with open('model/bagofwordsvector300.pkl', 'rb') as f:
    most_freq = pickle.load(f)


app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

@app.route('/', methods=['GET', 'POST'])
def main():
    print("HERE..............1")
    if flask.request.method == 'GET':
        print("HERE..............2")
        return(flask.render_template('main.html'))
    if flask.request.method == 'POST':
        print("HERE..............3")
        headline = flask.request.form.get('headline')
        opprice=flask.request.form.get('stockopprice')
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        no_punct = ""
        print("HERE..............4")
        for char in headline:
            if char not in punctuations:
                no_punct = no_punct + char
        sentence=no_punct        
        sentence_vectors = []
        print("HERE..............5")
        sentence_tokens = nltk.tokenize.word_tokenize(sentence)
        sent_vec = []
        print("HERE..............6")
        for token in most_freq:
            if token in sentence_tokens:
                sent_vec.append(1)
            else:
                sent_vec.append(0)
        print("HERE..............7")
        sentence_vectors.append(sent_vec)
        sentence_vectors = np.asarray(sentence_vectors)
        print("HERE..............8")
        sentence_vectors=np.append(sentence_vectors,[opprice])
        features = [sentence_vectors]
        print("HERE..............9")
        prediction = dtree.predict(features)
        print("HERE..............10")
        if(prediction==1):
            output='rise'
        elif(prediction==-1):
            output='fall'
        str='Stocks expected to : '
        print("HERE..............11")
        return(flask.render_template('main.html',string=str,prediction='{}'.format(output)))
if __name__ == '__main__':
    app.run()
