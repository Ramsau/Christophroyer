from django.conf import settings

import re
import os
import datetime
from moviepy.editor import VideoFileClip, concatenate_videoclips
import epitran
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.tools.drawing import circle, color_gradient

from .models import Clip, MissingWord




def createVideo(text):
    epi = epitran.Epitran('deu-Latn')
    text = text.lower()
    words = text.split()  # split into words and remove empty
    text_clean = ' '.join(words)

    clip_db, created_clip_db = Clip.objects.get_or_create(text=text_clean)
    if not created_clip_db:  # read existing file, renew life cycle
        clip_db.accessed = clip_db.accessed + 1
        clip_db.save()

    # delete old files
    cutoffTime = datetime.datetime.now() - datetime.timedelta(seconds=settings.KURZ_MAX_CACHE)
    clips_delete = Clip.objects.filter(created__lt=cutoffTime)

    for clip_del in clips_delete.all():
        try:
            os.remove(os.path.join(settings.KURZ_CLIPS, str(clip_del.id) + '.mp4'))
        except FileNotFoundError:
            pass

    # create file only if it doesn't already exist or caching is disabled
    if not os.path.exists(os.path.join(settings.KURZ_CLIPS, str(clip_db.id) + '.mp4'))\
            or not settings.KURZ_ENABLE_CACHE:
        videoFileClips = []
        for word in words:
            vidPath = os.path.join(settings.KURZ_WORDS, word + '.mp4')
            if os.path.exists(vidPath):
                videoFileClips.append(VideoFileClip(vidPath))
            else:
                # save entry for stats
                word_db, created_word = MissingWord.objects.get_or_create(word=word)
                if not created_word:
                    word_db.accessed = word_db.accessed + 1
                    word_db.save()

                # build word from phonemes
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
                        os.path.join(settings.KURZ_PHONEMES, '_.mp4')
                    )
                )


        if len(videoFileClips) == 0 and False:
            emptyVidPath = os.path.join(settings.KURZ_WORDS, '_.mp4')
            if os.path.exists(emptyVidPath):
                videoFileClips.append(VideoFileClip(emptyVidPath))

        # resize clips
        videoFileClips = [clip.resize(height=360) for clip in videoFileClips]

        # concatenate
        clip = concatenate_videoclips(videoFileClips, method='compose')

        # add caption
        text = TextClip(
            'kurzspricht.at',
            fontsize=15,
            size=(100, 20),
            align='center',
            method='caption',
            color='white',
        )\
            .set_duration(clip.duration)\
            .set_position((530, 15))
        grad = TextClip(
            '',
            fontsize=15,
            size=(100, 25),
            align='South',
            method='caption',
            color='#2f63c9',
            bg_color='#2f63c9'
        )\
            .set_duration(clip.duration)\
            .set_position((530, 8))\
            .set_opacity(0.8)
        clip = CompositeVideoClip([clip, grad, text])
        clip.write_videofile(os.path.join(settings.KURZ_CLIPS, str(clip_db.id) + '.mp4'), logger=None)

    return str(clip_db.id) + '.mp4'
