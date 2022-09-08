from learning.models import Category, Lesson, Question, QuestionOption



categories = Category.objects.all()
lessons = Lesson.objects.all()
questions = Question.objects.all()
qoptions = QuestionOption.objects.all()



for k in categories:
    audio_f = k.audio_file
    thumb_n = k.thumbnail
    if "?X-Amz-Credential=" in str(audio_f):
        aud = str(audio_f).split("?X-Amz-Credential=")[0]
        k.audio_file = aud
    if "?X-Amz-Credential=" in str(thumb_n):
        thumb = str(thumb_n).split("?X-Amz-Credential=")[0]
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
    if "?X-Amz-Credential=" in str(audio_f):
        aud = str(audio_f).split("?X-Amz-Credential=")[0]
        k.audio_file = aud
        print(k.id)
    if "?X-Amz-Credential=" in str(thumb_n):
        thumb = str(thumb_n).split("?X-Amz-Credential=")[0]
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
    if "?X-Amz-Credential=" in str(audio_f):
        #print(k.id, k.audio_file)
        aud = str(audio_f).split("?X-Amz-Credential=")[0]
        k.audio_file = aud
        #print(k.id, k.audio_file)
    
    if "?X-Amz-Algorithm=" in str(audio_f):
        #print(k.id, k.audio_file)
        aud = str(audio_f).split("?X-Amz-Algorithm=")[0]
        k.audio_file = aud
    k.save()


for k in qoptions:
    audio_f = k.audio_file
    thumb_n = k.thumbnail
    if "?X-Amz-Credential=" in str(audio_f):
        aud = str(audio_f).split("?X-Amz-Credential=")[0]
        k.audio_file = aud
        print(k.id)
    if "?X-Amz-Credential=" in str(thumb_n):
        thumb = str(thumb_n).split("?X-Amz-Credential=")[0]
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
