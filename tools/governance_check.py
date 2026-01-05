"""Tool for assessing governance baseline from manual governance checklist."""

# import libraries
import argparse
import sys
from pathlib import Path
from typing import Iterable, Optional

# adjust path for relative imports when executed as script
if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parent.parent))

# import assess helper libraries
import tools.assess_helpers as assess
import tools.global_helpers as global_helpers

# import functions
__all__ = [*assess.__all__, "main"]


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    """Parse command line arguments for the Nuclei scanning CLI."""

    parser = argparse.ArgumentParser(description="CSFLite governance baseline assessment tool")
    parser.add_argument("--governance_checklist", type=str, help="Governance checklist CSV File")
    parser.add_argument("--governance_assessment", type=str, help="Governance assessment ouput the CSV")
    parser.add_argument("--governance_heatmap", type=str, help="Governance assessment heatmap ouput")

    return parser.parse_args(argv)


def validate_arguments(args: argparse.Namespace) -> None:
    """Validate that both arguments are provided."""
    if not args.nuclei_raw or not args.csflite_out:
        raise ValueError(
            "'--governance_checklist' '--governance_assessment' '--goverance_heatmap' arguments are required."
        )


def main(argv: Optional[Iterable[str]] = None) -> None:
    try:
        args = parse_args(argv)

        # Validate the arguments
        validate_arguments(args)

        # get reference file paths
        paths = global_helpers.get_paths()

        # get command line params
        governance_checklist = args.governance_checklist
        governance_assessment = args.governance_assessment
        governance_heatmap = args.governance_heatmap

        # get CSF lookup reference
        csf_lookup = assess.get_csf_lookup(paths["csf_lookup"])

        # map governance check to CSF
        #
        # get check questionaire result
        governance_checklist_results = assess.get_governance_checklist_results(governance_checklist)

        """generate governance assessment"""
        # write governance assessment score
        governance_assessment = assess.generate_governance_assessement(governance_checklist_results, csf_lookup)
        global_helpers.write_to_csv(governance_assessment, governance_assessment)

        # write governance assessment heatmap
        governance_heatmap = assess.generate_governance_heatmap(governance_assessment)
        global_helpers.write_to_csv(governance_heatmap, governance_heatmap)

    except ValueError as ve:
        print(f"Argument Error: {ve}", file=sys.stderr)


if __name__ == "__main__":
    main()
