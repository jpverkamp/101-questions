import random
import pyparsing as pp

ID_ALPHABET = 'abcdefghijklmnopqrstuvwxyz0123456789'
ID_LENGTH = 7

def randomID():
    return ''.join([random.choice(ID_ALPHABET) for i in range(ID_LENGTH)])

def parseFrequency(input):
    dayOfWeek = (
        pp.Literal('mon')
        | pp.Literal('tues')
        | pp.Literal('wed')
        | pp.Literal('thurs')
        | pp.Literal('fri')
        | pp.Literal('sat')
        | pp.Literal('sun')
    ) + pp.Optional('day').suppress()

    daily = pp.Group(pp.Literal('daily'))

    weekly = pp.Group(
        (
            pp.Optional(pp.Literal('weekly'))
            + pp.Optional('on').suppress()
            + dayOfWeek
        ) | pp.Literal('weekly')
    )

    monthly = pp.Group(
        pp.Literal('monthly')
        + pp.Optional(
            pp.Optional('on').suppress()
            + pp.Literal('day').suppress()
            + pp.Word(pp.nums)
        )
    )

    frequency = monthly | weekly | daily

    time = (
        pp.Optional(pp.Literal('at')).suppress()
        + pp.Word(pp.nums)
        + pp.Optional(pp.Literal('am') | pp.Literal('pm'))
    )

    parser = pp.Group(
        frequency
        + pp.ZeroOrMore(pp.Literal(',').suppress() + frequency)
    ) + pp.Group(pp.Optional(time))

    result = parser.parseString(input.lower())

    dayOfWeek = { 'mon': 0, 'tues': 1, 'wed': 2, 'thurs': 3, 'fri': 4, 'sat': 5, 'sun': 6 }

    # Fix aliases on dates
    for i, raw_date in enumerate(result[0]):
        if raw_date[0] == 'weekly' and len(raw_date) == 1:
            result[0][i] = ['weekly', 0]
        elif raw_date[0] == 'weekly' and len(raw_date) == 2:
            result[0][i] = ['weekly', dayOfWeek[raw_date[1]]]
        elif raw_date[0] in dayOfWeek:
            result[0][i] = ['weekly', dayOfWeek[raw_date[0]]]
        elif raw_date[0] == 'monthly' and len(raw_date) == 1:
            result[0][i] = ['monthly', 1]
        elif raw_date[0] == 'monthly' and len(raw_date) == 2:
            result[0][i] = ['monthly', int(raw_date[1])]

    # Fix aliases on time
    if not result[1]:
        hour = 0
    elif len(result[1]) == 1:
        hour = int(result[1][0])
    else:
        hour = int(result[1][0])
        if len(result[1]) == 2 and result[1][1].lower() == 'pm':
            hour += 12

    if hour > 24:
        hour = hour // 100

    result[1] = hour

    return result
