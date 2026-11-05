#!/usr/bin/env python3
"""
CLI for FCLR-010 forward validation
Validates against provided parquet path without retuning
"""

import sys
import json
import argparse
from pathlib import Path
import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent))
from fclr010_harness import FCLR010Harness


def main():
    parser = argparse.ArgumentParser(description='FCLR-010 Frozen Validation Harness')
    parser.add_argument('--data', type=Path, help='Path to new parquet data for validation')
    parser.add_argument('--pre-reg', type=Path, help='Pre-registration file (must exist before inspecting outcomes)')
    parser.add_argument('--output', type=Path, default=Path('research_state'), help='Output directory')
    parser.add_argument('--dry-run', action='store_true', help='Dry run without inspecting outcomes')

    args = parser.parse_args()

    harness = FCLR010Harness()
    config = harness.get_frozen_config()

    print("=== FCLR-010 FROZEN VALIDATION HARNESS ===")
    print(f"Experiment: {config['experiment_id']}")
    print(f"Primary contrast: {config['primary_contrast']} on {config['primary_metric']}")
    print(f"Bootstrap reps: {config['bootstrap_reps']}")
    print()

    if args.dry_run:
        print("DRY RUN - showing frozen config only")
        return

    if not args.pre_reg or not args.pre_reg.exists():
        print("ERROR: Pre-registration file required before inspecting outcomes on new data")
        print("Create research_state/experiment_prereg_LIQUIDATION_FORWARD_VALIDATE_004_<TIMESTAMP>.json first")
        sys.exit(1)

    if not args.data or not args.data.exists():
        print("ERROR: Data path required")
        sys.exit(1)

    print(f"Pre-reg: {args.pre_reg}")
    print(f"Data: {args.data}")
    print()
    print("Ready for validation with frozen harness (no retuning)")


if __name__ == '__main__':
    main()
