import unittest


class MyTest(unittest.TestCase):  # 继承unittest.TestCase
    def tearDown(self):
        # 每个测试用例执行之后做操作
        print('2')

    def setUp(self):
        # 每个测试用例执行之前做操作
        print('1')

    def test_run(self):
        # self.assertEqual(1,1)
        self.assertIs(1, 1)
        # 测试用例

    def test_run2(self):
        # self.assertEqual(1,1)
        self.assertIs(1, 1)
        # 测试用例

    def test_run3(self):
        # self.assertEqual(1,1)
        self.assertEqual(1, 8)
        # 测试用例

    def test_run1(self):
        # self.assertEqual(1,1)
        self.assertIs(1, 2)
        # 测试用例


if __name__ == '__main__':
    test_suite = unittest.TestSuite()  # 创建一个测试集合
    # test_suite.addTest(MyTest('test_run1'))  # 测试套件中添加测试用例
    # test_suite.addTest(MyTest('test_run2'))  # 测试套件中添加测试用例
    # test_suite.addTest(MyTest('test_run3'))  # 测试套件中添加测试用例
    suites = [MyTest('test_run1'), MyTest('test_run2'), MyTest('test_run3')]
    test_suite.addTests(suites)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)
