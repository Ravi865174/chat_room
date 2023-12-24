from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import nltk

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

pos_colors = {
    'JJ': '#ffcb75',   # Adjective - Light Orange
    'RB': '#ce9999',   # Adverb - Pale Violet Red
    'CC': '#cccc9f',   # Conjunction - Dark Khaki
    'DT': '#999ac8',   # Determiner - Slate Blue
    'NN': '#cccccc',   # Noun - Light Grey
    'NNS': '#cccccc',  # Noun, plural - Light Grey
    'NNP': '#cccccc',  # Proper noun, singular - Light Grey
    'NNPS': '#cccccc', # Proper noun, plural - Light Grey
    'CD': '#5ccc9e',   # Number - Medium Aquamarine
    'IN': '#ff99c9',   # Preposition - Light Pink
    'PRP': '#eeed88',  # Pronoun - Pale Goldenrod
    'PRP$': '#eeed88', # Possessive pronoun - Pale Goldenrod
    'VB': '#c9fe7e',   # Verb, base form - Light Green
    'VBD': '#c9fe7e',  # Verb, past tense - Light Green
    'VBG': '#c9fe7e',  # Verb, gerund or present participle - Light Green
    'VBN': '#c9fe7e',  # Verb, past participle - Light Green
    'VBP': '#c9fe7e',  # Verb, non-3rd person singular present - Light Green
    'VBZ': '#c9fe7e',  # Verb, 3rd person singular present - Light Green
}

@app.route('/')
def sessions():
    return render_template('chat.html')

@socketio.on('connect')
def on_connect():
    send('Someone has joined the chat!', broadcast=True)

@socketio.on('message')
def handle_message(data):
    if data.startswith('analyze: '):
        # Extract sentence to analyzed
        sentence = data[8:]
        tokens = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)
        
        # Generate color for sentence
        colored_sentence = ' '.join([f'<span style="background-color: {pos_colors.get(tag, "#FFFFFF")}">{word}</span>' for word, tag in tagged])
        emit('message', {'data': colored_sentence, 'html': True}, broadcast=True)
    else:
        send(data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
