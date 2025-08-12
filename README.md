# Dedicated.ai - Intelligent Conversational AI Assistant

![Dedicated.ai](https://img.shields.io/badge/Dedicated.ai-AI%20Assistant-red)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## 🎥 Demo Video
[![Watch Demo](https://img.shields.io/badge/Watch%20Demo-YouTube-red)](https://youtu.be/kYPZX0Y22mU)

## Overview

Dedicated.ai is an intelligent conversational AI assistant designed to provide structured and thoughtful responses to user queries. The application serves as a research-oriented chatbot that not only answers questions but also shows its reasoning process, making it transparent and educational for users who want to understand how the AI arrives at its conclusions.

## Features

- **Structured AI Responses**: Each response includes reasoning, answer, and auto-generated title
- **Persistent Chat History**: All conversations saved across sessions using SQLite
- **Multiple Thread Management**: Handle multiple conversations simultaneously
- **Transparent AI Reasoning**: Shows the thought process behind each response
- **Clean User Interface**: Modern Streamlit-based web interface
- **Automatic Conversation Titling**: AI-generated titles for easy conversation identification

## Tech Stack

- **Frontend**: Streamlit
- **AI Framework**: LangChain, LangGraph
- **Language Model**: ChatGroq (Llama 3.3 70B)
- **Database**: SQLite
- **Backend**: Python 3.8+

## Project Structure

```
dedicated-ai/
│
├── project_backend.py      # Backend logic and AI model integration
├── project_frontend.py     # Streamlit frontend application
├── footer.py              # Footer component for UI
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── chating3.db           # SQLite database (auto-created)
```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/dedicated-ai.git
   cd dedicated-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Get your Groq API key from [Groq Console](https://console.groq.com/)
   - Replace the API key in `project_backend.py` or use environment variables

4. **Run the application**
   ```bash
   streamlit run project_frontend.py
   ```

## Requirements

Create a `requirements.txt` file with the following dependencies:

```txt
streamlit>=1.28.0
langchain-groq>=0.1.0
langgraph>=0.1.0
langchain-core>=0.2.0
pydantic>=2.0.0
sqlite3
uuid
htbuilder
```

## Configuration

### API Key Setup
Replace the API key in `project_backend.py`:
```python
model = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key="your-groq-api-key-here",
    temperature=0.5
)
```

### Database Configuration
The SQLite database `chating3.db` is automatically created on first run. No manual setup required.

## Usage

1. Start the application using `streamlit run project_frontend.py`
2. Open your browser and navigate to the provided local URL
3. Start chatting with the AI assistant
4. View reasoning process in the expandable sections
5. Switch between conversations using the sidebar
6. Create new chats anytime with the "New Chat" button

## How It Works

1. **User Input**: User types a message in the chat interface
2. **AI Processing**: The system processes input through ChatGroq using structured output
3. **Response Generation**: AI generates structured response with reasoning, answer, and title
4. **Data Storage**: Conversation history is saved to SQLite database
5. **Display**: Response shown with expandable reasoning and answer sections

## Key Components

### Backend (project_backend.py)
- **StructuredResponse**: Pydantic model for structured AI outputs
- **ChatState**: TypedDict for managing conversation state
- **chat()**: Main function for AI interaction
- **retrive_history()**: Function to fetch conversation history
- **retrive_all_threads()**: Function to get all conversation threads

### Frontend (project_frontend.py)
- **Streamlit Interface**: Modern web UI for chat interaction
- **Session Management**: Handles multiple conversation threads
- **Message Display**: Shows chat history with expandable sections
- **Navigation**: Sidebar for switching between conversations

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Future Enhancements

- [ ] User authentication system
- [ ] Export chat conversations
- [ ] Multiple AI model support
- [ ] Advanced search in chat history
- [ ] Custom AI prompts
- [ ] Dark/Light theme toggle

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

**Pritiyax Shukla**
- LinkedIn: [Pritiyax Shukla](https://www.linkedin.com/in/pritiyax-shukla-0646982b3/)
- YouTube Demo: [Watch Here](https://youtu.be/kYPZX0Y22mU)

## Acknowledgments

- Built with LangChain and LangGraph frameworks
- Powered by Groq's high-performance AI inference
- UI created with Streamlit framework

---

⭐ If you found this project helpful, please give it a star!
