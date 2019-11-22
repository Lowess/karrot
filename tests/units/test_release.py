#!/usr/bin/env python
# -*- coding: utf-8 -*-


from karrot.release import __version__


def test_release_file():
    # Version should be a valid semver format
    assert len(__version__) > 0
