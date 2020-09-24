#  -*- coding: utf-8 -*-
#***************************************************************************
#* Copyright (C) 2019-2020 by Andreas Langhoff                             *
#* <andreas.langhoff@frm2.tum.de>                                          *
#* This program is free software; you can redistribute it and/or modify    *
#* it under the terms of the GNU General Public License v3 as published    *
#* by the Free Software Foundation;                                        *
# **************************************************************************


from __future__ import print_function
import re
import os.path
from subprocess import PIPE, Popen
from datetime import datetime

__all__ = ['get_version']

RELEASE_VERSION_FILE = os.path.join(os.path.dirname(__file__),
                                    'RELEASE-VERSION')
GIT_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.git'))



def get_git_version(abbrev=0):
    try:

        p = Popen(['git', 'rev-list', '--all'],
                  stdout=PIPE, stderr=PIPE, cwd=GIT_REPO, shell=True)
        allrevisions, _stderr = p.communicate()

        lines = allrevisions.splitlines()

        latest = lines[0].decode('utf-8', 'ignore')

        p = Popen(['git', 'describe', '--tags', latest],
                  stdout=PIPE, stderr=PIPE, cwd=GIT_REPO)
        stdout, _stderr = p.communicate()

        version = stdout.decode('utf-8', 'ignore').split('-')
        GIT_LATEST_TAG = '0'
        if len(version) > 0:
            GIT_LATEST_TAG = version[0].strip(' \n')
        git_latest_tag = re.sub("[^0-9]", "", GIT_LATEST_TAG)
        GIT_NUMBER_OF_COMMITS_SINCE = '0'
        if len(version) > 1:
            GIT_NUMBER_OF_COMMITS_SINCE = version[1].strip(' \n')
            if len(GIT_NUMBER_OF_COMMITS_SINCE) == 0:
                GIT_NUMBER_OF_COMMITS_SINCE = '0'

        oneup = os.path.abspath(os.path.join(GIT_REPO, '..'))
        p = Popen(['git', 'diff', 'HEAD'],
                  stdout=PIPE, stderr=PIPE, cwd=oneup)
        stdout, _stderr = p.communicate()
        GIT_DIFF_HEAD = stdout.decode('utf-8', 'ignore')


        if GIT_DIFF_HEAD == '':
            p = Popen(['git', 'show', '-s', '--format=%cd', '--date=format:%Y-%m-%dT%H_%M%z'],
                      stdout=PIPE, stderr=PIPE, cwd=oneup)
            stdout, _stderr = p.communicate()
            GIT_DATE = stdout.decode('utf-8', 'ignore')
        else:
            now = datetime.now()
            GIT_DATE = 'Uncommitted-'+now.strftime("%Y-%m-%dT%H_%M%z")
        patch = ''
        if len(version) > 2:
            patch = version[2].strip(' \n')
        rv = git_latest_tag +'.'+GIT_NUMBER_OF_COMMITS_SINCE+'.'+re.sub(r'[^0-9a-f]', "", patch)+'_'+GIT_DATE
        return rv
    except Exception:
        return None


def read_release_version():
    try:
        with open(RELEASE_VERSION_FILE) as f:
            return f.readline().strip()
    except Exception:
        return None


def write_release_version(version):
    with open(RELEASE_VERSION_FILE, 'w') as f:
        f.write("%s\n" % version)


def get_version(abbrev=4):
    # determine the version from git and from RELEASE-VERSION
    git_version = get_git_version(abbrev)
    release_version = read_release_version()

    # if we have a git version, it is authoritative
    if git_version:
        if git_version != release_version:
            write_release_version(git_version)
        return git_version
    elif release_version:
        return release_version
    else:
        raise ValueError('Cannot find a version number - make sure that '
                         'git is installed or a RELEASE-VERSION file is '
                         'present!')


if __name__ == "__main__":
    print(get_version())
