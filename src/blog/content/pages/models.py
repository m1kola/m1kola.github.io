# -*- coding: utf-8 -*-
from datetime import date


class JobPosition(object):
    def __init__(self, company_name, position, start_at, leave_at=None,
                 location=None, website=None,
                 responsibilities=list(),
                 achievements=list()):
        self.company_name = company_name
        self.position = position
        self.start_at = start_at
        self.leave_at = leave_at if leave_at else date.today()
        self.location = location
        self.website = website
        self.responsibilities = responsibilities
        self.achievements = achievements
