from fastapi.templating import Jinja2Templates
from ultralytics import YOLO
import io
import subprocess
import os
import cv2
import torch
from fastapi import FastAPI, File, UploadFile, HTTPException, Response, status
from fastapi.responses import StreamingResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import aiofiles
from fastapi.responses import JSONResponse
import shutil
from fastapi.staticfiles import StaticFiles
from datetime import datetime

timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/uploadform/")
async def form_page():
	htmlcontent = """
	<html>
  		<head>
    			<title> Object detection using YOLOV8 </title>
  		</head>
  		<body style="background-color:powderblue;">
    			<center>
    			<h2> Object detection using YOLOV8 </h2>
    			<img src="/static/od.jpeg" width="600" height="300">
    			<form method="POST" action="/uploadfile/" enctype="multipart/form-data">
      				<input type="file" name="item" /><br>
      				<button type="submit" style="height:40px;width:60px">Submit</button> 
    			</form>
    			</center>
  		</body>
	</html>
	"""
	return HTMLResponse(content=htmlcontent, status_code=200)
@app.post("/uploadfile/")
async def create_upload_file(item: UploadFile):
	if os.path.exists("./runs"):
		shutil.rmtree("./runs")
	fn = item.filename
	model = YOLO("8l-e20-20k.pt")
	data = await item.read()
	if fn.split(".")[-1] in ["jpg", "jpeg", "png"]:
		with open("image."+fn.split(".")[-1], "wb") as f:
			f.write(data)
		#print(fn.split(".")[-1])
		shutil.copy("./image."+fn.split(".")[-1], "./static/input_image.jpg")
		model.predict("image."+fn.split(".")[-1], save=True)
		output_file_path ="./runs/detect/predict/image."+fn.split(".")[-1]
		shutil.copy(output_file_path, "./static/output_image.jpg")
		html_content = """
		<html lang="en">
		<head>
    			<meta charset="UTF-8">
    			<meta name="viewport" content="width=device-width, initial-scale=1.0">
    			<title>Display Two Images with Headings</title>
		</head>
		<body>

		<div>
    			<h2>Input Image</h2>
    			<img src="/static/input_image.jpg" alt="First Image">
		</div>

		<div>
    			<h2>Detected Image</h2>
    			<img src="/static/output_image.jpg" alt="Second Image">
		</div>

		</body>
		</html>

		"""
		return HTMLResponse(content=html_content, status_code=200)


	elif fn.split(".")[-1] in ["mov", "mp4"]:
		with open("video."+fn.split(".")[-1], "wb") as f:
			f.write(data)
		model.predict("video."+fn.split(".")[-1], save=True)
		shutil.copy("./video.mov", "./static/input_video.mp4")
		output_file_path ="./runs/detect/predict/video.mp4"
		shutil.copy(output_file_path, "./static/video.mp4")
		input_video = "./static/video.mp4"
		output_video = "output_video.mp4"
		ffmpeg_command = [
    			"ffmpeg",
    			"-i", input_video,
    			"-c:v", "libx264",
    			"-c:a", "aac",
    			"-strict", "experimental",
    			output_video
		]
		subprocess.run(ffmpeg_command, check=True)
		shutil.copy("./output_video.mp4", "./static/output_video.mp4")
		html_content = """
		<html lang="en">
		<head>
    			<meta charset="UTF-8">
    			<meta name="viewport" content="width=device-width, initial-scale=1.0">
    			<title>Display Two Videos with Headings</title>
		</head>
		<body>

		<div>
    			<h2>Input Video</h2>
    			<video width="320" height="240" controls>
        			<source src="/static/input_video.mp4" type="video/mp4">
        			Your browser does not support the video tag.
    			</video>
		</div>

		<div>
    			<h2>Detected Video</h2>
    			<video width="320" height="240" controls>
        			<source src="/static/output_video.mp4" type="video/mp4">
        			Your browser does not support the video tag.
    			</video>
		</div>

		</body>
		</html>

    		"""
		return HTMLResponse(content=html_content, status_code=200)








