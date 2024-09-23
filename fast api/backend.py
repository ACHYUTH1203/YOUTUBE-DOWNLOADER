from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse  # Import JSONResponse
import os
import yt_dlp

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Specify the exact origin of your frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

cur_dir = os.getcwd()

@app.post("/download")
def download_video(link: str = Form(...)):
    if not link:
        return JSONResponse({"message": "No link provided", "status": "failed"}, status_code=400)
    
    youtube_dl_options = {
        "format": "best",  # Replace 'b' with the desired format code for the video quality
        "outtmpl": os.path.join(cur_dir, f"Video-{link[-11:]}.mp4")  # Save the video as 'abcsample.mp4'
    }

    try:
        with yt_dlp.YoutubeDL(youtube_dl_options) as ydl:
            ydl.download([link])
        return JSONResponse({"message": "Download successful", "status": "success"})
    except Exception as e:
        return JSONResponse({"message": f"Error: {str(e)}", "status": "failed"}, status_code=500)
