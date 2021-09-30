from unittest.suite import *
from unittest.suite import _call_if_exists, _DebugResult
from unittest.suite import TestSuite as TestSuiteSrc
import sys

# 重写TestSuite
class TestSuite(TestSuiteSrc):
    def _miniClassSetUp(self, test, result):
        pass

    def _handleClassSetUp(self, test, result):
        previousClass = getattr(result, '_previousTestClass', None)
        currentClass = test.__class__
        if currentClass == previousClass:
            return
        if result._moduleSetUpFailed:
            return
        if getattr(currentClass, "__unittest_skip__", False):
            return

        try:
            currentClass._classSetupFailed = False
        except TypeError:
            # test may actually be a function
            # so its class will be a builtin-type
            pass
        _miniClassSetUp = getattr(currentClass, '_miniClassSetUp', None)
        setattr(currentClass, "__is_minitest_suite__", True)
        if _miniClassSetUp is not None:
            _call_if_exists(result, '_setupStdout')
            try:
                _miniClassSetUp()
            except Exception as e:
                setattr(currentClass, "__minitest_class_setup_failure__", True)
                setattr(currentClass, "__minitest_class_setup_failure_why__", sys.exc_info())
                return
            finally:
                _call_if_exists(result, '_restoreStdout')
        super(TestSuite, self)._handleClassSetUp(test, result)
