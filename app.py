import flask
import pandas as pd
import numpy as np
import pickle
import nltk
import logging
import sys


app = flask.Flask(__name__, template_folder='templates')

with open('model/bagofwordssvm.pkl', 'rb') as f:
    model = pickle.load(f)

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
        sentence_tokens = nltk.word_tokenize(sentence)
        sent_vec = []
        for token in most_freq:
            if token in sentence_tokens:
                sent_vec.append(1)
            else:
                sent_vec.append(0)
        sentence_vectors.append(sent_vec)
        sentence_vectors = np.asarray(sentence_vectors)
        sentence_vectors=np.append(sentence_vectors,[opprice])
        features = [sentence_vectors]
        
        prediction = model.predict(features)
        if(prediction==1):
            output='rise'
        elif(prediction==-1):
            output='fall'
        elif(prediction==0):
            output='be neutral'
        str='Stocks expected to : '
        return(flask.render_template('main.html',string=str,prediction='{}'.format(output)))
if __name__ == '__main__':
    app.run()
