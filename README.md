# AI Chat Assistant

A versatile chat application built with Streamlit that provides unified access to multiple Language Model providers (OpenAI, Anthropic, and DeepSeek) through liteLLM integration.

## Features

- **Unified LLM Integration**: Seamlessly interact with multiple AI models:
  - OpenAI (o1-mini)
  - Anthropic (claude-3-5-sonnet-latest)
  - DeepSeek (deepseek-chat)

- **Rich Content Support**:
  - Code block rendering with syntax highlighting
  - LaTeX mathematical expression support
  - Markdown formatting

- **Conversation Management**:
  - Save and load conversations
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

3. Configure environment variables:
   Create a `.env` file in the project root with your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   DEEPSEEK_API_KEY=your_deepseek_api_key
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Architecture

### Model Management
The application uses liteLLM to provide a unified interface for different LLM providers. This abstraction layer allows for:
- Consistent API interface across providers
- Easy addition of new model providers
- Unified error handling

### Conversation Handling
- Conversations are stored as JSON files in the `conversations` directory
- Each conversation includes:
  - Message history
  - Code blocks
  - LaTeX expressions
  - Timestamp
  - Custom title

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