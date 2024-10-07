import os

import moviepy.editor as mpe

from pytubefix import YouTube

from apps.clip.models import Clip
from config import settings

proxy_handler = {
    "http": settings.PROXY_URL,
    "https": settings.PROXY_URL,
}


def download_clips():
    clips = Clip.objects.all()

    clips_ids_to_download = (
        clip.youtube_id
        for clip in clips
        if not os.path.exists(
            os.path.join(settings.CLIPS_PATH, f"{clip.youtube_id}.mp4")
        )
    )

    for clip_id_to_download in clips_ids_to_download:
        download_clip(clip_id_to_download)


def download_clip(clip_id: str):
    video_url = f"https://www.youtube.com/watch?v={clip_id}"
    yt = YouTube(video_url, proxies=proxy_handler)
    video_path = _download_video(yt, clip_id)
    audio_path = _download_audio(yt, clip_id)

    _mix_video_and_audio(video_path, audio_path, clip_id)

    os.remove(video_path)
    os.remove(audio_path)


def _download_video(yt: YouTube, clip_id: str):
    video_name = f"clip_{clip_id}.mp4"

    video = (
        yt.streams.filter(type="video", mime_type="video/mp4")
        .order_by("resolution")
        .last()
        .download(output_path=settings.CLIPS_PATH, filename=video_name)
    )
    return video


def _download_audio(yt: YouTube, clip_id: str):
    audio_name = f"audio_{clip_id}.mp3"

    audio = (
        yt.streams.filter(only_audio=True)
        .first()
        .download(output_path=settings.CLIPS_PATH, filename=audio_name)
    )
    return audio


def _mix_video_and_audio(video_path, audio_path, clip_id):
    video = mpe.VideoFileClip(video_path)
    audio = mpe.AudioFileClip(audio_path)
    final = video.set_audio(audio)

    final.write_videofile(os.path.join(settings.CLIPS_PATH, f"{clip_id}.mp4"))
