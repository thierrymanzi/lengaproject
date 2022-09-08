#!/projects/env/bin/python
import os
import sys

sys.path.append("/projects/lenga")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lenga.settings.base")

import django

django.setup()

from datetime import datetime
from learning.models import Category, Lesson, Question, QuestionOption, RankPriorityOption, QuestionEndScreenAudio


#####
from boto3.s3.transfer import S3Transfer
import boto3
def set_file_public(file_link):
    try:
        print("Here")
        print(file_link)
        if '%20' in file_link:
            file_link = file_link.replace("%20", " ")
        if '.com/' in file_link:
            file_link = file_link.split(".com/")[1]
        elif '.net/' in file_link:
            file_link = file_link.split(".net/")[1]
        file_link = file_link.split("/")
        access_key = "AKIAQUXB422QKSLOTIDL"
        secret_key = "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"

        client = boto3.client(
            's3', aws_access_key_id=access_key,
            aws_secret_access_key = secret_key
        )
        transfer = S3Transfer(client)
        bucket_name = "busara-lenga"

        folder_name = file_link[0]
        filename = file_link[1]

        response = client.put_object_acl(ACL='public-read', Bucket=bucket_name, Key="%s/%s" % (folder_name, filename))
        print(response)

    except Exception as e:
        print("link:{},status={}".format(
            file_link, e
        ))
    #####



categories = Category.objects.all()
lessons = Lesson.objects.all()
questions = Question.objects.all()
qoptions = QuestionOption.objects.all()
rank_priority_options = RankPriorityOption.objects.all()


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
    set_file_public(k.thumbnail)
    set_file_public(k.audio_file)


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
    set_file_public(k.thumbnail)
    set_file_public(k.audio_file)


for k in questions:
    audio_f = k.audio_file
    if "?X-" in str(audio_f):
        #print(k.id, k.audio_file)
        aud = str(audio_f).split("?X-")[0]
        k.audio_file = aud
        #print(k.id, k.audio_file)
    
    if "?X-" in str(audio_f):
        #print(k.id, k.audio_file)
        aud = str(audio_f).split("?X-")[0]
        k.audio_file = aud
    k.save()
    set_file_public(k.audio_file)
    try:
        set_file_public(k.thumbnail)
    except Exception as e:
        print(e)

    try:
        set_file_public(k.video_file)
    except Exception as e:
        print(e)


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
    set_file_public(k.thumbnail)
    set_file_public(k.audio_file)



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
    set_file_public(k.thumbnail)


end_screen_audios = QuestionEndScreenAudio.objects.all()
for k in end_screen_audios:
    set_file_public(k.audio_file)


print("Successfully ran at:{}".format(datetime.now()))

