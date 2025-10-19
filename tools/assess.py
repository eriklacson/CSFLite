"""Tool for assessing security posture based on scan findings and governance manual governance checklist."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# import assess helper libraries
import tools.assess_helpers as assess
import tools.global_helpers as global_helpers

# import functions
__all__ = [*assess.__all__, "main"]


def main():
    paths = global_helpers.get_paths()

    """get input data"""
    # nuclei scan outputt
    findings = assess.read_scan_json(paths["scan_input_json"])

    """get reference data"""
    # CSF lookup
    csf_lookup = assess.get_csf_lookup(paths["csf_lookup"])

    # map scan findings to CSF
    mapped_scan = assess.map_scan_to_csf(findings, paths["lookup_csv"])

    # map governance check to CSF
    #
    # get check questionaire result
    governance_checklist_results = assess.get_governance_checklist_results(paths["governance_checklist"])

    # generate governance assessment

    # write scan findings
    global_helpers.write_to_csv(mapped_scan, paths["output_csv"])
    global_helpers.write_to_json(mapped_scan, paths["output_json"])

    # write scan heatmap
    scan_heatmap = assess.generate_scan_heatmap(mapped_scan, paths["heatmap_lookup"])
    global_helpers.write_to_csv(scan_heatmap, paths["heatmap_csv"])

    # write governance assessment
    governance_assessment = assess.generate_governance_assessement(governance_checklist_results, csf_lookup)
    global_helpers.write_to_csv(governance_assessment, paths["governance_assessment_csv"])

    goverance_heatmap = assess.generate_governance_heatmap(governance_assessment)
    global_helpers.write_to_csv(goverance_heatmap, paths["governance_heatmap_csv"])


if __name__ == "__main__":
    main()
