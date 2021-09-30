import sys
from unittest.case import *
from unittest.case import _Outcome
from unittest.case import TestCase as TestCaseSrc


# 重写testcase
class TestCase(TestCaseSrc):
    def _callSetUp(self):
        # self._miniSetUp()
        self.setUp()

    def _miniSetUp(self):
        pass

    def _callTearDown(self):
        # self._miniTearDown()
        self.tearDown()

    def _miniTearDown(self):
        pass

    def run(self, result=None):
        orig_result = result
        if result is None:
            result = self.defaultTestResult()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()

        result.startTest(self)

        testMethod = getattr(self, self._testMethodName)
        if (getattr(self.__class__, "__unittest_skip__", False) or
                getattr(testMethod, "__unittest_skip__", False)):
            # If the class or method was skipped.
            try:
                skip_why = (getattr(self.__class__, '__unittest_skip_why__', '')
                            or getattr(testMethod, '__unittest_skip_why__', ''))
                self._addSkip(result, self, skip_why)
            finally:
                result.stopTest(self)
            return

        expecting_failure_method = getattr(testMethod,
                                           "__unittest_expecting_failure__", False)
        expecting_failure_class = getattr(self,
                                          "__unittest_expecting_failure__", False)
        expecting_failure = expecting_failure_class or expecting_failure_method
        outcome = _Outcome(result)
        try:
            self._outcome = outcome
            if getattr(self.__class__, "__minitest_class_setup_failure__", False):
                exc_info = getattr(self.__class__, "__minitest_class_setup_failure_why__", sys.exc_info())
                self._outcome.success = False
                self._outcome.errors.append((self, exc_info))
                result.addError(self, exc_info)
                return result

            with outcome.testPartExecutor(self):
                self._miniSetUp()
            if outcome.success:
                with outcome.testPartExecutor(self):
                    self._callSetUp()
                if outcome.success:
                    outcome.expecting_failure = expecting_failure
                    with outcome.testPartExecutor(self, isTest=True):
                        self._callTestMethod(testMethod)
                    outcome.expecting_failure = False
                    with outcome.testPartExecutor(self):
                        self._callTearDown()
            outcome.expecting_failure = False
            with outcome.testPartExecutor(self):
                self._miniTearDown()

            self.doCleanups()
            for test, reason in outcome.skipped:
                self._addSkip(result, test, reason)
            self._feedErrorsToResult(result, outcome.errors)
            if outcome.success:
                if expecting_failure:
                    if outcome.expectedFailure:
                        self._addExpectedFailure(result, outcome.expectedFailure)
                    else:
                        self._addUnexpectedSuccess(result)
                else:
                    result.addSuccess(self)
            return result
        finally:
            result.stopTest(self)
            if orig_result is None:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()

            # explicitly break reference cycles:
            # outcome.errors -> frame -> outcome -> outcome.errors
            # outcome.expectedFailure -> frame -> outcome -> outcome.expectedFailure
            outcome.errors.clear()
            outcome.expectedFailure = None

            # clear the outcome, no more needed
            self._outcome = None
