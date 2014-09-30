# -*- coding: utf-8 -*-

import model.base

class Campaign(model.base.BaseModel):
    '''A collection of questionsets actively being sent out.'''

    def __init__(self, app, id = None, **kwargs):
        super(Campaign, self).__init__(
            app,
            id,
            {
                'title': None,
                'start-date': None,
                'frequency': None,
                'users': [],
                'questions': [],
            },
            True,
            **kwargs
        )
