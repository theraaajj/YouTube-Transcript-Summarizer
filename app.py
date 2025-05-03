import streamlit as st
from dotenv import load_dotenv
load_dotenv()  # Load all environment variables
import os
import google.generativeai as genai
import re  # Importing regex module for improved video ID extraction
from youtube_transcript_api import YouTubeTranscriptApi

# Configure the Gemini API key
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Prompt for summarizing video content
prompt = """You are a YouTube Video Summarizer. You will take the transcripts of the video and summarize the entire video and provide the important summary in points within 500 words. The transcript text is: """

# Function to extract video ID from various YouTube link formats
def extract_video_id(video_url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, video_url)
    return match.group(1) if match else None

# Function to fetch video transcript
def extract_details(video_url):
    try:
        video_id = extract_video_id(video_url)  # Extracting video ID using regex
        if not video_id:
            raise ValueError("Invalid YouTube URL")

        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)  # Retrieve transcripts

        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript
    except Exception as e:
        raise e

# Function to generate content using the Gemini model
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")  # Gemini model selection
    response = model.generate_content(prompt + transcript_text)
    return response.text if hasattr(response, 'text') else response

# Streamlit App UI
st.title("YouTube Video Summarizer")
video_link = st.text_input("Enter the link to a YouTube video: ")

if video_link:
    video_id = extract_video_id(video_link)  # Extract video ID from link
    if video_id:
        st.image(f'http://img.youtube.com/vi/{video_id}/0.jpg', use_container_width=True)

if st.button("Get Detailed Notes"):
    transcripts = extract_details(video_link)

    if transcripts:
        summary = generate_gemini_content(transcripts, prompt)
        st.markdown("## Detailed Notes: ")
        st.write(summary)
