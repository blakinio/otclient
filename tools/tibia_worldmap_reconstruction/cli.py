from __future__ import annotations

import argparse
from .pipeline import build_otbm_plan, compare, dump_json, load_json, reconstruct


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail-closed Tibia worldmap reconstruction helper")
    sub = parser.add_subparsers(dest="command", required=True)

    p_reconstruct = sub.add_parser("reconstruct")
    p_reconstruct.add_argument("--observations", required=True)
    p_reconstruct.add_argument("--catalog", required=True)
    p_reconstruct.add_argument("--mapping", required=True)
    p_reconstruct.add_argument("--output", required=True)

    p_compare = sub.add_parser("compare")
    p_compare.add_argument("--snapshot", required=True)
    p_compare.add_argument("--reference", required=True)
    p_compare.add_argument("--output", required=True)

    p_plan = sub.add_parser("plan-otbm")
    p_plan.add_argument("--snapshot", required=True)
    p_plan.add_argument("--output", required=True)

    args = parser.parse_args()
    if args.command == "reconstruct":
        dump_json(args.output, reconstruct(load_json(args.observations), load_json(args.catalog), load_json(args.mapping)))
    elif args.command == "compare":
        dump_json(args.output, compare(load_json(args.snapshot), load_json(args.reference)))
    elif args.command == "plan-otbm":
        dump_json(args.output, build_otbm_plan(load_json(args.snapshot)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
