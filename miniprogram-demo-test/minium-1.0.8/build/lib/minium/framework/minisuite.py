#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
Author:         lockerzhang
Filename:       minisuite.py
Create time:    2020/1/3 16:22
Description:

"""
import os
import json
import fnmatch
import logging.handlers

logger = logging.getLogger()


class MiniSuite:
    def __init__(self, suite_path=None):
        self.suite_json = {}
        if suite_path:
            if os.path.exists(suite_path):
                self.suite_json = json.load(open(suite_path, "rb"))
            else:
                logger.warning("test suite filename: %s not exists", suite_path)

    def get_case_config(self, cls_name, case_name):
        for pkg_cases in self.pkg_list:
            pkg = pkg_cases["pkg"]
            if fnmatch.fnmatch(cls_name, pkg):
                for case_info in pkg["case_list"]:
                    if isinstance(case_info, dict):
                        if fnmatch.fnmatch(case_info["name"], case_name):
                            return case_info.get("attr", dict())
        return dict()

    @property
    def pkg_list(self):
        return self.suite_json.get("pkg_list", list())
