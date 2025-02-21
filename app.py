import streamlit as st
import re
import json
from datetime import datetime
import os
from dotenv import load_dotenv
from litellm import completion

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖", layout="wide")

# Ensure the conversations directory exists
if not os.path.exists("conversations"):
    os.makedirs("conversations")

def save_conversation():
    if len(st.session_state.messages) > 1:
        # Generate a unique ID for the conversation if it doesn't exist
        if "current_conversation_id" not in st.session_state:
            st.session_state.current_conversation_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Take the first user message as the title, limited to 30 chars
        title = next((msg["content"][:30] + "..." for msg in st.session_state.messages 
                     if msg["role"] == "user"), st.session_state.current_conversation_id)
        
        conversation_data = {
            "messages": st.session_state.messages,
            "code_blocks": st.session_state.code_blocks,
            "latex_blocks": st.session_state.latex_blocks,
            "timestamp": st.session_state.current_conversation_id,
            "title": title
        }
        
        filename = f"conversations/conversation_{st.session_state.current_conversation_id}.json"
        with open(filename, "w") as f:
            json.dump(conversation_data, f)
        
        return filename

def load_conversation(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    st.session_state.messages = data["messages"]
    st.session_state.code_blocks = data["code_blocks"]
    st.session_state.latex_blocks = data["latex_blocks"]
    # Set the current conversation ID to prevent duplicate saves
    st.session_state.current_conversation_id = data["timestamp"]

def delete_conversation(filename):
    try:
        os.remove(f"conversations/{filename}")
        # Clear the current conversation ID if we're deleting the active conversation
        if ("current_conversation_id" in st.session_state and 
            f"conversation_{st.session_state.current_conversation_id}.json" == filename):
            del st.session_state.current_conversation_id
        return True
    except Exception as e:
        st.error(f"Error deleting conversation: {str(e)}")
        return False

def get_saved_conversations():
    if not os.path.exists("conversations"):
        return []
    files = os.listdir("conversations")
    conversations = []
    for file in files:
        if file.endswith(".json"):
            with open(f"conversations/{file}", "r") as f:
                data = json.load(f)
                conversations.append({
                    "filename": file,
                    "title": data.get("title", file),
                    "timestamp": data.get("timestamp", "")
                })
    return sorted(conversations, key=lambda x: x["timestamp"], reverse=True)

def update_conversation_title(filename, new_title):
    try:
        filepath = f"conversations/{filename}"
        with open(filepath, "r") as f:
            data = json.load(f)
        
        # Update the title
        data["title"] = new_title
        
        # Save the updated data
        with open(filepath, "w") as f:
            json.dump(data, f)
        return True
    except Exception as e:
        st.error(f"Error updating title: {str(e)}")
        return False

def process_message_content(content):
    # Process code blocks (```language\ncode```)
    code_pattern = r'```(\w+)?\n(.*?)```'
    code_blocks = re.finditer(code_pattern, content, re.DOTALL)
    processed_content = content

    for match in code_blocks:
        language = match.group(1) or "python"
        code = match.group(2)
        # Replace the code block with a special marker
        marker = f"__CODE_BLOCK_{id(code)}__"
        processed_content = processed_content.replace(match.group(0), marker)
        # Store the code block for later rendering
        st.session_state.code_blocks[marker] = (code.strip(), language)

    # Process inline LaTeX ($...$)
    latex_pattern = r'\$(.*?)\$'
    latex_blocks = re.finditer(latex_pattern, processed_content)
    
    for match in latex_blocks:
        latex = match.group(1)
        marker = f"__LATEX_BLOCK_{id(latex)}__"
        processed_content = processed_content.replace(match.group(0), marker)
        st.session_state.latex_blocks[marker] = latex

    return processed_content

def render_message(content):
    # Split content and render each part
    parts = content.split('__')
    
    for part in parts:
        if part.startswith('CODE_BLOCK_'):
            code, language = st.session_state.code_blocks[f"__{part}__"]
            st.code(code, language=language, line_numbers=True)
        elif part.startswith('LATEX_BLOCK_'):
            latex = st.session_state.latex_blocks[f"__{part}__"]
            st.latex(latex)
        elif part:  # Regular text
            st.markdown(part)

# Define model names as variables
MODEL_NAMES = {
    "OpenAI": "openai/o1-mini",
    "Anthropic": "anthropic/claude-3-5-sonnet-latest",
    "DeepSeek": "deepseek/deepseek-chat"
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful AI assistant. When showing code examples, use markdown code blocks with language specification. For mathematical expressions, use LaTeX notation enclosed in single $ symbols."}
    ]
if "code_blocks" not in st.session_state:
    st.session_state.code_blocks = {}
if "latex_blocks" not in st.session_state:
    st.session_state.latex_blocks = {}

# Sidebar for conversation management
with st.sidebar:
    st.title("💬 Conversations")
    
    # Update model selector to include all providers
    model_provider = st.selectbox(
        "Select Model Provider",
        ["OpenAI", "Anthropic", "DeepSeek"],
        help="Choose between OpenAI, Anthropic, and DeepSeek models"
    )
    
    # New conversation button
    if st.button("New Conversation"):
        st.session_state.messages = [st.session_state.messages[0]]
        st.session_state.code_blocks = {}
        st.session_state.latex_blocks = {}
        if "current_conversation_id" in st.session_state:
            del st.session_state.current_conversation_id
        st.rerun()
    
    # Display saved conversations
    st.subheader("Saved Conversations")
    conversations = get_saved_conversations()
    
    # Initialize session state for editing titles if not exists
    if "editing_title" not in st.session_state:
        st.session_state.editing_title = None
    
    for conv in conversations:
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            # Show either edit input or conversation title
            if st.session_state.editing_title == conv['filename']:
                # Edit mode
                new_title = st.text_input(
                    "Edit title",
                    value=conv['title'],
                    key=f"edit_{conv['filename']}",
                    label_visibility="collapsed"
                )
                if new_title != conv['title']:
                    if update_conversation_title(conv['filename'], new_title):
                        st.session_state.editing_title = None
                        st.rerun()
            else:
                # Display mode
                if st.button(f"📜 {conv['title']}", key=f"load_{conv['filename']}"):
                    load_conversation(f"conversations/{conv['filename']}")
                    st.rerun()
        
        with col2:
            # Edit/Save button
            if st.session_state.editing_title == conv['filename']:
                if st.button("💾", key=f"save_{conv['filename']}"):
                    st.session_state.editing_title = None
                    st.rerun()
            else:
                if st.button("✏️", key=f"edit_{conv['filename']}"):
                    st.session_state.editing_title = conv['filename']
                    st.rerun()
        
        with col3:
            # Delete button
            if st.button("🗑️", key=f"delete_{conv['filename']}"):
                if delete_conversation(conv['filename']):
                    if st.session_state.editing_title == conv['filename']:
                        st.session_state.editing_title = None
                    st.rerun()

# Main chat interface
if model_provider == "DeepSeek":
    st.title("🤖 DeepSeek Chat")
    st.markdown(f"Chat with {MODEL_NAMES['DeepSeek']}, powered by DeepSeek")
elif model_provider == "OpenAI":
    st.title("🤖 OpenAI Chat")
    st.markdown(f"Chat with {MODEL_NAMES['OpenAI']}, powered by OpenAI")
else:  # Anthropic
    st.title("🤖 Claude Chat")
    st.markdown(f"Chat with {MODEL_NAMES['Anthropic']}, powered by Anthropic")

# Display chat messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            render_message(process_message_content(message["content"]))

# Chat input
if prompt := st.chat_input("What's on your mind?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # Configure model and API key based on provider
            model = MODEL_NAMES[model_provider]
            api_key = os.getenv(f"{model_provider.upper()}_API_KEY")
            
            # Use liteLLM for all model providers
            completion_response = completion(
                model=model,
                messages=st.session_state.messages,
                api_key=api_key
            )
            
            response = completion_response.choices[0].message.content
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Save conversation and rerun if this is the first message
            saved_file = save_conversation()
            if len(st.session_state.messages) == 3:  # System message + first user message + first AI response
                st.rerun()
            
            # Process and display the response
            processed_response = process_message_content(response)
            render_message(processed_response)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
