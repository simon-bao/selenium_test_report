# -*- coding: UTF-8 -*-

import datetime
import StringIO
import sys
import unittest
import json


__author__ = "Simon"
__version__ = "0.1.0"


class RollAppsTestRunner():
    """
    """
    STATUS = {
        0: 'pass',
        1: 'fail',
        2: 'error',
    }

    def __init__(self, stream=sys.stdout, verbosity=1, title=None, description=None, report_id=None):
        self.stream = stream
        self.verbosity = verbosity
        self.report_id = report_id
        if title is None:
            self.title = self.DEFAULT_TITLE
        else:
            self.title = title
        if description is None:
            self.description = self.DEFAULT_DESCRIPTION
        else:
            self.description = description

        self.startTime = datetime.datetime.now()


    def run(self, test):
        "Run the given test case or test suite."
        result = _TestResult(self.verbosity)
        test(result) # simon: from here, start to call unitest.suite.test
        self.stopTime = datetime.datetime.now()
        self.generateReport(test, result)
       # print >>sys.stderr, '\nTime Elapsed: %s' % (self.stopTime-self.startTime)
        return result


    def sortResult(self, result):
        # unittest does not seems to run in any particular order.
        # Here at least we want to group them together by class.
        result_list = result.result
        test_Result_list = []
        clsmap={}
        report_map = {}
        startTime = str(self.startTime)[:19]
        stopTime = str(self.stopTime)[:19]
        duration = str(self.stopTime - self.startTime)
        #result.success_count


        #检索result_list，并生成一个新的字典clsmap。
        self.scan_Results(clsmap, result_list)

        #将clsmap中的values，添加到rlist集合中
        for k in clsmap.keys():
            test_Result_list.append(clsmap[k])#完成详细测试结果数组的生成

        #生成最终的report_map(是个map，或者称为字典)
        report_map['startTime'] = startTime
        report_map['stopTime'] = stopTime
        report_map['duration'] = duration#测试所花费的时间
        report_map['testResults'] = test_Result_list
        report_map['success_ocunt'] = result.success_count
        report_map['failure_count'] = result.failure_count
        report_map['error_count'] = result.error_count
        report_map['report_id'] = self.report_id#来自于python的命令行参数，通常传入的是测试step的BUILD_TAG


        return report_map
    #def sum_Results(self):

    def scan_Results(self, clsmap, result_list):

        for n, t, o, e in result_list:

            # 获取测试类的名称及描述，并赋值到desc中
            cls = t.__class__
            if cls.__module__ == "__main__":
                clsname = cls.__name__
            else:
                clsname = "%s.%s" % (cls.__module__, cls.__name__)  # 获取class的名称，格式为classname或者modulename.classname
            clsdesc = cls.__doc__ and cls.__doc__.split("\n")[0] or ""  # 获取class的描述
            # desc = doc and '%s: %s' % (clsname, doc) or clsname

            # 获取测试方法的测试结果，并添加到所属测试类的集合中
            methodname = t.id().split('.')[-1]
            methoddesc = t.shortDescription() or ""
            # testdesc = testdoc and ('%s: %s' % (testname, testdoc)) or testname
            status = self.STATUS[n]

            # 新建一个method_Map
            method_Map = {"name": methodname, "desc": methoddesc, 'status': status, 'o': o, 'e': e}

            # 在clsmap字典里，添加元素
            if not clsmap.has_key(clsname):
                clsmap[clsname] = {"class": clsname, "desc": clsdesc, "method": []}
            # tmp = clsmap[clsname]
            # tmp["method"].append(method_Map)
            clsmap[clsname]["method"].append(method_Map)

    def generateReport(self, test, result):
        sortedResult = self.sortResult(result)
        # testx = result.success_count
        #report = self._generate_report(result)

        output = json.dumps(sortedResult)
        self.stream.write(output.encode('utf8'))
        #能不能有这一条，是个问题，原因是如果是多线程测试（如果有）的话，能否将这个流关闭
        #self.stream.close()

TestResult = unittest.TestResult
class _TestResult(TestResult):
    # note: _TestResult is a pure representation of results.
    # It lacks the output and reporting ability compares to unittest._TextTestResult.

    def __init__(self, verbosity=1):
        TestResult.__init__(self)
        self.stdout0 = None
        self.stderr0 = None
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.verbosity = verbosity

        # result is a list of result in 4 tuple
        # (
        #   result code (0: success; 1: fail; 2: error),
        #   TestCase object,
        #   Test output (byte string),
        #   stack trace,
        # )
        self.result = []


    def startTest(self, test):
        TestResult.startTest(self, test)
        # just one buffer for both stdout and stderr
        self.outputBuffer = StringIO.StringIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.stdout0 = sys.stdout
        self.stderr0 = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector


    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue()


    def stopTest(self, test):
        # Usually one of addSuccess, addError or addFailure would have been called.
        # But there are some path in unittest that would bypass this.
        # We must disconnect stdout in stopTest(), which is guaranteed to be called.
        self.complete_output()


    def addSuccess(self, test):
        self.success_count += 1
        TestResult.addSuccess(self, test)
        output = self.complete_output()
        self.result.append((0, test, output, ''))
        if self.verbosity > 1:
            sys.stderr.write('ok ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('.')

    def addError(self, test, err):
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.result.append((2, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('E  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E')

    def addFailure(self, test, err):
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('F  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')


class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """
    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(s)

    def writelines(self, lines):
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()

stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)