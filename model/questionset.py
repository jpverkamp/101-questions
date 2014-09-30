# -*- coding: utf-8 -*-

import model.base

class QuestionSet(model.base.BaseModel):
    '''A collection of questions'''

    def __init__(self, app, id = None, **kwargs):
        super(QuestionSet, self).__init__(
            app,
            id,
            {
                'title': None,
                'questions': []
            },
            True,
            **kwargs
        )
