import os
import re
import string
import pickle as pkl
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model, model_from_json, Model
from tensorflow.keras.layers import Input
from tensorflow.keras.preprocessing.sequence import pad_sequences
from PIL import Image
import cv2

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variables for models
cnn_model = None
nlp_encoder_model = None
nlp_decoder_model = None
tokenizer_input = None
tokenizer_target = None
reverse_word_map_target = None

def load_models():
    """Load all models and tokenizers"""
    global cnn_model, nlp_encoder_model, nlp_decoder_model
    global tokenizer_input, tokenizer_target, reverse_word_map_target
    
    try:
        # Load CNN model for food detection
        if os.path.exists('vgg191_multilabel_model_sample.keras'):
            cnn_model = load_model('vgg191_multilabel_model_sample.keras')
            print("✓ CNN model loaded successfully")
        else:
            print("⚠ CNN model not found")

        # Load tokenizers
        if os.path.exists('tokenizer_input.pkl'):
            with open('tokenizer_input.pkl', 'rb') as f:
                tokenizer_input = pkl.load(f)
            print("✓ Input tokenizer loaded")

        if os.path.exists('tokenizer_target.pkl'):
            with open('tokenizer_target.pkl', 'rb') as f:
                tokenizer_target = pkl.load(f)
            reverse_word_map_target = {v: k for k, v in tokenizer_target.word_index.items()}
            print("✓ Target tokenizer loaded")

        # Load NLP model architecture and weights
        if (os.path.exists('model_qa.json') and 
            os.path.exists('model_qa.weights.h5') and
            tokenizer_input and tokenizer_target):
            
            load_nlp_inference_models()
            print("✓ NLP models loaded successfully")
        else:
            print("⚠ NLP model files not found or tokenizers missing")
            
    except Exception as e:
        print(f"✗ Error loading models: {e}")

def load_nlp_inference_models():
    """Load NLP inference models (encoder and decoder)"""
    global nlp_encoder_model, nlp_decoder_model
    
    try:
        # Load the main model
        with open('model_qa.json', 'r') as f:
            nlp_model_json = f.read()
        nlp_model = model_from_json(nlp_model_json)
        nlp_model.load_weights('model_qa.weights.h5')
        
        latent_dim = 256
        
        # Create encoder model
        encoder_inputs = nlp_model.input[0]
        encoder_outputs, state_h, state_c = nlp_model.layers[4].output  # LSTM layer output
        encoder_states = [state_h, state_c]
        nlp_encoder_model = Model(encoder_inputs, encoder_states)
        
        # Create decoder model
        decoder_state_h_input = Input(shape=(latent_dim,))
        decoder_state_c_input = Input(shape=(latent_dim,))
        decoder_state_input = [decoder_state_h_input, decoder_state_c_input]
        
        decoder_input_inf = nlp_model.input[1]
        decoder_emb_inf = nlp_model.layers[3](decoder_input_inf)  # Embedding layer
        decoder_lstm_inf = nlp_model.layers[5]  # Decoder LSTM layer
        decoder_output_inf, decoder_state_h_inf, decoder_state_c_inf = decoder_lstm_inf(
            decoder_emb_inf, initial_state=decoder_state_input
        )
        decoder_state_inf = [decoder_state_h_inf, decoder_state_c_inf]
        dense_inf = nlp_model.layers[6]  # Dense layer
        decoder_output_final = dense_inf(decoder_output_inf)
        
        nlp_decoder_model = Model(
            [decoder_input_inf] + decoder_state_input,
            [decoder_output_final] + decoder_state_inf
        )
        
    except Exception as e:
        print(f"Error creating inference models: {e}")
        nlp_encoder_model = None
        nlp_decoder_model = None

# Constants
max_length_src = 20
class_names = ['good_items', 'spoiled_items']

predefined_responses = {
    "hello": "Hi there! How can I assist you? You can ask me questions.",
    "how are you": "I'm doing great! I can help with questions.",
    "what is your name": "I'm an Integrated ChatBot.",
    "bye": "Goodbye! Have a great day! Please provide a rating (1-5):",
    "food is spoiled": "Please upload an image of the spoiled food for verification.",
    "my food is cold": "Could you provide an image for verification?",
    "help": "I can answer questions and detect food spoilage. For spoilage, type 'food is spoiled' and upload an image."
}

