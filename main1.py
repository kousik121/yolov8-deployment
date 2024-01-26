from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/items/")
async def read_items():
    html_content = """
    <html>
      <body>
        <video width="320" height="240" controls>
          <source src="/static/output_video.mp4" type="video/mp4">
          Your browser does not support the video tag.
        </video>
	<script>
          var video = document.querySelector('video');
          video.addEventListener('error', function (e) {
            console.error('Video playback error:', e);
          });
        </script>
      </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
