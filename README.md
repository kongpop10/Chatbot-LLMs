# Grok Chat Application

A Streamlit-based chat application that interfaces with xAI's Grok model, featuring a ChatGPT-like interface with additional capabilities for handling code and LaTeX expressions.

## Features

- 💬 Interactive chat interface with Grok AI
- 📝 Support for code syntax highlighting and LaTeX rendering
- 💾 Automatic conversation saving
- 📂 Conversation management (load, edit, delete)
- 🔍 Code block detection and formatting
- ➗ LaTeX mathematical expression support

## Prerequisites

- Python 3.8 or higher
- Streamlit
- xAI API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd grok-chat
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Set up your xAI API key:
   - Create a `.streamlit` folder in the project root
   - Create a `secrets.toml` file inside the `.streamlit` folder
   - Add your API key:
   ```toml
   XAI_API_KEY = "your-api-key-here"
   ```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided URL (typically `http://localhost:8501`)

3. Start chatting with Grok!

## Features in Detail

### Code Handling
- Automatically detects code blocks in messages
- Provides syntax highlighting
- Supports multiple programming languages
- Includes line numbers for better reference

### LaTeX Support
- Renders mathematical expressions using LaTeX
- Supports inline LaTeX expressions enclosed in single `$` symbols

### Conversation Management
- Automatically saves conversations
- Load previous conversations
- Edit conversation titles
- Delete unwanted conversations

## File Structure
```
grok-chat/
├── .streamlit/
│   └── secrets.toml
├── conversations/
├── .gitignore
├── README.md
├── requirements.txt
└── app.py
```

## Security Notes

- Never commit your `.streamlit/secrets.toml` file
- Keep your API key confidential
- The `conversations` directory contains chat history - handle with appropriate privacy considerations

## Contributing

Feel free to submit issues and enhancement requests!

## License

[MIT License](LICENSE)