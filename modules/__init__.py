
# modules/__init__.py

import sys
from modules.settings import BASE_DIR

# NOTE: To append modules

modules_dir = BASE_DIR / 'modules'
sys.path.append(str(modules_dir))
