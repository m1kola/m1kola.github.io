import os

if os.environ.get('APP_ENV', 'prod') == 'prod':
    from base.settings.env.prod import *  # NOQA
else:
    from base.settings.env.dev import *  # NOQA
