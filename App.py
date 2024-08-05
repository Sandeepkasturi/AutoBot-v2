import os
import streamlit as st
import requests
import webbrowser
import time
import base64
from google.generativeai import configure, GenerativeModel
from urllib.parse import urlparse
from streamlit_lottie import st_lottie
from together import Together

# Configure the Generative AI and Together clients
configure(api_key=os.environ.get("GEN_API"))
model = GenerativeModel('gemini-pro')
together_api_key = os.environ.get("TOGETHER_API_KEY")
client = Together(api_key=together_api_key)


# Lottie animation loader
def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()


# Function to download HTML code
def download_html_code(html_content, url):
    try:
        domain = urlparse(url).netloc.replace('www.', '')
        filename = f"{domain}_code.html"
        with open(filename, 'w') as file:
            file.write(html_content)
        st.markdown(get_binary_file_downloader_html(filename), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to download HTML code: {e}")


# Function to redirect to GitHub Codespaces
def redirect_to_codespaces():
    with st.spinner("Redirecting to GitHub Codespaces..."):
        time.sleep(2)
    webbrowser.open_new_tab("https://github.com/codespaces")
    st.info("If the application can't redirect, use the link below:")
    st.markdown("[GitHub Codespaces](https://github.com/codespaces)")


# Function to download generated code
def download_generated_code(content, filename, format='txt'):
    extension = format
    temp_filename = f"{filename}.{extension}"
    with open(temp_filename, 'w') as file:
        file.write(content)
    with open(temp_filename, 'rb') as file:
        data = file.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/{format};base64,{b64}" download="{filename}.{format}">Download Code ({format.upper()})</a>'
    st.markdown(href, unsafe_allow_html=True)
    os.remove(temp_filename)


# Function to display file download link
def get_binary_file_downloader_html(bin_file, file_label='Download Code'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/html;base64,{b64}" download="{bin_file}" target="_blank">{file_label}</a>'
    return href


# Function to display footer
def display_footer():
    footer_html = """
    <style>
    .footer {
        padding: 10px;
        background-color: #f8f9fa;
        text-align: center;
        border-top: 1px solid #e1e1e1;
        font-family: 'Arial', sans-serif;
        color: #6c757d;
    }
    </style>
    <body>
        <script src="//code.tidio.co/pwcadzxfjcnszjctpvlutoucjowgrrrw.js" async></script>
        </body>
    <div class="footer">
        <p><b>&copy; 2024 SKAV TECH. All rights reserved. | Follow us on <a href="https://bit.ly/socialinstag">Instagram</a></b></p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)


# Function to fetch YouTube video suggestions
def fetch_youtube_videos(query):
    api_key = os.environ.get("YOUTUBE_API_KEY")
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 4,
        "key": api_key
    }
    response = requests.get(search_url, params=params)
    video_details = []
    if response.status_code == 200:
        results = response.json()["items"]
        for item in results:
            video_id = item["id"]["videoId"]
            video_title = item["snippet"]["title"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_details.append({
                "title": video_title,
                "url": video_url,
                "video_id": video_id
            })
    else:
        st.error(f"Failed to fetch YouTube videos. Status code: {response.status_code}")
    return video_details


# Function to extract the main topic from the prompt
def extract_topic(prompt):
    start_phrases = ["@codex", "codex", "@autobot"]
    for phrase in start_phrases:
        if prompt.lower().startswith(phrase):
            return prompt[len(phrase):].strip()
    return prompt.strip()


# Main Streamlit application
def main():
    st.set_page_config(page_title="AutoBot AI", page_icon="💀", layout="wide", initial_sidebar_state="expanded")

    st.sidebar.image("autobot2.png", use_column_width=True)
    page = st.sidebar.selectbox("**MENU**",
                                ["🏠 Home", "AutoBot 💀", "CODEX ⚡", "Web Scrapper 🌐", "GitHub Codespaces 🖥️",
                                 "Mega Bot 🐸", "Refund & Privacy Policy 💸", ])

    st.sidebar.title("Support Us")
    st.sidebar.info("Your support helps us improve AutoBot AI.")
    st.sidebar.markdown("""
        <p>Donate for Knowledge, We will be doing this again ❤️</p>
        <a href="https://ibb.co/nBtGVnk"><img src="https://i.ibb.co/0Kv7WFJ/Google-Pay-QR.png" width="50"></a>
    """, unsafe_allow_html=True)

    if page == "🏠 Home":
        st.title("Welcome to AutoBot AI 💀")
        st.markdown("""
        **AutoBot AI**:
        **Functionalities:**
        1. AI Chatbot
        2. CODEX
        3. Web Scrapper
        4. GitHub Codespaces

        AutoBot, powered by the Gemini API, is a basic chatbot designed for automation. It excels in writing code and generating downloadable files with a .txt extension, offering the ability to handle up to 60 queries per minute.

        Developed by SKAV TECH, a company focused on creating practical AI projects, AutoBot is intended for educational purposes only. We do not endorse any illegal or unethical activities.
        """)

        # Embedding Lottie animation
        st.markdown("""
        <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <lottie-player src="https://lottie.host/ee1e5978-9014-47cb-8031-45874d2dc909/tXASIvRMrN.json" background="#FFFFFF" speed="1" style="width: 300px; height: 300px" loop controls autoplay direction="1" mode="normal"></lottie-player>
        """, unsafe_allow_html=True)

        st.video("https://youtu.be/i0Q-NBrYpPI", start_time=0)
        display_footer()

    elif page == "AutoBot 💀":
        st.image("autobot2.png")
        st.header("AutoBot 💀")
        st.markdown(
            "AutoBot is effective for code generation. If your prompt contains code generation **-prompt-**, you can get downloadable files.")

        question = st.text_input("Ask the model a question:")

        if st.button("Ask AI"):

            lottie_url = "https://lottie.host/fb24aa71-e6dd-497e-8a6c-3098cb64b1ed/V9N1Sd3klS.json"

            # Load and display Lottie animation
            lottie_animation = load_lottie_url(lottie_url)
            if lottie_animation:
                st_lottie(lottie_animation, speed=27, width=150, height=100, key="lottie_animation")
            else:
                st.error("Failed to load Lottie animation.")
            with st.spinner("Generating response 💀..."):
                try:
                    response = model.generate_content(question)
                    if response.text:
                        st.text("AutoBot Response:")
                        st.write(response.text)
                        st.markdown('---')
                        st.markdown(
                            "Security Note: We use **.txt** file format for code downloads, which is not easily susceptible to virus and malware attacks.")
                    else:
                        st.error("No valid response received from the AI model.")
                        st.write(f"Safety ratings: {response.safety_ratings}")
                except ValueError as e:
                    st.info(f"Unable to assist with that prompt due to: {e}")
                except IndexError as e:
                    st.info(f"Unable to assist with that prompt due to: {e}")
                except Exception as e:
                    st.info(f"An unexpected error occurred: {e}")

                code_keywords = ["code", "write code", "develop code", "generate code", "generate", "build"]
                if any(keyword in question.lower() for keyword in code_keywords):
                    st.text("Download the generated code 💀:")
                    download_generated_code(response.text, "code", format='txt')

        display_footer()

    elif page == "CODEX ⚡":
        st.header("CODEX ⚡")
        st.markdown("Upload a Python script (.py) to download the HTML code generated by CODEX.")
        uploaded_file = st.file_uploader("Choose a file", type=["py"])
        if uploaded_file is not None:
            file_content = uploaded_file.read().decode("utf-8")
            with st.spinner("Generating HTML code..."):
                response = client.translate(script=file_content, target_language="HTML")
                st.code(response.text)
                download_html_code(response.text, uploaded_file.name)
        display_footer()

    elif page == "Web Scrapper 🌐":
        st.header("Web Scrapper 🌐")
        url = st.text_input("Enter the website URL:")
        if st.button("Scrape"):
            with st.spinner("Scraping the website..."):
                response = client.scrape(url)
                st.code(response.text)
                download_html_code(response.text, url)
        display_footer()

    elif page == "GitHub Codespaces 🖥️":
        st.header("GitHub Codespaces 🖥️")
        st.markdown("Redirect to GitHub Codespaces for code editing and collaboration.")
        if st.button("Go to GitHub Codespaces"):
            redirect_to_codespaces()
        display_footer()

    elif page == "Mega Bot 🐸":
        st.image("megabot.png")
        st.markdown('---')
        st.subheader("🤖 Multi-model AI Application")
        st.markdown(
            "This application integrates multiple AI models and tools for various functionalities such as chat, code generation, image generation.")

        # Tabs for navigation
        tabs = st.tabs(["General Chat", "Code Generation", "Image Generation"])
        # Load animations
        chat_animation = load_lottie_url("https://assets2.lottiefiles.com/private_files/lf30_xTmPwn.json")
        code_animation = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_ba55esn2.json")
        image_animation = load_lottie_url("https://assets2.lottiefiles.com/private_files/lf30_O5QGL0.json")

        # General Chat Tab
        with tabs[0]:
            st.header("💬 General Chat")
            user_prompt = st.text_input("Enter your prompt:", "")
            if st.button("Generate Response"):
                with st.spinner("Generating response..."):
                    response = model.generate_content(user_prompt)
                    st.markdown('---')
                    st.write(response.text)
                    st.markdown('---')
            st.sidebar.write("""
                **General Chat Instructions:**
                1. Enter your prompt in the text box.
                2. Click on the 'Generate Response' button to see the AI's response.
            """)

        # Code Generation Tab
        with tabs[1]:
            st.header("💻 Code Generation")
            user_prompt = st.text_input("Enter your coding prompt:", "")
            if st.button("Generate Code"):
                with st.spinner("Generating code..."):
                    response = client.chat.completions.create(
                        model="codellama/CodeLlama-70b-Instruct-hf",
                        messages=[{"role": "user", "content": user_prompt}],
                    )
                    st.code(response.choices[0].message.content, language="python")
            st.sidebar.write("""
                **Code Generation Instructions:**
                1. Enter your coding prompt in the text box.
                2. Click on the 'Generate Code' button to see the generated code.
            """)

        # Image Generation Tab
        with tabs[2]:
            st.header("🖼️ Image Generation")
            st.markdown('---')
            st.info(
                "We are currently working on Tuning the Models, So the AI generated images might not match your prompts. Improve your Prompt Context to get good results 😊")
            st.markdown('---')
            user_prompt = st.text_input("Enter your image prompt:", "")
            model_choice = st.selectbox("Choose the image model", [
                "SG161222/Realistic_Vision_V3.0_VAE",
                "stabilityai/stable-diffusion-2-1",
                "runwayml/stable-diffusion-v1-5",
                "prompthero/openjourney"
            ])
            if st.button("Generate Image"):
                with st.spinner("Generating image..."):
                    response = client.images.generate(
                        prompt=user_prompt,
                        model=model_choice,
                        steps=10,
                        n=1
                    )
                    img_data = response.data[0].b64_json
                    img_bytes = base64.b64decode(img_data)
                    st.image(img_bytes)
            st.sidebar.write("""
                **Image Generation Instructions:**
                1. Enter your image prompt in the text box.
                2. Choose an image generation model from the dropdown.
                3. Click on the 'Generate Image' button to see the generated image.
            """)

        # Run the app with: streamlit run app.py

        display_footer()

    elif page == "Refund & Privacy Policy 💸":
        st.image("autobot2.png")
        st.header("Refund & Privacy Policy 💸")
        st.markdown(
            """
            ## Refund Policy
            We want you to be satisfied with our services. If you have any issues or concerns, please contact us within 30 days of purchase. We will review your request and provide a refund if deemed appropriate.

            ## Privacy Policy
            Your privacy is important to us. We collect only the necessary data to provide our services and do not share your information with third parties without your consent. Please review our [full privacy policy](https://www.example.com/privacy-policy) for more details.
            """
        )

        display_footer()
        # Add Razorpay donation button to the sidebar
      st.sidebar.markdown("### Support Us")
      st.sidebar.markdown("If you find this tool useful, please consider supporting us by making a donation.")
      components.html(
        """
        <form>
            <script src="https://checkout.razorpay.com/v1/payment-button.js" data-payment_button_id="pl_Oe7PyEQO3xI82m" async> </script>
        </form>
        """,
        height=450,
        width=300
    )


if __name__ == "__main__":
    main()
