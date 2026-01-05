"""Tool for assessing governance baseline from manual governance checklist."""

import sys

# import standard libraries
from pathlib import Path

# adjust path for relative imports when executed as script
if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parent.parent))

# import assess helper libraries
import tools.assess_helpers as assess
import tools.global_helpers as global_helpers

# import functions
__all__ = [*assess.__all__, "main"]


def main():
    paths = global_helpers.get_paths()

    # CSF lookup
    csf_lookup = assess.get_csf_lookup(paths["csf_lookup"])

    # map governance check to CSF
    #
    # get check questionaire result
    governance_checklist_results = assess.get_governance_checklist_results(paths["governance_checklist"])

    """generate governance assessment"""

    # write governance assessment
    governance_assessment = assess.generate_governance_assessement(governance_checklist_results, csf_lookup)
    global_helpers.write_to_csv(governance_assessment, paths["governance_assessment_csv"])

    goverance_heatmap = assess.generate_governance_heatmap(governance_assessment)
    global_helpers.write_to_csv(goverance_heatmap, paths["governance_heatmap_csv"])


if __name__ == "__main__":
    main()
