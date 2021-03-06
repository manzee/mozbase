#!/usr/bin/env python

import os
import unittest
import proctest
import mozinfo
from mozprocess import processhandler

here = os.path.dirname(os.path.abspath(__file__))

class ProcTestWait(proctest.ProcTest):
    """ Class to test process waits and timeouts """

    def test_process_normal_finish(self):
        """Process is started, runs to completion while we wait for it"""

        p = processhandler.ProcessHandler([self.python, self.proclaunch, "process_normal_finish_python.ini"],
                                          cwd=here)
        p.run()
        p.wait()

        detected, output = proctest.check_for_process(self.proclaunch)
        self.determine_status(detected,
                              output,
                              p.proc.returncode,
                              p.didTimeout)

    def test_process_wait(self):
        """Process is started runs to completion while we wait indefinitely"""

        p = processhandler.ProcessHandler([self.python, self.proclaunch,
                                          "process_waittimeout_10s_python.ini"],
                                          cwd=here)
        p.run()
        p.wait()

        detected, output = proctest.check_for_process(self.proclaunch)
        self.determine_status(detected,
                              output,
                              p.proc.returncode,
                              p.didTimeout)


    def test_process_timeout(self):
        """ Process is started, runs but we time out waiting on it
            to complete
        """
        p = processhandler.ProcessHandler([self.python, self.proclaunch, "process_waittimeout_python.ini"],
                                          cwd=here)
        p.run(timeout=10)
        p.wait()

        detected, output = proctest.check_for_process(self.proclaunch)

        if mozinfo.isUnix:
            # process was killed, so returncode should be negative
            self.assertLess(p.proc.returncode, 0)

        self.determine_status(detected,
                              output,
                              p.proc.returncode,
                              p.didTimeout,
                              False,
                              ['returncode', 'didtimeout'])

    def test_process_waittimeout(self):
        """
        Process is started, then wait is called and times out.
        Process is still running and didn't timeout
        """
        p = processhandler.ProcessHandler([self.python, self.proclaunch,
                                          "process_waittimeout_10s_python.ini"],
                                          cwd=here)

        p.run()
        p.wait(timeout=5)

        detected, output = proctest.check_for_process(self.proclaunch)
        self.determine_status(detected,
                              output,
                              p.proc.returncode,
                              p.didTimeout,
                              True,
                              ())

    def test_process_waitnotimeout(self):
        """ Process is started, runs to completion before our wait times out
        """
        p = processhandler.ProcessHandler([self.python, self.proclaunch,
                                          "process_waittimeout_10s_python.ini"],
                                          cwd=here)
        p.run(timeout=30)
        p.wait()

        detected, output = proctest.check_for_process(self.proclaunch)
        self.determine_status(detected,
                              output,
                              p.proc.returncode,
                              p.didTimeout)

if __name__ == '__main__':
    unittest.main()
