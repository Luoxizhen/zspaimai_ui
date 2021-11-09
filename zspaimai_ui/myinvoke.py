# content of myinvoke.py
import pytest
python_file = "test/test_firstp.py"

class MyPlugin:
    def pytest_sessionfinish(self):
        print("*** test run reporting finishing")


pytest.main(["-x", "test/test_firstp.py::test_111", "--junitxml=reports/result1.xml"], plugins=[MyPlugin()])