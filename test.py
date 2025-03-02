import requests
import json

def test_transcription_and_summarization(file_path):
    upload_url = "http://127.0.0.1:5000/upload"
    summarize_url = "http://127.0.0.1:5000/summarize"
    
    # Step 1: Upload the audio file for transcription
    with open(file_path, "rb") as audio_file:
        files = {"file": audio_file}
        response = requests.post(upload_url, files=files)
    
    if response.status_code != 200:
        print(f"Error in transcription request: {response.text}")
        return
    
    response_json = response.json()
    transcript = response_json.get("transcript", "")
    summary = response_json.get("summary", "")
    
    print("Transcription:")
    print(transcript)
    print("\nInitial Summary:")
    print(summary)
    
    # Step 2: Send the transcript to the summarization endpoint
    summarize_response = requests.post(summarize_url, json={"text": transcript})
    
    if summarize_response.status_code != 200:
        print(f"Error in summarization request: {summarize_response.text}")
        return
    
    final_summary = summarize_response.json().get("summary", "")
    print("\nFinal Summary:")
    print(final_summary)

# Run the test
test_transcription_and_summarization("test.mp3")