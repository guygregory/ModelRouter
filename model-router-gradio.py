import os
import gradio as gr
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

endpoint = os.environ["AZURE_OPENAI_API_ENDPOINT"]
deployment = os.environ["AZURE_OPENAI_API_MODEL"]
subscription_key = os.environ["AZURE_OPENAI_API_KEY"]
api_version = os.environ["AZURE_OPENAI_API_VERSION"]

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

# Function to handle chat responses with streaming
def respond(user_message):
    # prepare single-turn exchange
    user_entry = {"role": "user", "content": user_message}
    assistant_entry = {"role": "assistant", "content": ""}
    history = [user_entry, assistant_entry]
    messages_for_api = [
        {"role": "system", "content": "You are a helpful assistant."},
        user_entry
    ]

    # initial: clear input & disable buttons
    yield history, "", gr.update(value=""), gr.update(interactive=False), gr.update(interactive=False)

    response = client.chat.completions.create(
        model=deployment,
        stream=True,
        messages=messages_for_api,
        max_tokens=8192,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

    model_router_model = None
    for chunk in response:
        if not getattr(chunk, "choices", []) or getattr(chunk.choices[0].delta, "content", None) is None:
            continue
        model_router_model = chunk.model
        assistant_entry["content"] += chunk.choices[0].delta.content or ""

        # stream back updated assistant response
        yield history, model_router_model, gr.update(value=""), gr.update(interactive=False), gr.update(interactive=False)

    # done streaming: re-enable buttons (input stays cleared)
    yield history, model_router_model, gr.update(value=""), gr.update(interactive=True), gr.update(interactive=True)

# Function to clear chat and model info
def clear_history():
    # clear chat, model_info, input; re-enable buttons
    return [], "model-router", "", gr.update(interactive=True), gr.update(interactive=True)  # Clear chatbot, model_info, and input textbox

# Build Gradio interface
with gr.Blocks() as demo:
    # inject MathJax + custom CSS + MathJax re-typeset script
    gr.HTML(
        """
        <script>
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
            },
            svg: {fontCache: 'global'}
        };
        </script>
        <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
        <style>
          /* bump font size and eliminate top margin for model_info */
          #model_info textarea { 
            font-size: 32px !important; 
            margin-top: 0 !important; 
          }
        </style>
        <script>
        // Observe chatbot for changes and re-typeset with MathJax
        function typesetChatbot() {
            if (window.MathJax && window.MathJax.typeset) {
                window.MathJax.typeset();
            }
        }
        function scrollChatbotToBottom() {
            const chatbot = document.querySelector('[data-testid="chatbot"]');
            if (chatbot) {
                chatbot.scrollTop = chatbot.scrollHeight;
            }
        }
        const observer = new MutationObserver(() => {
            typesetChatbot();
            scrollChatbotToBottom();
        });
        window.addEventListener("DOMContentLoaded", function() {
            const chatbot = document.querySelector('[data-testid="chatbot"]');
            if (chatbot) {
                observer.observe(chatbot, { childList: true, subtree: true });
            }
        });
        </script>
        """,
        visible=False
    )

    # Add a center-aligned title above the model used textbox
    gr.HTML(
        '<h2 style="text-align:center; font-size:32px; margin-bottom:0.5em;">Azure OpenAI - Model Router demo</h2>'
    )

    # Add a read-only textbox to display current model, with centered text
    model_info = gr.Textbox(
        label="Model used:",
        interactive=False,
        value="model-router",
        elem_id="model_info"
    )

    chatbot    = gr.Chatbot(label="Assistant", height=400, type="messages")
    txt        = gr.Textbox(show_label=False, placeholder="Type your message…", lines=1)

    with gr.Row():
        submit_btn = gr.Button("Submit")
        clear_btn  = gr.Button("Clear")

    # Now outputs is a list: [chatbot, model_info]
    submit_btn.click(
        fn=respond,
        inputs=[txt],
        outputs=[chatbot, model_info, txt, submit_btn, clear_btn],
    )
    txt.submit(
        fn=respond,
        inputs=[txt],
        outputs=[chatbot, model_info, txt, submit_btn, clear_btn],
    )
    clear_btn.click(
        fn=clear_history,
        inputs=None,
        outputs=[chatbot, model_info, txt, submit_btn, clear_btn],
    )

if __name__ == "__main__":
    demo.launch()
