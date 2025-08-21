# 🤖 AI-Chatbot-Project-Intelligent-Food-Spoilage-Detector-CNN-NLP

## 📋 Project Overview

This project combines **Computer Vision (CNN)** and **Natural Language Processing (NLP)** to create an intelligent customer service chatbot that can:
- Answer customer queries about food-related issues
- Detect food spoilage from uploaded images
- Provide automated refund recommendations based on image analysis

## 🏗️ Project Architecture

```
NLP_CHATBOT/
├── backend/
│   ├── app.py                              # Flask server with AI models
│   ├── requirements.txt                    # Python dependencies
│   └── [Model Files]:
│       ├── model_qa.json                   # NLP model architecture
│       ├── model_qa.weights.h5             # NLP model weights
│       ├── tokenizer_input.pkl             # Input text tokenizer
│       ├── tokenizer_target.pkl            # Target text tokenizer
│       └── vgg191_multilabel_model_sample.keras  # CNN model for image classification
├── frontend/
│   ├── public/
│   │   ├── index.html                      # HTML template
│   │   ├── robot.png                       # Chatbot avatar (optional)
│   │   └── user.png                        # User avatar (optional)
│   ├── src/
│   │   ├── index.js                        # React entry point
│   │   ├── App.js                          # Main app component
│   │   ├── Chatbot.js                      # Chat logic & API calls
│   │   ├── ChatInput.js                    # Input field & file upload
│   │   ├── ChatMessages.js                 # Message container
│   │   ├── ChatMessage.js                  # Individual message components
│   │   └── style.css                       # Complete styling
│   └── package.json                        # React dependencies
└── README.md                               # This file
```

## 🧠 Technical Components

### 1. **Computer Vision (CNN Model)**
- **Architecture**: VGG19 with custom classification layers
- **Purpose**: Classify food images as "spoiled" or "fresh"
- **Training**: Fine-tuned on custom dataset of food images
- **Input**: 224x224 RGB images
- **Output**: Binary classification (spoiled/good items)

### 2. **Natural Language Processing (NLP Model)**
- **Architecture**: Encoder-Decoder LSTM with attention mechanism
- **Purpose**: Generate responses to customer queries
- **Training**: Trained on ~400 question-answer pairs
- **Features**: Text preprocessing, tokenization, sequence-to-sequence generation

### 3. **Frontend (React.js)**
- **Framework**: React with functional components and hooks
- **Features**: 
  - Real-time chat interface
  - Image upload with preview
  - Responsive design
  - Loading states and error handling

### 4. **Backend (Flask API)**
- **Framework**: Flask with CORS support
- **Endpoints**:
  - `/api/chat` - Text-based conversations
  - `/api/classify` - Image classification
  - `/api/health` - System health check

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd NLP_CHATBOT/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install flask flask-cors tensorflow keras numpy opencv-python pillow pickle-mixin
   ```
   *Or use requirements.txt if available:*
   ```bash
   pip install -r requirements.txt
   ```

4. **Place model files**
   Ensure these files are in the backend directory:
   - `model_qa.json`
   - `model_qa.weights.h5`
   - `tokenizer_input.pkl`
   - `tokenizer_target.pkl`
   - `vgg191_multilabel_model_sample.keras`

5. **Start the backend server**
   ```bash
   python app.py
   ```
   Server will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install react react-dom react-scripts
   ```

3. **Start the development server**
   ```bash
   npm start
   ```
   Application will open on `http://localhost:3000`

## 🔄 How It Works

### Text Conversation Flow:
1. User sends a message
2. Frontend sends POST request to `/api/chat`
3. Backend processes text using NLP model
4. Response is generated and sent back
5. Frontend displays the response

### Image Classification Flow:
1. User uploads an image
2. Frontend sends POST request to `/api/classify`
3. Backend processes image using CNN model
4. Classification result determines response
5. Frontend displays analysis result

## 🛠️ API Endpoints

### POST `/api/chat`
**Purpose**: Handle text-based conversations
```json
{
  "message": "How can you help me?"
}
```
**Response**:
```json
{
  "response": "I can help with food spoilage detection..."
}
```

### POST `/api/classify`
**Purpose**: Classify uploaded food images
- **Content-Type**: `multipart/form-data`
- **Body**: Form data with `file` field containing image

**Response**:
```json
{
  "result": "Your food appears to be in good condition..."
}
```

### GET `/api/health`
**Purpose**: Check system health and model loading status
```json
{
  "status": "healthy",
  "models": {
    "cnn_loaded": true,
    "nlp_loaded": true,
    "tokenizers_loaded": true
  }
}
```

## 🎯 Features

- ✅ **Dual AI Integration**: Combines CNN and NLP models
- ✅ **Real-time Chat**: Instant responses to customer queries
- ✅ **Image Analysis**: Upload and analyze food images
- ✅ **Responsive Design**: Works on desktop and mobile
- ✅ **Error Handling**: Graceful handling of errors and edge cases
- ✅ **File Validation**: Checks file type and size before upload
- ✅ **Health Monitoring**: API endpoint to check system status

## 📊 Model Performance

### CNN Model (VGG19):
- **Task**: Binary classification (spoiled vs fresh food)
- **Architecture**: VGG19 + custom classification head
- **Training**: Fine-tuned with data augmentation and callbacks

### NLP Model (Encoder-Decoder LSTM):
- **Task**: Question-answering for customer service
- **Architecture**: LSTM-based sequence-to-sequence model
- **Dataset**: ~400 curated question-answer pairs
- **Features**: Text cleaning, tokenization, teacher forcing

## 🔧 Troubleshooting

### Common Issues:

1. **Models not loading**
   - Ensure all model files are in the correct directory
   - Check file permissions and sizes
   - Verify Python dependencies are installed

2. **CORS errors**
   - Backend includes CORS support for frontend communication
   - Ensure backend is running on `http://localhost:5000`

3. **Image upload fails**
   - Check file size (max 10MB)
   - Ensure file is a valid image format
   - Verify backend `/uploads` directory exists

4. **Frontend won't connect to backend**
   - Update `API_BASE_URL` in `Chatbot.js` if backend runs on different port
   - Check that both servers are running

## 💡 Future Enhancements

- [ ] Add more food categories and classes
- [ ] Implement user authentication
- [ ] Add conversation history storage
- [ ] Deploy to cloud platforms
- [ ] Add more sophisticated NLP models (BERT, GPT)
- [ ] Implement real-time notifications
- [ ] Add multilingual support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍🎓 Author
Kottu Saikumar

📧 Email: kottusaikumar2003@gmail.com

📞 Phone: +91 6304830339

📍 Location: Hyderabad, Telangana

🎓 B.Tech in Electronics and Communication Engineering (2020–2024)

🏫 University College of Engineering, JNTUK

💡 Areas of Interest: Data Science, Deep Learning, NLP, Computer Vision

**Kottu Sai Kumar**  
- GitHub: [@kottusaikumar](https://github.com/kottusaikumar/AI-Chatbot-Project-Intelligent-Food-Spoilage-Detector-CNN-NLP-)  
- LinkedIn: [Kottu.SaiKumar](https://www.linkedin.com/in/sai-kumar-10541b269)  

---

### 🌟 If you found this project helpful, please give it a star! ⭐

## 📸 Screenshots

<img width="807" height="921" alt="image" src="https://github.com/user-attachments/assets/7cdded42-548d-4026-8fed-c51b1ff022d1" />


