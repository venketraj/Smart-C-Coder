import streamlit as st
import requests
import os

st.set_page_config(page_title="C Code Rewriter with Guidelines", page_icon="🎨")

# UI styling
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

# File uploaders
code_file = st.file_uploader("Upload your C code file (.c)", type=["c"])
guideline_file = st.file_uploader("Upload guideline text file (.txt)", type=["txt"])

def parse_response(response_text):
    # Try separating code and explanation by looking for keywords
    split_phrases = ["Explanation:", "Explanation of Changes", "Provide the improved code and a clear explanation of the changes."]
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

if code_file and guideline_file:
    c_code = code_file.read().decode("utf-8")
    guidelines = guideline_file.read().decode("utf-8")
    
    if st.button("Rewrite Code with Guidelines"):
        with st.spinner("Sending request to Codestral API..."):
            result = call_codestral_api(c_code, guidelines)
            if result and not result.startswith("Error:"):
                code_part, explanation_part = parse_response(result)
                
                st.subheader("🎉 Improved C Code")
                st.code(code_part, language="c")

                st.subheader("💡 Explanation of Changes")
                st.markdown(explanation_part)

                st.subheader("🌟 Recommendations to Improve Your Project")
                st.markdown("""
                - 🖌️ **Use `st.code` for color syntax highlighting in Streamlit.**
                - 📝 **Format explanations with bullet points and bold text for clarity.**
                - 🔍 **Add original vs improved code diffs interactively.**
                - ⚠️ **Provide user-friendly error handling in UI.**
                - 💾 **Add download button for improved code file.**
                - 📚 **Offer pre-built guideline templates for common coding practices.**
                - 🕒 **Implement revision history with timestamps.**
                - ⭐ **Enable user feedback/rating on code improvements.**
                """)
            else:
                st.error(result)
else:
    st.info("Please upload both your C code and the guideline files to proceed.")
