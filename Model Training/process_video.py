import subprocess
import os
import sys
import numpy as np
import pickle
import librosa
from moviepy.editor import VideoFileClip, concatenate_videoclips
from sklearn.ensemble import RandomForestClassifier

# Load trained model
MODEL_PATH = "cheer_detector_rf.pkl"

with open(MODEL_PATH, "rb") as model_file:
    model = pickle.load(model_file)

# Extract features from an audio segment
def extract_features(audio_segment, sr):
    mfcc = librosa.feature.mfcc(y=audio_segment, sr=sr, n_mfcc=13)
    spectral_centroid = librosa.feature.spectral_centroid(y=audio_segment, sr=sr)
    zero_crossing_rate = librosa.feature.zero_crossing_rate(audio_segment)
    features = np.hstack([np.mean(mfcc, axis=1), np.mean(spectral_centroid), np.mean(zero_crossing_rate)])
    return features

# Process video file
def process_video(video_path, output_dir, segment_duration=2.0, cheer_threshold=0.6):
    audio_path = os.path.join(output_dir, "extracted_audio.wav")

    # Extract audio
    subprocess.run(["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path, "-y"], check=True)

    # Load audio
    y, sr = librosa.load(audio_path, sr=16000)
    total_duration = librosa.get_duration(y=y, sr=sr)

    cheer_segments = []

    # Process each segment
    for start_time in np.arange(0, total_duration, segment_duration):
        end_time = min(start_time + segment_duration, total_duration)
        start_sample = int(start_time * sr)
        end_sample = int(end_time * sr)
        segment = y[start_sample:end_sample]

        if len(segment) > 0:
            features = extract_features(segment, sr).reshape(1, -1)
            probability = model.predict_proba(features)[0][1]

            if probability >= cheer_threshold:
                cheer_segments.append((start_time, end_time))
    # Cut and merge clipsM
    cut_and_merge_clips(video_path, cheer_segments, output_dir)

def merge_segments(segments, min_gap=2.0):
    """
    Merge overlapping or nearby segments into a single segment.
    """
    if not segments:
        return []

    # Sort segments by start time
    segments.sort()
    merged_segments = []
    current_start, current_end = segments[0]

    for start, end in segments[1:]:
        if start <= current_end + min_gap:  # Segments are close enough to merge
            current_end = max(current_end, end)  # Extend the current segment
        else:
            merged_segments.append((current_start, current_end))
            current_start, current_end = start, end

    # Add the last segment
    merged_segments.append((current_start, current_end))
    return merged_segments

def cut_and_merge_clips(video_path, cheer_segments, output_dir):
    video = VideoFileClip(video_path)
    cheer_clips = []

    # Merge overlapping or nearby segments
    merged_segments = merge_segments(cheer_segments)

    for start, end in merged_segments:
        # Calculate the 10-second window around the detected cheer segment
        mid_point = (start + end) / 2
        clip_start = max(0, mid_point - 5)  # 5 seconds before the mid-point
        clip_end = min(video.duration, mid_point + 5)  # 5 seconds after the mid-point

        # Ensure the clip is exactly 10 seconds long
        if clip_end - clip_start < 10:
            if clip_start == 0:
                clip_end = min(video.duration, clip_start + 10)
            else:
                clip_start = max(0, clip_end - 10)

        clip = video.subclip(clip_start, clip_end)
        cheer_clips.append(clip)

    if cheer_clips:
        final_video = concatenate_videoclips(cheer_clips)
        output_video_path = os.path.join(output_dir, "highlight_reel.mp4")
        final_video.write_videofile(output_video_path, codec="libx264", fps=30)
        print(f"Final video saved at: {output_video_path}")
    else:
        print("No cheers detected.")

video_file = "highlights.mp4"
output_directory = "output"
os.makedirs(output_directory, exist_ok=True)

process_video(video_file, output_directory)