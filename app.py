# app.py
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import nltk

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Dictionary for part-of-speech colors
pos_colors = {
    'NN': '#ADD8E6',  # Light Blue for Noun
    'DT': '#FFFF00',  # Yellow for Determiner
    'IN': '#FFC0CB',  # Pink for Preposition
    'JJ': '#FFA500',  # Orange for Adjective
    'VB': '#008000',  # Green for Verb
    'RB': '#0000FF',  # Blue for Adverb
    'PRP': '#FF00FF', # Magenta for Pronoun
    # More POS tags can be added here
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
        # Extract the sentence to be analyzed
        sentence = data[8:]
        tokens = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)
        
        # Generate the colored sentence
        colored_sentence = ' '.join([f'<span style="background-color: {pos_colors.get(tag, "#FFFFFF")}">{word}</span>' for word, tag in tagged])
        emit('message', {'data': colored_sentence, 'html': True}, broadcast=True)
    else:
        send(data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
