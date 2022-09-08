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



from learning.models import Category, Lesson, Question,QuestionEndScreenAudio, RankPriorityOption


ORIGINAL_LINK = "https://busara-lenga.s3.amazonaws.com"
NEW_LINK = "http://d19y5kr4id28vg.cloudfront.net"

categories = Category.objects.all()

for category in categories:
    thumbnail = category.thumbnail
    thumbnail = thumbnail.replace(ORIGINAL_LINK, NEW_LINK)
    category.thumbnail = thumbnail
    category.save()
    try:
        audio_file = category.audio_file
        audio_file = audio_file.replace(ORIGINAL_LINK, NEW_LINK)
        category.audio_file = audio_file
        category.save()
    except Exception as e:
        print(e)


    lessons = Lesson.objects.filter(category=category)

    for lesson in lessons:
        thumbnail = lesson.thumbnail
        thumbnail = thumbnail.replace(ORIGINAL_LINK, NEW_LINK)
        lesson.thumbnail = thumbnail
        lesson.save()
        try:
            audio_file = lesson.audio_file
            audio_file = audio_file.replace(ORIGINAL_LINK, NEW_LINK)
            lesson.audio_file = audio_file
            lesson.save()
        except Exception as e:
            print(e)



        questions = Question.objects.filter(lesson=lesson)

        for question in questions:
            audio_file = question.audio_file
            audio_file = audio_file.replace(ORIGINAL_LINK, NEW_LINK)
            question.audio_file = audio_file
            question.save()
            try:
                video_file = question.video_file
                video_file = video_file.replace(ORIGINAL_LINK, NEW_LINK)
                question.video_file = video_file
                question.save()
            except Exception as e:
                print(e)


            question_options =  question.question_options.all()
            for question_option in question_options:
                audio_file = question_option.audio_file
                thumbnail = question_option.thumbnail

                try:
                    audio_file = audio_file.replace(ORIGINAL_LINK, NEW_LINK)
                    question_option.audio_file = audio_file
                    question_option.save()
                except Exception as e:
                    print(e)

                try:
                    thumbnail = thumbnail.replace(ORIGINAL_LINK, NEW_LINK)
                    question_option.thumbnail = thumbnail
                    question_option.save()
                except Exception as e:
                    print(e)


                sub_options = question_option.sub_options.all()
                for sub_option in sub_options:
                    audio_file = sub_option.audio_file
                    thumbnail = sub_option.thumbnail

                    try:
                        audio_file = audio_file.replace(ORIGINAL_LINK, NEW_LINK)
                        sub_option.audio_file = audio_file
                        sub_option.save()
                    except Exception as e:
                        print(e)

                    try:
                        thumbnail = thumbnail.replace(ORIGINAL_LINK, NEW_LINK)
                        sub_option.thumbnail = thumbnail
                        sub_option.save()
                    except Exception as e:
                        print(e)




ranks = RankPriorityOption.objects.all()

for rank in ranks:
    thumbnail = rank.thumbnail
    try:
        thumbnail = thumbnail.replace(ORIGINAL_LINK, NEW_LINK)
        rank.thumbnail = thumbnail
        rank.save()
    except Exception as e:
        print(e)


end_screen_audios = QuestionEndScreenAudio.objects.all()
for end_screen_audio in end_screen_audios:
    audio_file = end_screen_audio.audio_file
    try:
        audio_file = audio_file.replace(ORIGINAL_LINK, NEW_LINK)
        end_screen_audio.audio_file = audio_file
        end_screen_audio.save()
    except Exception as e:
        print(e)


