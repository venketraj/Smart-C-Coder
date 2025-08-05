import streamlit as st
import requests
import os
from datetime import datetime

st.set_page_config(page_title="C Code Rewriter with Guidelines", page_icon="🎨")

# UI styling remains same as before
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #333333;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    .title {
        color: #ff4b1f;
        font-weight: 900;
        font-size: 3.5rem;
        text-align: center;
        margin-bottom: 0.25rem;
        text-shadow: 2px 2px #f9d423;
    }
    .subtitle {
        color: #1f4037;
        font-weight: 700;
        font-size: 1.25rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .stFileUploader>label {
        font-weight: 800;
        color: #ff4b1f;
    }
    .response-box {
        background: #dff6f0;
        border-radius: 15px;
        padding: 15px 20px;
        font-family: 'Courier New', monospace;
        font-size: 1rem;
        white-space: pre-wrap;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    .recommendations li {
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="title">🎨 C Code Rewriter with Guidelines</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload your C code and Guidelines to transform your code with style!</div>', unsafe_allow_html=True)

# Pre-built guidelines templates
guideline_templates = {
    "Select a guideline template": "",
    "Fix Off-By-One Errors": (
        "1. Fix off-by-one errors in loops when indexing arrays.\n"
        "2. Declare loop variables inside loops.\n"
        "3. Add detailed comments explaining logic.\n"
        "4. Follow consistent indentation and brace style."
    ),
    "Memory Safety and Pointer Use": (
        "1. Check for null pointers before dereferencing.\n"
        "2. Use meaningful variable names.\n"
        "3. Avoid magic numbers; use constants.\n"
        "4. Add comments about pointer usage and memory management."
    ),
    "Code Readability and Style": (
        "1. Use consistent indentation and spacing.\n"
        "2. Add descriptive comments for functions and complex logic.\n"
        "3. Avoid nested control structures when possible.\n"
        "4. Declare variables close to their use."
    ),
}

code_file = st.file_uploader("Upload your C code file (.c)", type=["c"])
guideline_file = st.file_uploader("Upload guideline text file (.txt)", type=["txt"])

selected_template = st.selectbox("Or choose a guideline template to auto-fill guidelines", list(guideline_templates.keys()))
if selected_template != "Select a guideline template" and not guideline_file:
    guidelines = guideline_templates[selected_template]
else:
    guidelines = None

def parse_response(response_text):
    split_phrases = [
        "Explanation:",
        "Explanation of Changes",
        "Provide the improved code and a clear explanation of the changes."
    ]
    code_part = response_text
    explanation_part = ""
    for phrase in split_phrases:
        if phrase in response_text:
            parts = response_text.split(phrase)
            code_part = parts[0].strip()
            explanation_part = parts[1].strip()
            break
    return code_part, explanation_part

def call_codestral_api(c_code, guidelines):
    api_key = "LTIT3rxCF0vyjonVc1GQ4KPTozbsOT2D"
    if not api_key:
        st.error("MISTRAL_API_KEY environment variable not set.")
        return None
    url = "https://codestral.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    system_msg = (
        "You are a helpful assistant that rewrites C code strictly following given guidelines "
        "and explains what was improved."
    )
    user_msg = (
        "Here is the C code:\n\n"
        f"{c_code}\n\n"
        "Please modify it according to these guidelines:\n\n"
        f"{guidelines}\n\n"
        "Provide the improved code and a clear explanation of the changes."
    )
    payload = {
        "model": "codestral-latest",
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ],
        "max_tokens": 600,
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=payload)
    try:
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}\nResponse: {response.text}"

if code_file and (guideline_file or guidelines):
    c_code = code_file.read().decode("utf-8")
    if guideline_file:
        guidelines = guideline_file.read().decode("utf-8")
    # else guidelines already assigned from selected template or None

    if st.button("Rewrite Code with Guidelines"):
        with st.spinner("Sending request to Codestral API..."):
            result = call_codestral_api(c_code, guidelines)
            if result and not result.startswith("Error:"):
                code_part, explanation_part = parse_response(result)

                st.subheader("🎉 Original Code vs Improved Code")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Original Code**")
                    st.code(c_code, language="c")

                with col2:
                    st.markdown("**Improved Code**")
                    st.code(code_part, language="c")

                st.subheader("💡 Explanation of Changes")
                st.markdown(explanation_part)

                # Download improved code button
                st.download_button(
                    label="💾 Download Improved Code (.c)",
                    data=code_part,
                    file_name="improved_code.c",
                    mime="text/plain"
                )

                # Initialize or update revision history in session state
                if 'revision_history' not in st.session_state:
                    st.session_state['revision_history'] = []

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state['revision_history'].append({
                    "timestamp": timestamp,
                    "original_code": c_code,
                    "improved_code": code_part,
                    "explanation": explanation_part
                })

                # Show revision history
                st.subheader("🕒 Revision History")
                for i, rev in enumerate(reversed(st.session_state['revision_history']), 1):
                    with st.expander(f"Revision {len(st.session_state['revision_history']) - i + 1} - {rev['timestamp']}"):
                        st.markdown("**Improved Code**")
                        st.code(rev['improved_code'], language="c")
                        st.markdown("**Explanation**")
                        st.markdown(rev['explanation'])

                # Feedback system - simple star rating and text input
                st.subheader("⭐ Rate & Feedback")
                rating = st.slider("Rate the quality of the code improvement:", 1, 5, 3)
                feedback = st.text_area("Leave your feedback:")

                if st.button("Submit Feedback"):
                    st.success(f"Thank you for your rating of {rating} stars and your feedback!")
                    # Here you can add code to save feedback externally (e.g., database/file)
                    st.session_state['last_feedback'] = {"rating": rating, "feedback": feedback}

            else:
                st.error(result)
else:
    st.info("Please upload your C code file and either a guideline text file or select a guideline template to proceed.")
