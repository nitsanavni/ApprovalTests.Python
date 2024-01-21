from hiker import global_answer, Hiker
from approvaltests.approvals import verify

# from approvaltests.reporters.report_on_cyber_dojo import ReportOnCyberDojo
from approvaltests import set_default_reporter
import pytest

# @pytest.fixture(autouse=True, scope='session')
# def setup():
#    set_default_reporter(ReportOnCyberDojo())

# if you want to change the expected result,
# move test_hiker.test_global.recieved.txt
# to   test_hiker.test_global.approved.txt
# to view the differences,
# open test_hiker.test_global.diff


def test_global():
    result = str(global_answer())
    verify(result)


def test_instance():
    result = str(Hiker().instance_answer())
    verify(result)


def instance_check():
    result = str(Hiker().instance_answer())
    verify(result)
