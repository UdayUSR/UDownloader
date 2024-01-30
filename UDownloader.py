#UDownloader by Uday
#30/01/2024
#Download Youtube Audio and Video

from pytube import YouTube
from pytube.cli import on_progress
import os
from moviepy.editor import VideoFileClip, AudioFileClip

def sanitize_filename(filename):
    # Define a set of invalid characters not allowed in filenames
    invalid_chars = r'<>:"/\|?*'

    # Replace invalid characters with underscores
    for char in invalid_chars:
        filename = filename.replace(char, '_')

    return filename

def download_audio(url, output_path):
    yt = YouTube(url, on_progress_callback=on_progress)
    
    audio_stream = yt.streams.filter(only_audio=True).last()
    if audio_stream:
        print("Downloading audio...")
        audio_stream.download(output_path)
        # Get the default filename of the audio file
        base, ext = os.path.splitext(audio_stream.default_filename)
        # Convert the audio file to mp3
        #new_file = base + '.mp3'
        new_file = os.path.join(output_path, base + '.mp3')
        # Rename the mp3 file
        #os.rename(audio_stream.default_filename, new_file)
        os.rename(os.path.join(output_path, audio_stream.default_filename), new_file)
        print("Mp3 download completed successfully!-UDownloader by Uday")
        return new_file  # Return the new audio file name

def download_video(url, res="720p", output_path="C:\\Users\\ASUS\\Downloads"):
    yt = YouTube(url, on_progress_callback=on_progress)
    video_stream = yt.streams.filter(res=res, file_extension="mp4").first()
    if video_stream:
        print(f"Downloading {res} video...")
        video_stream.download(output_path)
        # Get the video title and sanitize it
        video_title = sanitize_filename(yt.title)
        # Append the resolution to the sanitized video title
        new_filename = os.path.join(output_path, f"{video_title}_{res}.mp4")
        os.rename(os.path.join(output_path, video_stream.default_filename), new_filename)
        print("Download completed successfully!-UDownloader by Uday")
        return new_filename,yt.title  # Return the new video file name
    else:
        print(f"Error: No {res} resolution video found!")



def merge_audio_and_video(url, res="1080p", output_path="C:\\Users\\ASUS\\Downloads"):
    # Download the video-only stream (without audio) for the specified resolution
    v, t = download_video(url, res, output_path)

    # Download the audio stream separately (as mp3)
    a = download_audio(url, output_path)

    # Get the video title and sanitize it
    video_title = sanitize_filename(t)
    #Load the video and audio using moviepy
    video_clip = VideoFileClip(v)
    audio_clip = AudioFileClip(a)

    # Combine the video and audio
    final_clip = video_clip.set_audio(audio_clip)

    # Save the final merged video with both video and audio
    output_filename = os.path.join(output_path, f"{video_title}_{res}_merged.mp4")
    #output_filename = f"{video_title}_{res}_merged.mp4"
    final_clip.write_videofile(output_filename, codec="libx264")


    final_clip.close()
    video_clip.close()
    audio_clip.close()

    # # Define the output file path for the merged video
    # output_file_path = f"{video_title}_merged.mp4"

    # # Load the video and audio using python-ffmpeg
    # video_input = ffmpeg.input(v)
    # audio_input = ffmpeg.input(a)

    # # Combine the video and audio
    # merged_video = ffmpeg.output(video_input, audio_input, output_file_path, vcodec='copy', acodec='aac', strict='experimental')
    # ffmpeg.run(merged_video)

    # Remove the temporary video and audio files
    os.remove(v)
    os.remove(a)

    print("Merging completed successfully!-UDownloader by Uday")

# Download the video or merge audio and video for "1080p" resolution
url = input("Enter the YouTube video URL: ")
res = input("Enter the resolution (mp3, 144p, 240p, 360p, 480p, 720p, 1080p): ")
output_path = "C:\\Users\\ASUS\\Downloads"

# Create a YouTube object
#yt = YouTube(url, on_progress_callback=on_progress)

if res.lower() == "1080p":
    # Download the audio stream separately (as mp3) and get the audio file name
    # audio_file = download_audio(yt)
    merge_audio_and_video(url, res, output_path)
elif res.lower() == "mp3":
    download_audio(url, output_path)
else:
    download_video(url, res, output_path)