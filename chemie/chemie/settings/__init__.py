import os
import sys


TESTING = 'test' in sys.argv[:2]

if TESTING:
    from .test import *

else:
    if os.environ.get('PRODUCTION') == 'True':
        from .production import *
    else:
        try:
            from .local import *
        except ImportError as e:
            raise ImportError("Couldn't load local settings chemie.chemie.settings.local")