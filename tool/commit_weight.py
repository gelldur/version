import re
import logging

logger = logging.getLogger(__name__)


def get_list(text):
    split_list = [x.strip()
                  for x in text.split(',')]
    split_list = list(filter(None, split_list))
    return split_list


def contains(find_list, text):
    for element in find_list:
        if element in text:
            return True
    return False


def weight_of_commits_for_semantic(config, commits):
    major = 0
    minor = 0
    patch = 0

    markers_major = get_list(config['markers_major'])
    markers_minor = get_list(config['markers_minor'])
    markers_patch = get_list(config['markers_patch'])

    for commit_message in commits:
        if contains(markers_major, commit_message):
            major += 1
        elif contains(markers_minor, commit_message):
            minor += 1
        elif contains(markers_patch, commit_message):
            patch += 1
    if patch == 0 and len(commits) > 0:
        patch = 1
    logger.debug("Counted sematic changes: major:{} minor:{} patch:{}".format(
        major, minor, patch))
    if major > 0:
        return 1000000
    if minor > 0:
        return minor * 1000
    return patch


def weight_of_commits(versioning_patterns, versioning_style, commits):

    config_style = versioning_patterns[versioning_style]

    if versioning_style == 'semantic':
        return weight_of_commits_for_semantic(config_style, commits)
    elif versioning_style == 'revision':
        # Revision versioning is interested only in changes count
        return len(commits)
    return 0


#############################################################
# Quick test
# commit_major = 'Add Totally new version of app\n\n[MAJOR]\n\nFi far foo bar'
# commit_minor = 'Update log API\n\n[MINOR] Foo bar fo fo bar'
# commit_patch = 'Fix memory corruption\n\n[PATCH] Blah blah blah'
# commit_none = 'Refactor code\n\nWaiting too long with this change'

# assert weight_of_commits('semantic', [commit_major]) == 1000000
# assert weight_of_commits('semantic', [commit_minor]) == 1000
# assert weight_of_commits('semantic', [commit_patch]) == 1
# assert weight_of_commits('semantic', [commit_none]) == 1

# assert weight_of_commits('semantic', [commit_major, commit_major]) == 1000000
# assert weight_of_commits('semantic', [commit_minor, commit_minor]) == 2000
# assert weight_of_commits('semantic', [commit_patch, commit_patch]) == 2
# assert weight_of_commits('semantic', [commit_none, commit_none]) == 1

# assert weight_of_commits('semantic', [
#                          commit_major, commit_major, commit_minor]) == 1000000
# assert weight_of_commits('semantic', [
#                          commit_minor, commit_minor, commit_patch]) == 2000
# assert weight_of_commits('semantic', [
#                          commit_patch, commit_patch, commit_none]) == 2
# assert weight_of_commits('semantic', [
#                          commit_none, commit_none, commit_none]) == 1

# assert weight_of_commits('semantic', [
#                          commit_major, commit_major, commit_patch]) == 1000000
# assert weight_of_commits('semantic', [
#                          commit_minor, commit_minor, commit_major]) == 1000000
# assert weight_of_commits('semantic', [
#                          commit_patch, commit_minor, commit_none]) == 1000
# assert weight_of_commits('semantic', [
#                          commit_patch, commit_none, commit_none]) == 1
