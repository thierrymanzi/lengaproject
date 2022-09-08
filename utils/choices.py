# -*- coding: utf-8 -*-
# @Author: Simon Muthusi
# @Email: simonmuthusi@gmail.com
# @Date:   2020-06-15 14:42:43
# @Last Modified by:   Simon Muthusi
# @Last Modified time: 2020-06-15 15:43:58
# Project: lenga


class Choice:
    INDIVIDUAL = 'Individual'
    GROUP = 'Group'

    ACCOUNT_TYPE = (
        (INDIVIDUAL, INDIVIDUAL),
        (GROUP, GROUP)
    )

    MONTH = 'Month'
    WEEK = 'Week'

    PERIOD_CHOICES = (
        (MONTH, MONTH),
        (WEEK, WEEK)
    )

    PARTNER = 'partner'
    LOCATION = 'location'
    USER_TYPE = 'user_type'
    PERIOD = 'Period'

    SIGNUP_STATS_BREAKDOWN_ITEMS = (
        (PARTNER, PARTNER),
        (LOCATION, LOCATION),
        (USER_TYPE, USER_TYPE),
        (PERIOD, PERIOD)
    )


QUESTION_TYPES = (
    ('text', 'Open Ended'),
    ('video', 'Video'),
    ('single-choice', 'Single Choice'),
    ('multiple-choice', 'Multiple Choice'),
    ('category', 'Category'),
    ('sorting', 'Sorting'),
    ('rank', 'Rank'),
    ('discussion', 'discussion'),
    ('group_discussion_choose_one', 'group_discussion_choose_one'),
    ('calculator', 'calculator'),
    ('budget', 'budget'),
    ('saving_goal', 'saving_goal'),
    ('priority_no_stacking', 'priority_no_stacking'),
)


NORMAL_RANK = 'NORMAL'
PRIORITY_OPTIONS_LIST_RANK = 'PRIORITY_OPTIONS_LIST'
PRIORITY_CLUSTER = 'PRIORITY_CLUSTER'
PIE_CHART = 'PIE_CHART'
REORDER = 'REORDER'

RANK_TYPES = (
    (NORMAL_RANK, NORMAL_RANK),
    (PRIORITY_OPTIONS_LIST_RANK, PRIORITY_OPTIONS_LIST_RANK),
    (PRIORITY_CLUSTER, PRIORITY_CLUSTER),
    (PIE_CHART, PIE_CHART),
    (REORDER, REORDER),
)


QUESTION_OPTION = 'question_option'
QUESTION_SUB_OPTION = 'question_sub_option'

RANK_MOVABLE_ITEMS = (
    (QUESTION_OPTION, QUESTION_OPTION),
    (QUESTION_SUB_OPTION, QUESTION_SUB_OPTION),
)


SHOW_QUESTION_OPTION_AUDIO_ICON_YES = 'YES'
SHOW_QUESTION_OPTION_AUDIO_ICON_NO = 'NO'

SHOW_QUESTION_OPTION_AUDIO_ICON_OPTIONS = (
    (SHOW_QUESTION_OPTION_AUDIO_ICON_YES, SHOW_QUESTION_OPTION_AUDIO_ICON_YES),
    (SHOW_QUESTION_OPTION_AUDIO_ICON_NO, SHOW_QUESTION_OPTION_AUDIO_ICON_NO),
)

EFFECT_QUESTION_VALIDATION_YES = 'YES'
EFFECT_QUESTION_VALIDATION_NO = 'NO'

EFFECT_QUESTION_VALIDATION_CHOICES = (
    (EFFECT_QUESTION_VALIDATION_YES, EFFECT_QUESTION_VALIDATION_YES),
    (EFFECT_QUESTION_VALIDATION_NO, EFFECT_QUESTION_VALIDATION_NO)
)


