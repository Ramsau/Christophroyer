from django.conf import settings

import re
import os
import datetime
from moviepy.editor import VideoFileClip, concatenate_videoclips

from .models import Clip

def createVideo(text):
    text = text.lower()
    words = [s for s in re.split('[^a-zA-Z]', text) if s]  # split into words and remove empty
    text_clean = ' '.join(words)

    if (Clip.objects.filter(text__iexact=text_clean).exists()):  # read existing file, renew life cycle
        clip_db = Clip.objects.get(text__iexact=text_clean)
        clip_db.created = datetime.datetime.now()
        clip_db.save()
    else:  # create new clip
        clip_db = Clip.objects.create(text=text_clean)

        videoFileClips = []
        for word in words:
            vidPath = os.path.join(settings.KURZ_WORDS, word + '.mp4')
            if os.path.exists(vidPath):
                videoFileClips.append(VideoFileClip(vidPath))
        # TODO: ADD EMPTY SNIPPET IF NO WORDS ARE MATCHED
        clip = concatenate_videoclips(videoFileClips)
        clip.write_videofile(os.path.join(settings.KURZ_CLIPS, str(clip_db.id) + '.webm'))

    return str(clip_db.id) + '.webm'
