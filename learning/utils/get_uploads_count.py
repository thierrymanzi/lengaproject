from learning.models import (
    Category, Lesson,
    Question,QuestionEndScreenAudio,
    RankPriorityOption
)


def getCount():
    count = 0

    categories = Category.objects.all()

    for category in categories:
        thumbnail = category.thumbnail
        if thumbnail != '' and thumbnail is not None:
            count += 1
        try:
            audio_file = category.audio_file
            if audio_file != '' and audio_file is not None:
                count += 1
        except Exception as e:
            pass

        lessons = Lesson.objects.filter(category=category)

        for lesson in lessons:
            thumbnail = lesson.thumbnail
            if thumbnail != '' and thumbnail is not None:
                count += 1

            try:
                audio_file = lesson.audio_file
                if audio_file != '' and audio_file is not None:
                    count += 1
            except Exception as e:
                pass

            questions = Question.objects.filter(lesson=lesson)

            for question in questions:
                audio_file = question.audio_file
                if audio_file != '' and audio_file is not None:
                    count += 1
                try:
                    video_file = question.video_file
                    if video_file != '' and video_file is not None:
                        count += 1
                except Exception as e:
                    pass

                question_options = question.question_options.all()
                for question_option in question_options:
                    audio_file = question_option.audio_file
                    thumbnail = question_option.thumbnail

                    try:
                        if audio_file != '' and audio_file is not None:
                            count += 1
                    except Exception as e:
                        pass

                    try:
                        if thumbnail != '' and thumbnail is not None:
                            count += 1
                    except Exception as e:
                        pass

                    sub_options = question_option.sub_options.all()
                    for sub_option in sub_options:
                        audio_file = sub_option.audio_file
                        thumbnail = sub_option.thumbnail

                        try:
                            if audio_file != '' and audio_file is not None:
                                count += 1
                        except Exception as e:
                            pass

                        try:
                            if thumbnail != '' and thumbnail is not None:
                                count += 1
                        except Exception as e:
                            pass

    ranks = RankPriorityOption.objects.all()

    for rank in ranks:
        thumbnail = rank.thumbnail
        try:
            if thumbnail != '' and thumbnail is not None:
                count += 1
        except Exception as e:
            pass

    end_screen_audios = QuestionEndScreenAudio.objects.all()
    for end_screen_audio in end_screen_audios:
        audio_file = end_screen_audio.audio_file
        try:
            if audio_file != '' and audio_file is not None:
                count += 1
        except Exception as e:
            pass

    return count




