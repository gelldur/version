#!/bin/python3
#
# pip install --user gitpython
#
# How to use this script
# ----------------------
# Please run it in your project root directory (git root of project)
# ./3rdparty/version/tool/release.py --dry-run --verbose --name=MyApp --pattern-name=revision

import logging
import git
import argparse
import common
from pprint import pprint

from versioning import *
from commit_weight import *
from bump_style import bump_version

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sha1", help="pass sha1 of commit which should be marked as release, by default HEAD")
    parser.add_argument(
        "--pattern-name", help="Example: revision, semantic")
    parser.add_argument(
        "--name", help="Example: MyApp")
    parser.add_argument(
        "--dry-run", help="Simulate what would be done", action="store_true")
    parser.add_argument(
        "--verbose", help="", action="store_true")

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger('release')
    ################################################################################################
    ################################################################################################
    versioning_patterns = load_versioning_patterns()

    prefix = '' if args.name is None else args.name + '-'

    repo = git.Repo(search_parent_directories=True)
    previous_release_tag = common.husk_previous_release(
        args.name, prefix, repo)

    if args.pattern_name is None:
        args.pattern_name = common.discover_versioning_style(
            versioning_patterns, previous_release_tag)

    if not common.check_versioning_style(args.pattern_name, versioning_patterns):
        exit(1)

    if previous_release_tag is not None and what_versioning(versioning_patterns, previous_release_tag) != args.pattern_name:
        logger.error("Different versioning!")
        raise Exception()

    start_commit, end_commit, commits_to_release_messages = common.get_commits_message(
        repo, None, previous_release_tag)

    if len(commits_to_release_messages) < 1:
        exit(0)

    new_release_tag = common.generate_new_version(start_commit, end_commit, args.pattern_name,
                                                  commits_to_release_messages, prefix,
                                                  previous_release_tag, versioning_patterns)
    if len(new_release_tag) < 1:
        exit(0)

    if not args.dry_run:
        repo.create_tag(new_release_tag, start_commit)
