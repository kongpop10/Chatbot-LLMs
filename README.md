# AI Chat Application

A Streamlit-based chat application that allows you to interact with multiple AI models.

## Features

- 🤖 Support for multiple AI models:
  - xAI's Grok-Beta
  - OpenAI's GPT-4 Turbo Preview
  - Anthropic's Claude 3 Sonnet
- 💬 Conversation Management:
  - Save conversations automatically
  - Load previous conversations
  - Delete unwanted conversations
  - Edit conversation titles
- 📝 Rich Text Support:
  - Code blocks with syntax highlighting
  - LaTeX mathematical expressions
- 🎨 Clean and intuitive user interface
- 🔄 Real-time model switching via sidebar

## Setup

1. Clone the repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.streamlit/secrets.toml` file with your API keys:
```toml
XAI_API_KEY = "your-xai-api-key"
OPENAI_API_KEY = "your-openai-api-key"
ANTHROPIC_API_KEY = "your-anthropic-api-key"
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided URL (typically `http://localhost:8501`)

3. Select your preferred model:
   - Choose between xAI (Grok-Beta), OpenAI (GPT-4 Turbo), or Anthropic (Claude 3 Sonnet) from the sidebar dropdown
   - The interface will update to reflect your chosen model

4. Start chatting:
   - Type your message in the chat input
   - View AI responses with support for code and LaTeX rendering
   - Conversations are automatically saved

## Features in Detail

### Model Selection
- Switch between models in real-time using the sidebar dropdown
- Each model has its own unique capabilities:
  - Grok-Beta: xAI's latest model
  - GPT-4 Turbo Preview: OpenAI's advanced model
  - Claude 3 Sonnet: Anthropic's latest model

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
ai-chat/
├── .streamlit/
│   └── secrets.toml
├── conversations/
├── .gitignore
├── README.md
├── requirements.txt
└── app.py
```

## Requirements

- Python 3.7+
- Streamlit >= 1.31.0
- OpenAI >= 1.0.0
- Python-dotenv >= 1.0.0
- Anthropic >= 0.7.0

## Security Notes

- Never commit your `.streamlit/secrets.toml` file
- Keep your API keys confidential
- The `conversations` directory contains chat history - handle with appropriate privacy considerations

## Contributing

Feel free to submit issues and enhancement requests!

## License

[MIT License](LICENSE)