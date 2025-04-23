from flask import Flask, request, jsonify
import os
from process_video import process_video

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return "Welcome to the Automated Video Editor API!"

@app.route('/process', methods=['POST'])
def process():
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video = request.files['video']
    video_path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(video_path)

    try:
        process_video(video_path, OUTPUT_FOLDER)
        output_video_path = os.path.join(OUTPUT_FOLDER, "highlight_reel.mp4")
        return jsonify({
            "message": "Video processed successfully.",
            "output_path": output_video_path
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
