# -*- coding: utf-8 -*-
# @Author: Simon Muthusi
# @Email: simonmuthusi@gmail.com
# @Date:   2020-06-15 14:42:43
# @Last Modified by:   Simon Muthusi
# @Last Modified time: 2020-06-15 16:33:37
# Project: lenga
from rest_framework import serializers

from learning.models import (
    Category,
    Lesson,
    Question,
    QuestionOption,
    Answer, MediaFile,
    Location,
    RankPriorityOption, QuestionEndScreenAudio)
from utils.choices import NORMAL_RANK, PRIORITY_OPTIONS_LIST_RANK



class ListQuestionOptionSerializer(serializers.ModelSerializer):
    sub_options = serializers.SerializerMethodField()
    audio_file = serializers.CharField(required=False, max_length=5000, allow_blank=True)
    thumbnail = serializers.CharField(required=False, max_length=5000, allow_blank=True)
    show_audio_icon = serializers.CharField(required=False, max_length=100, allow_blank=True)
    text_value = serializers.CharField(required=False, max_length=100, allow_blank=True)


    class Meta:
        model = QuestionOption
        fields = '__all__'

    def get_sub_options(self, obj):
        return obj.sub_options.all().values()

class QuestionSubOptionSerializer(serializers.ModelSerializer):
    audio_file = serializers.CharField(required=False, max_length=5000, allow_blank=True)
    thumbnail = serializers.CharField(required=False, max_length=5000, allow_blank=True)
    show_audio_icon = serializers.CharField(required=False, max_length=100, allow_blank=True)
    text_value = serializers.CharField(required=False, max_length=100, allow_blank=True)
    associated_rank_priority_order = serializers.IntegerField(required=False)

    class Meta:
        model = QuestionOption
        fields = '__all__'


    def update(self, instance, validated_data):
        # instance = super().update(instance, validated_data)
        instance = super(QuestionSubOptionSerializer, self).update(instance, validated_data)
        return instance


class QuestionOptionSerializer(serializers.ModelSerializer):
    sub_options = QuestionSubOptionSerializer(many=True, required=False)
    audio_file = serializers.CharField(required=False, max_length=5000, allow_blank=True)
    thumbnail = serializers.CharField(required=False, max_length=5000, allow_blank=True)
    show_audio_icon = serializers.CharField(required=False, max_length=100, allow_blank=True)
    text_value = serializers.CharField(required=False, max_length=100, allow_blank=True)
    associated_rank_priority_order = serializers.IntegerField(required=False)


    class Meta:
        model = QuestionOption
        fields = '__all__'


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListQuestionOptionSerializer
        return QuestionOptionSerializer



class RankPriorityOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = RankPriorityOption
        fields = '__all__'



class QuestionEndScreenAudioSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionEndScreenAudio
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    question_options = QuestionOptionSerializer(many=True, required=False)
    rank_priority_options = RankPriorityOptionSerializer(
        many=True, required=False,
        source='rank_priority_option'
    )
    rank_type = serializers.CharField(required=False, max_length=100, allow_blank=True)
    question_end_screen_audios = QuestionEndScreenAudioSerializer(
        many=True, required=False,
        source='question_end_screen_audio'
    )
    description2 = serializers.CharField(required=False, max_length=100, allow_blank=True)
    thumbnail = serializers.CharField(required=False, max_length=5000, allow_blank=True)
    header_color = serializers.SerializerMethodField()
    main_color = serializers.SerializerMethodField()
    footer_color = serializers.SerializerMethodField()
    effect_validation = serializers.CharField(
        required=False, max_length=100, allow_blank=True
    )

    class Meta:
        model = Question
        fields = '__all__'

    def get_header_color(self, obj):
        return str(obj.lesson.header_color)

    def get_main_color(self, obj):
        return str(obj.lesson.main_color)

    def get_footer_color(self, obj):
        return str(obj.lesson.footer_color)

    @staticmethod
    def create_question_option(question, question_options):
        if question_options:
            all = []
            for question_option in question_options:

                try:
                    sub_options = question_option['sub_options']
                    qo = question_option.pop('sub_options')
                    try:
                        associated_rank_priority_order = question_option['audio_file']
                    except Exception as e:
                        associated_rank_priority_order = 0
                    data = {
                        'audio_file': question_option['audio_file'],
                        'thumbnail': question_option['thumbnail'],
                        'show_audio_icon': question_option['show_audio_icon'],
                        'text_value': question_option['text_value'],
                        'text': question_option['text'],
                        'is_answer': question_option['is_answer'],
                        'order': question_option['order'],
                        'associated_rank_priority_order': associated_rank_priority_order
                    }

                    print("qo={}".format(qo))
                    qo = QuestionOption.objects.create(**data)
                    # all.append(qo)
                    question.question_options.add(qo)
                    question.save()
                    for sub_option in sub_options:
                        sub_option = QuestionOption.objects.create(**sub_option)
                        qo.sub_options.add(sub_option)
                        qo.save()

                except Exception as e:
                    print(e)
        return question


    @staticmethod
    def create_rank_priority_option(question, rank_priority_options):
        if rank_priority_options:
            for rank_priority_option in rank_priority_options:
                rank_priority_option = RankPriorityOption.objects.create(**rank_priority_option)
                rank_priority_option.question = question
                rank_priority_option.save()
            question.rank_type = PRIORITY_OPTIONS_LIST_RANK

        question.save()
        return question


    @staticmethod
    def create_question_end_screen_audio(question, question_end_screen_audio):
        if question_end_screen_audio:
            for question_end_screen_audio_ in question_end_screen_audio:
                curr_question_end_screen_audio = QuestionEndScreenAudio.objects.create(
                    **question_end_screen_audio_
                )
                curr_question_end_screen_audio.question = question
                curr_question_end_screen_audio.save()
        return question

    def create(self, validated_data):

        question_options = validated_data.pop('question_options') \
            if validated_data.get('question_options') else None
        text = validated_data['text']
        question_type = validated_data['question_type']
        lesson = validated_data['lesson']
        video_file = validated_data['video_file']
        order = validated_data["order"]
        thumbnail = validated_data["thumbnail"]
        description = ""
        audio_file = ""
        description2 = ""
        associated_rank_priority_order = 0

        try:
            description = validated_data['description']
        except Exception as e:
            pass

        try:
            audio_file = validated_data['audio_file']
        except Exception as e:
            pass

        try:
            description2 = validated_data['description2']
        except Exception as e:
            pass



        question = Question.objects.create(
            text=text,question_type=question_type,lesson=lesson,video_file=video_file,
            order=order,description=description,audio_file=audio_file,thumbnail=thumbnail,
            description2=description2)

        try:
            rank_type = validated_data['rank_type'] or None
            if rank_type:
                question.rank_type = rank_type.strip().upper()
                question.save()
        except Exception as e:
            pass
        try:
            rank_priority_options = validated_data['rank_priority_option']
            self.create_rank_priority_option(question, rank_priority_options)
        except Exception as e:
            pass

        try:
            #[{"audio_file":"", "order": 1}]
            question_end_screen_audios = validated_data['question_end_screen_audios']
            self.create_question_end_screen_audio(question, question_end_screen_audios)
        except Exception as e:
            pass
        return self.create_question_option(question, question_options)


    def update(self, instance, validated_data):
        """
        Given data with the structure below, update appropriate tables
            {
                "id": "897eb01e-c751-447f-b5ad-d8173c304e1e",
                "question_options": [
                    {
                        "id": "0e5ab438-3a2e-4a59-94fc-c7ab66ad7e53",
                        "sub_options": [
                            {
                                "id": "424d5f03-8559-4c7b-89aa-592f082a100a",
                            },
                            {
                                "id": "ac9f84bb-88cf-49db-87ab-5e351f8134b5"
                            }
                        ]
                    }
                ],
            }
        """
        validated_data.pop('question_options') \
            if validated_data.get('question_options') else None
        question = instance
        question.text = validated_data['text']
        question.question_type = validated_data['question_type']
        question.video_file = validated_data['video_file']
        question.order = validated_data['order']
        question.description = validated_data['description']
        question.audio_file = validated_data['audio_file']
        question.lesson = validated_data['lesson']
        question.thumbnail = validated_data['thumbnail']
        try:
            question.description2 = validated_data['description2']
        except Exception as e:
            pass
        question.save()

        q_options = QuestionOption.objects.all()

        sub_opts_ = []

        # We use context to get the request data since we require the id fields
        # to retrieve the question_options and sub_options to allow updates
        try:
            for option in self.context['request'].data.get('question_options'):
                try:
                    sub_options = option['sub_options']
                except Exception as e:
                    sub_options = None
                q_option = q_options.filter(id=option['id']).last()

                # Update sub_options if it exists
                if sub_options:
                    for sub in sub_options:
                        q_so = q_options.filter(id=sub['id']).last()

                        try:
                            q_so.text = sub['text']
                            q_so.thumbnail = sub['thumbnail']
                            q_so.audio_file = sub['audio_file']
                            q_so.is_answer = sub['is_answer']
                            q_so.order = sub['order']
                            q_so.show_audio_icon = sub['show_audio_icon']
                            q_so.text_value = sub['text_value']
                            q_so.associated_rank_priority_order = sub['associated_rank_priority_order'] or 0
                            q_so.save()
                            q_option.sub_options.remove(q_so)
                            q_option.sub_options.add(q_so)
                            sub_opts_.append(q_so)
                            q_option.save()
                            question.save()
                        except Exception as e:
                            pass

                q_option.text = option['text']
                q_option.thumbnail = option['thumbnail']
                q_option.audio_file = option['audio_file']
                q_option.is_answer = option['is_answer']
                q_option.order = option['order']
                q_option.show_audio_icon = option['show_audio_icon']
                q_option.text_value = option['text_value']
                q_option.order = option['order']
                q_option.associated_rank_priority_order = option['associated_rank_priority_order'] or 0
                q_option.save()
        except Exception as e:
            pass


        try:
            rank_priority_options = validated_data['rank_priority_option']

            if rank_priority_options:
                    print("rank_priority_options={}".format(rank_priority_options))
                    for rank_priority_option in rank_priority_options:
                        try:
                            RankPriorityOption.objects.filter(
                                id=rank_priority_option['id']
                            ).update(**rank_priority_option)
                        except Exception as e:
                            rpo = RankPriorityOption.objects.get_or_create(
                                order=rank_priority_option['order'],
                                thumbnail=rank_priority_option['thumbnail'],
                                question=question
                            )
                        question.save()
        except Exception as e:
            print("ERROR:{}".format(e))

        try:
            rank_type = validated_data['rank_type'] or None
            if rank_type:
                question.rank_type = rank_type.strip().upper()
                question.save()
        except Exception as e:
            pass

        try:
            question_end_screen_audios = validated_data['question_end_screen_audio']
            if question_end_screen_audios:
                    for question_end_screen_audio in question_end_screen_audios:
                        try:
                            esa = QuestionEndScreenAudio.objects.filter(
                            id=question_end_screen_audio['id']
                            ).update(**question_end_screen_audio)
                        except Exception as e:
                            esa = QuestionEndScreenAudio.objects.get_or_create(
                                audio_file=question_end_screen_audio['audio_file'],
                                order=question_end_screen_audio['order'],
                                question=question
                            )
                        question.save()
        except Exception as e:
            pass


        for sub_opt in sub_opts_:
            try:
                question.question_options.remove(sub_opt)
                question.save()
            except Exception as e:
                pass

        return question


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(
        read_only=True, many=True, source='lesson_questions')

    class Meta:
        model = Lesson
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    no_lessons = serializers.SerializerMethodField()

    def get_no_lessons(self, category):
        return Lesson.objects.filter(category=category).count()

    class Meta:
        model = Category
        fields = '__all__'


class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = '__all__'
