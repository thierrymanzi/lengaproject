#!/projects/env/bin/python
import os
import sys

sys.path.append("/projects/lenga")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lenga.settings.base")

import django

django.setup()

from datetime import datetime
from learning.models import Category, Lesson, Question, QuestionOption, RankPriorityOption, QuestionEndScreenAudio



categories = Category.objects.all()
lessons = Lesson.objects.all()
questions = Question.objects.all()
qoptions = QuestionOption.objects.all()
rank_priority_options = RankPriorityOption.objects.all()
end_screen_audios = QuestionEndScreenAudio.objects.all()


for k in categories:
    audio_f = k.audio_file
    thumb_n = k.thumbnail
    if "?X-" in str(audio_f):
        aud = str(audio_f).split("?X-")[0]
        k.audio_file = aud
    if "?X-" in str(thumb_n):
        thumb = str(thumb_n).split("?X-")[0]
        k.thumbnail = thumb

    if "?X-Amz-Algorithm=" in str(audio_f):
        aud = str(audio_f).split("?X-Amz-Algorithm=")[0]
        k.audio_file = aud
    if "?X-Amz-Algorithm=" in str(thumb_n):
        thumb = str(thumb_n).split("?X-Amz-Algorithm=")[0]
        k.thumbnail = thumb
    k.save()

for k in lessons:
    audio_f = k.audio_file
    thumb_n = k.thumbnail
    if "?X-" in str(audio_f):
        aud = str(audio_f).split("?X-")[0]
        k.audio_file = aud
        print(k.id)
    if "?X-" in str(thumb_n):
        thumb = str(thumb_n).split("?X-")[0]
        k.thumbnail = thumb
        print(k.id)

    if "?X-Amz-Algorithm=" in str(audio_f):
        aud = str(audio_f).split("?X-Amz-Algorithm=")[0]
        k.audio_file = aud
        print(k.id)
    if "?X-Amz-Algorithm=" in str(thumb_n):
        thumb = str(thumb_n).split("?X-Amz-Algorithm=")[0]
        k.thumbnail = thumb
        print(k.id)
    k.save()


for k in questions:
    audio_f = k.audio_file
    video_f = k.video_file
    thumb_n = k.thumbnail
    if "?X-" in str(audio_f):
        #print(k.id, k.audio_file)
        aud = str(audio_f).split("?X-")[0]
        k.audio_file = aud
        #print(k.id, k.audio_file)
    
    if "?X-" in str(video_f):
        #print(k.id, k.audio_file)
        vid = str(video_f).split("?X-")[0]
        k.video_file = vid

    if "?X-" in str(thumb_n):
        try:
            thumb = str(thumb_n).split("?X-")[0]
            k.thumbnail = thumb
            print(k.id)
        except Exception as e:
           print("Video error:".format(e))

    k.save()


for k in qoptions:
    audio_f = k.audio_file
    thumb_n = k.thumbnail
    if "?X-" in str(audio_f):
        aud = str(audio_f).split("?X-")[0]
        k.audio_file = aud
        print(k.id)
    if "?X-" in str(thumb_n):
        thumb = str(thumb_n).split("?X-")[0]
        k.thumbnail = thumb
        print(k.id)

    if "?X-Amz-Algorithm=" in str(audio_f):
        aud = str(audio_f).split("?X-Amz-Algorithm=")[0]
        k.audio_file = aud
        print(k.id)
    if "?X-Amz-Algorithm=" in str(thumb_n):
        thumb = str(thumb_n).split("?X-Amz-Algorithm=")[0]
        k.thumbnail = thumb
        print(k.id)
    k.save()



for k in rank_priority_options:
    thumb_n = k.thumbnail
    if "?X-" in str(thumb_n):
        thumb = str(thumb_n).split("?X-")[0]
        k.thumbnail = thumb
        print(k.id)


    if "?X-Amz-Algorithm=" in str(thumb_n):
        thumb = str(thumb_n).split("?X-Amz-Algorithm=")[0]
        k.thumbnail = thumb
        print(k.id)
    k.save()


for k in end_screen_audios:
    thumb_n = k.audio_file
    if "?X-" in str(thumb_n):
        thumb = str(thumb_n).split("?X-")[0]
        k.audio_file = thumb
        print(k.id)


    if "?X-Amz-Algorithm=" in str(thumb_n):
        thumb = str(thumb_n).split("?X-Amz-Algorithm=")[0]
        k.audio_file = thumb
        print(k.id)
    k.save()
print("Successfully ran at:{}".format(datetime.now()))
