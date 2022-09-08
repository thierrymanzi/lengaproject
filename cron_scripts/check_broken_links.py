#!/projects/env/bin/python
import os
import sys

sys.path.append("/projects/lenga")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lenga.settings.base")

import django

django.setup()

import requests



def url_exists(link):
    request = requests.get(str(link))
    if request.status_code == 200:
        print('Web site exists')
        return True
    else:
        print('Web site does not exist')
        return False



from learning.models import Category, Lesson, Question,QuestionOption


# category = Category.objects.get(id="b9df2f20-4bb2-421e-ba53-200c9e21f24c")
lesson = Lesson.objects.get(id="31fc1518-8a3f-4806-aef0-12d305e344c9")

# lesson = Lesson.objects.get(id="5cb677f7-0e5b-4e67-834f-9823d1323745")

questions = Question.objects.filter(lesson=lesson)


incorrect_question_audio_file = []
incorrect_question_options_audio_files = []
incorrect_question_options_thumbnails = []
incorrect_question_sub_options_audio_files = []
incorrect_question_sub_options_thumbnails = []


for question in questions:
    audio_file = question.audio_file
    if audio_file != '':
        exists = url_exists(audio_file)
        if exists is False:
            incorrect_question_audio_file.append(
                {
                    'q_id': str(question.id),
                    'audio_file': audio_file
                }
            )
    question_options =  question.question_options.all()
    for question_option in question_options:
        audio_file = question_option.audio_file
        thumbnail = question_option.thumbnail
        if audio_file != '':
            exists = url_exists(audio_file)
            if exists is False:
                incorrect_question_options_audio_files.append(
                    {
                        'q_id': str(question.id),
                        'q_o_id': str(question_option.id),
                        'audio_file': audio_file
                    }
                )
        if thumbnail != '':
            exists = url_exists(thumbnail)
            if exists is False:
                incorrect_question_options_thumbnails.append(
                    {
                        'q_id': str(question.id),
                        'q_o_id': str(question_option.id),
                        'thumbnail': thumbnail
                    }
                )
        sub_options = question_option.sub_options.all()
        for sub_option in sub_options:
            audio_file = sub_option.audio_file
            thumbnail = sub_option.thumbnail
            if audio_file != '':
                exists = url_exists(audio_file)
                if exists is False:
                    incorrect_question_sub_options_audio_files.append(
                        {
                            'q_id': str(question.id),
                            'q_o_id': str(question_option.id),
                            'q_o_so_id': str(sub_option.id),
                            'audio_file': audio_file
                        }
                    )
            if thumbnail != '':
                exists = url_exists(thumbnail)
                if exists is False:
                    incorrect_question_sub_options_thumbnails.append(
                        {
                            'q_id': str(question.id),
                            'q_o_id': str(question_option.id),
                            'q_o_so_id': sub_option.id,
                            'thumbnail': thumbnail
                        }
                    )


print("incorrect_question_audio_file={}".format(len(incorrect_question_audio_file)))
print("incorrect_question_options_audio_files={}".format(len(incorrect_question_options_audio_files)))
print("incorrect_question_options_thumbnails={}".format(len(incorrect_question_options_thumbnails)))
print("incorrect_question_sub_options_audio_files={}".format(len(incorrect_question_sub_options_audio_files)))
print("incorrect_question_sub_options_thumbnails={}".format(len(incorrect_question_sub_options_thumbnails)))



if len(incorrect_question_audio_file) > 0:
    # print(incorrect_question_audio_file)
    print("\n\n\nincorrect_question_audio_file={}".format(incorrect_question_audio_file))

if len(incorrect_question_options_audio_files) > 0:
    # print(incorrect_question_options_audio_files)
    print("\n\n\nincorrect_question_options_audio_files={}".format(incorrect_question_options_audio_files))

if len(incorrect_question_options_thumbnails) > 0:
    # print(incorrect_question_options_thumbnails)
    print("\n\n\nincorrect_question_options_thumbnails={}".format(incorrect_question_options_thumbnails))

if len(incorrect_question_sub_options_audio_files) > 0:
    # print(incorrect_question_sub_options_audio_files)
    print("\n\n\nincorrect_question_sub_options_audio_files={}".format(incorrect_question_sub_options_audio_files))

if len(incorrect_question_sub_options_thumbnails) > 0:
    print("\n\n\nincorrect_question_sub_options_thumbnails={}".format(incorrect_question_sub_options_thumbnails))









