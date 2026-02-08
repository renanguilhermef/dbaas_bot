import os
from litellm import completion
# 1. Setup Environment
# Point to your downloaded Service Account JSON key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcloud.json"
os.environ["VERTEX_PROJECT"] = "vaulted-splice-486609-r3"
os.environ["VERTEX_LOCATION"] = "us-central1"
print("Credentials path:", os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
# Use 'vertex_ai/' prefix to tell litellm to use the Vertex API, not AI Studio
try:
    response = completion(
        model="vertex_ai/gemini-2.5-flash", 
        messages=[{"role": "user", "content": "Test Gemini API"}],
        # api_base is handled automatically by litellm based on VERTEX_LOCATION
    )
    print("Gemini response:", response.choices[0].message.content)
except Exception as e:
    print("Error:", e)