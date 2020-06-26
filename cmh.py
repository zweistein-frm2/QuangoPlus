#!/usr/bin/env python
import os
import sys
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if module_path not in sys.path:
    sys.path.append(module_path)
import quango.main
import cmh.quango_integration

sys.exit(cmh.quango_integration.run())

