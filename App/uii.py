import streamlit as st
import requests
import time
import json

# Set page config
st.set_page_config(page_title="Podcast Generator", layout="wide")

#
# App title
st.title("🎙️ CAST AI")

# Sidebar for input parameters
with st.sidebar:
    st.header("Settings")
    source_type = st.selectbox("Source Type", ["url", "pdf", "doc"])
    source = st.text_input("Source (URL or file path)")
    analogy = st.text_input("Analogy")
    emphasis = st.text_input("Emphasis")
    style = st.selectbox("Style", ["entertaining", "informative", "academic", "funny"])

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Generate Your Podcast")
    if st.button("Generate"):
        if not source or not analogy or not emphasis:
            st.error("Please fill in all required fields.")
        else:
            with st.spinner("Generating podcast... This may take a few minutes."):
                # API call to generate podcast
                response = requests.post(
                    "http://localhost:8000/generate_podcast",
                    json={
                        "source_type": source_type,
                        "source": source,
                        "analogy": analogy,
                        "emphasis": emphasis,
                        "style": style
                    }
                )
                
                if response.status_code == 200:
                    podcast_id = response.json()["id"]
                    
                    
                    # Poll for podcast status
                    while True:
                        status_response = requests.get(f"http://localhost:8000/podcast_status/{podcast_id}")
                        status = status_response.json()
                        
                        if status["status"] == "completed":
                            st.success("Podcast generated successfully!")
                            st.session_state.podcast_url = status["podcast_url"]
                            break
                        elif status["status"] == "failed":
                            st.error(f"Podcast generation failed: {status['podcast_url']}")
                            break
                        
                        time.sleep(5)
                else:
                    st.error("Failed to start podcast generation. Please try again.")

with col2:
    st.header("Play")
    if 'podcast_url' in st.session_state:
        st.audio(st.session_state.podcast_url)
    else:
        st.info("Generate a podcast to play it here!")

# Additional information
st.markdown("---")
st.subheader("How it works")
st.write("""
1. Enter the source of your content (URL, PDF, or DOC file).
2. Provide an analogy and emphasis to guide the podcast generation.
3. Choose a style for your podcast.
4. Click 'Generate Podcast' and wait for the magic to happen!
5. Once generated, your podcast will appear in the player on the right.
""")

st.markdown("---")
st.caption("Powered by AI - Developed by Lwanga Caleb :)")