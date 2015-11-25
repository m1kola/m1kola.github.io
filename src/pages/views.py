# -*- coding: utf-8 -*-

from datetime import date

from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from pages.models import JobPosition


class AboutView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)

        career_started_at = date(2006, 6, 1)

        job_positions = [
            JobPosition(
                company_name=_(u'Wargaming.net'),
                position=_(u'Team Lead'),
                start_at=date(2014, 10, 17),
                leave_at=date.today(),
                location=_(u'Минск'),
                website='wargaming.com',
                responsibilities=[
                    _(u'Разработка и сопровождение портала игры World Of Tanks в 7 регионах '
                      u'(worldoftanks.eu, worldoftanks.ru, worldoftanks.com, worldoftanks.kr, worldoftanks.asia, '
                      u'scw.worldoftanks.cn and ncw.worldoftanks.cn).'),
                    _(u'Управление командой.'),
                ],
                achievements=[
                    _(u'Опыт координирования работ между несколькими проектами.'),
                    _(u'Опыт наставничества разработчиков, которые переключаются с PHP.'),
                    _(u'Опыт публичного выступления на Wargaming Developers Conference 2014 (WG DevCon).'),
                ]
            ),
            JobPosition(
                company_name=_(u'Wargaming.net'),
                position=_(u'Python Developer'),
                start_at=date(2013, 12, 26),
                leave_at=date.today(),
                location=_(u'Минск'),
                website='wargaming.com',
                responsibilities=[
                    _(u'Разработка и сопровождение продуктов компании.'),
                ],
                achievements=[
                    _(u'Опыт работы с языком Python и Python-фреймворками (Django, Flask, Falcon, Twisted).'),
                    _(u'Опыт работы с мультиязычным проектом (worldoftanks.eu, worldoftanks.ru, worldoftanks.com, '
                      u'worldoftanks.kr, worldoftanks.asia, scw.worldoftanks.cn and ncw.worldoftanks.cn).'),
                    _(u'Опыт работы с системами мониторинга (Newrelic, Sentry, Zabbix).'),
                    _(u'Опыт работы с Fabric (fabfile.org).'),
                    _(u'Рекорд в книге рекордов Гиннеса: самый большой MMO турнир.'),
                ]
            ),
            JobPosition(
                company_name=_(u'StartupLabs Inc.'),
                position=_(u'Team Lead'),
                start_at=date(2013, 04, 1),
                leave_at=date(2013, 11, 1),
                location=_(u'Минск'),
                website='itstartuplabs.com',
                responsibilities=[
                    _(u'Разработка и сопровождение продуктов компании.'),
                    _(u'Управление командой.'),
                ],
                achievements=[
                    _(u'Опыт управления командой (Dev, BA, QA).'),
                    _(u'Опыт непрерывной интеграции и непрерывной поставки.'),
                    _(u'Опыт проведения технических интервью.'),
                ]
            ),
            JobPosition(
                company_name=_(u'StartupLabs Inc.'),
                position=_(u'PHP Developer'),
                start_at=date(2012, 10, 1),
                leave_at=date(2013, 11, 1),
                location=_(u'Минск'),
                website='itstartuplabs.com',
                responsibilities=[
                    _(u'Разработка и сопровождение продуктов компании.'),
                ],
                achievements=[
                    _(u'Опыт работы с Symfony, Silex.'),
                    _(u'Опыт работы с RabbitMQ.'),
                ]
            ),
            JobPosition(
                company_name=_(u'Onliner.by'),
                position=_(u'PHP Developer'),
                start_at=date(2011, 9, 1),
                leave_at=date(2012, 10, 1),
                location=_(u'Минск'),
                website='onliner.by',
                responsibilities=[
                    _(u'Разработка и сопровождение продуктов компании.'),
                ],
                achievements=[
                    _(u'Опыт применения шаблонов проектирования.'),
                    _(u'Опыт модульного тестирования (с использованием PHPUnit).'),
                    _(u'Опыт разработки высоконагруженных систем.'),
                    _(u'Опыт работы с Redis, Mongodb.'),
                    _(u'Опыт реинженеринга програмных средств.'),
                ]
            ),
            JobPosition(
                company_name=_(u'Фриланс'),
                position=_(u'PHP Developer'),
                start_at=date(2011, 1, 1),
                leave_at=date(2011, 9, 1),
                responsibilities=[
                    _(u'Разработка backend и frontend частей приложений.'),
                ],
                achievements=[
                    _(u'Опыт работы с PHP MVC фреймворками.'),
                    _(u'Опыт работы с ORM.'),
                    _(u'Понимание принципов ООП.'),
                    _(u'Опыт командной работы с использованием SVN и Git.'),
                ]
            ),
            JobPosition(
                company_name=_(u'Фриланс'),
                position=_(u'UI Developer'),
                start_at=career_started_at,
                leave_at=date(2011, 9, 1),
                responsibilities=[
                    _(u'Разработка UI веб сайтов и веб приложений (используя XHTML 1.0 Strict/CSS 2.1, JavaScript).'),
                    _(u'Интеграция UI с CMS (DataLife Engine, WordPress, Drupal) и PHP фреймворками (Kohana).'),
                ],
                achievements=[
                    _(u'Опыт разработки UI.'),
                ]
            ),
        ]

        context.update({
            'job_positions': job_positions,
            'career_started_at': career_started_at,
        })

        return context
