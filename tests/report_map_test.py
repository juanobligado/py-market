import random
import unittest

from runner.runner import ReportGenerator


class MyTestCase(unittest.TestCase):
    def test_report_gen(self):
        report = ReportGenerator()

        for i in range(0,999):
            report.add_point("agent 1", "usd",  random.randrange(80,110))
            report.add_point("agent 1", "asset",  random.randrange(80,110))
            report.add_point("agent 2", "usd",  random.randrange(80,110))
            report.add_point("agent 2", "asset",  random.randrange(80,110))

        report.plot()
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