def clean_text(text):
    """Clean text by removing punctuation and digits"""
    text = text.lower()
    text = re.sub(f'[{re.escape(string.punctuation)}]', '', text)
    text = re.sub(r'\d+', '', text)
    return text.strip()

def decode_sequence(input_seq):
    """Decode sequence using encoder-decoder models"""
    if not nlp_encoder_model or not nlp_decoder_model:
        return "NLP models not available"
    
    # Encode the input
    state_values = nlp_encoder_model.predict(input_seq, verbose=0)
    
    # Initialize target sequence
    target_seq = np.zeros((1, 1))
    if 'start' in tokenizer_target.word_index:
        target_seq[0, 0] = tokenizer_target.word_index['start']
    
    stop_condition = False
    decoded_sentence = ''
    
    while not stop_condition:
        output_tokens, h, c = nlp_decoder_model.predict(
            [target_seq] + state_values, verbose=0
        )
        
        # Sample a token
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        
        if sampled_token_index in reverse_word_map_target:
            sampled_word = reverse_word_map_target[sampled_token_index]
            decoded_sentence += ' ' + sampled_word
            
            # Stop conditions
            if sampled_word == 'end' or len(decoded_sentence) > 100:
                stop_condition = True
        else:
            stop_condition = True
        
        # Update target sequence and states
        target_seq[0, 0] = sampled_token_index
        state_values = [h, c]
    
    return decoded_sentence.strip()

def get_nlp_response(question):
    """Generate response using NLP model"""
    if not tokenizer_input:
        return "NLP tokenizer not available"
    
    cleaned_question = clean_text(question)
    input_seq = tokenizer_input.texts_to_sequences([cleaned_question])
    pad_sequence = pad_sequences(input_seq, maxlen=max_length_src, padding='post')
    response = decode_sequence(pad_sequence)
    
    if response.strip().endswith('end'):
        response = response.replace(' end', '').strip()
    
    return response if response.strip() else "I couldn't generate a proper response."

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.json
        user_input = data.get('message', '')
        user_input_lower = user_input.lower().strip()
        
        # Check predefined responses first
        if user_input_lower in predefined_responses:
            bot_reply = predefined_responses[user_input_lower]
        else:
            # Try NLP model
            bot_reply = get_nlp_response(user_input)
        
        return jsonify({"response": bot_reply})
    
    except Exception as e:
        return jsonify({"error": f"Error processing request: {str(e)}"}), 500

@app.route('/api/classify', methods=['POST'])
def classify():
    """Handle image classification"""
    try:
        if 'file' not in request.files:
            return jsonify({"result": "No file uploaded."})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"result": "No file selected."})
        
        # Save uploaded file
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        if not cnn_model:
            return jsonify({"result": "CNN model not available for classification."})
        
        # Load and preprocess image
        frame = cv2.imread(filepath)
        if frame is None:
            return jsonify({"result": "Error: Unable to load image."})
        
        # Resize and normalize
        img = cv2.resize(frame, (224, 224))
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        
        # Make prediction
        predictions = cnn_model.predict(img, verbose=0)
        threshold = 0.5
        predicted_label = class_names[1] if predictions[0][0] >= threshold else class_names[0]
        
        if predicted_label == 'spoiled_items':
            result = "I can see your food is spoiled. You can claim a refund. I apologize for the inconvenience."
        else:
            result = "Your food appears to be in good condition. Refund cannot be processed based on the image."
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify({"result": result})
    
    except Exception as e:
        return jsonify({"result": f"Error processing image: {str(e)}"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    model_status = {
        "cnn_loaded": cnn_model is not None,
        "nlp_loaded": nlp_encoder_model is not None and nlp_decoder_model is not None,
        "tokenizers_loaded": tokenizer_input is not None and tokenizer_target is not None
    }
    return jsonify({"status": "healthy", "models": model_status})

if __name__ == '__main__':
    print("Loading models...")
    load_models()
    print("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000)