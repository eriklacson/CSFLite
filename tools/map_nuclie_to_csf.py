"""

Sanity testing for mapping Nuclie dataset to CSF format. Should be intergrated with nuc2csf tool. Will be deleted afterwards.

"""

import os
import sys

# ensure project root is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Local Helper Modules
import tools.nuclei_json_converter as nuclei_json_converter  # noqa: F401
