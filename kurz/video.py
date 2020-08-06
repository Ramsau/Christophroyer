from django.conf import settings

import re
import os
import datetime
from moviepy.editor import VideoFileClip, concatenate_videoclips
import epitran

from .models import Clip

def createVideo(text):
    epi = epitran.Epitran('deu-Latn')
    text = text.lower()
    words = [s for s in re.split('[^a-zA-Z]', text) if s]  # split into words and remove empty
    text_clean = ' '.join(words)

    if (Clip.objects.filter(text__iexact=text_clean).exists()):  # read existing file, renew life cycle
        clip_db = Clip.objects.get(text__iexact=text_clean)
        clip_db.created = datetime.datetime.now()
        clip_db.save()
    else:
        # create new db entry
        clip_db = Clip.objects.create(text=text_clean)

        # delete old ones
        cutoffTime = datetime.datetime.now() - datetime.timedelta(seconds=settings.KURZ_MAX_CACHE)
        clips_delete = Clip.objects.filter(created__lt=cutoffTime)

        for clip_del in clips_delete.all():
            try:
                os.remove(os.path.join(settings.KURZ_CLIPS, str(clip_del.id) + '.mp4'))
            finally:
                clip_del.delete()

    # create file only if it doesn't already exist
    if not os.path.exists(os.path.join(settings.KURZ_CLIPS, str(clip_db.id) + '.mp4')):
        videoFileClips = []
        for word in words:
            vidPath = os.path.join(settings.KURZ_WORDS, word + '.mp4')
            if os.path.exists(vidPath):
                videoFileClips.append(VideoFileClip(vidPath))
            else:
                phonemes = epi.xsampa_list(word)

                for phoneme in phonemes:
                    phoneme_simple = phoneme.replace(':', '')
                    if phoneme_simple.isupper():
                        phoneme_simple = '^' + phoneme_simple.lower()

                    phonemePath = os.path.join(settings.KURZ_PHONEMES, phoneme_simple + '.mp4')

                    if os.path.exists(phonemePath):
                        videoFileClips.append(VideoFileClip(phonemePath))
                    else:
                        print('Phoneme not found: %s' % phoneme_simple)

                videoFileClips.append(
                    VideoFileClip(
                        os.path.join(settings.KURZ_WORDS, '_.mp4')
                    )
                )


        if len(videoFileClips) == 0:
            emptyVidPath = os.path.join(settings.KURZ_WORDS, '_.mp4')
            if os.path.exists(emptyVidPath):
                videoFileClips.append(VideoFileClip(emptyVidPath))

        clip = concatenate_videoclips(videoFileClips)
        clip.write_videofile(os.path.join(settings.KURZ_CLIPS, str(clip_db.id) + '.mp4'))

    return str(clip_db.id) + '.mp4'
