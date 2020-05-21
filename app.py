import flask
import re
import pandas as pd
import numpy as np
import pickle
import nltk

app = flask.Flask(__name__, template_folder='templates')

with open('model/bagofwordssvm.pkl', 'rb') as f:
    model = pickle.load(f)

with open('model/bagofwordsvector300.pkl', 'rb') as f:
    most_freq = pickle.load(f)


@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return(flask.render_template('main.html'))
    if flask.request.method == 'POST':
        headline = flask.request.form.get('headline')
        opprice=flask.request.form.get('stockopprice')
        headline=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", headline).split())
        sentence_vectors = []
        sentence=headline
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
        return flask.render_template('main.html',string=str,prediction='{}'.format(output))
if __name__ == '__main__':
    app.run()
