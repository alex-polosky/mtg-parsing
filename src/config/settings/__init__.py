import os
from .shared import *

match (env := os.environ.get('DJANGO_SETTINGS')):
    case None:
        pass
    case 'local':
        from .local import *
    case 'staging':
        from .staging import *
    case 'demo':
        from .demo import *
    case 'production':
        from .production import *

    case _:
        raise KeyError(f'No matching environment with name {env}')
