# UNIT TEST

- [UNIT TEST](#unit-test)
  - [1. Unit Test](#1-unit-test)
    - [1.1. Định nghĩa](#11-định-nghĩa)
    - [1.2. Lợi ích khi viết unit test](#12-lợi-ích-khi-viết-unit-test)
  - [2. Integration Test](#2-integration-test)
    - [2.1. Định nghĩa](#21-định-nghĩa)
    - [2.2. Mục đích](#22-mục-đích)
    - [2.3. Các loại Integration Test](#23-các-loại-integration-test)
  - [3. Testing trong Python](#3-testing-trong-python)
    - [3.1. Nguyên tắc](#31-nguyên-tắc)
    - [3.2. Cơ bản](#32-cơ-bản)
    - [3.3. Các công cụ](#33-các-công-cụ)
  - [4. Thư viện Unit Test trong Python](#4-thư-viện-unit-test-trong-python)
    - [4.1. Workflow chuẩn](#41-workflow-chuẩn)
    - [4.2. Một số định nghĩa quan trọng](#42-một-số-định-nghĩa-quan-trọng)
    - [4.3. Ví dụ bắt đầu](#43-ví-dụ-bắt-đầu)
    - [4.4. Giao diện Command-Line](#44-giao-diện-command-line)
    - [4.5. Test Discovery](#45-test-discovery)
    - [4.6. Tổ chức test code](#46-tổ-chức-test-code)
    - [4.7. Sử dụng lại test code](#47-sử-dụng-lại-test-code)
    - [4.8. Bỏ qua test và dự kiến lỗi](#48-bỏ-qua-test-và-dự-kiến-lỗi)
  - [5. Thư viện Mock trong Python](#5-thư-viện-mock-trong-python)
    - [5.1. Mocks aren't stubs](#51-mocks-arent-stubs)
      - [5.1.1. Regular Tests](#511-regular-tests)
      - [5.1.2. Test với Mock objects](#512-test-với-mock-objects)
      - [5.1.3. Sự khác nhau giữa Mocks và Stubs](#513-sự-khác-nhau-giữa-mocks-và-stubs)
      - [5.1.4. Classical and Mockist Testing](#514-classical-and-mockist-testing)
    - [5.2. Mock trong Python](#52-mock-trong-python)
    - [5.3. Mock class](#53-mock-class)
    - [5.4. Cấu trúc cơ bản của Mock class](#54-cấu-trúc-cơ-bản-của-mock-class)
  - [6. Tài liệu tham khảo](#6-tài-liệu-tham-khảo)

## 1. Unit Test

### 1.1. Định nghĩa

- Unit Test - Kiểm thử mức đơn vị
- Unit - Thành phần phần mềm nhỏ nhất có thể kiểm tra được - hàm, thủ tục, lớp và phương thức.
- "Thời gian tốn cho Unit Test sẽ được đền bù bằng việc tiết kiệm rất nhiều thời gian và chi phí cho việc kiểm tra và sửa lỗi ở các mức kiểm tra sau đó"
- Thường do LTV thực hiện.
- Mục đích: bảo đảm thông tin được xử lý và xuất là chính xác, trong mối tương quan với dữ liệu nhập và chức năng của Unit. Điều đó đòi hỏi tất cả các nhánh bên trong Unit đều phải kiểm tra để phát hiện nhánh phát sinh lỗi.

### 1.2. Lợi ích khi viết unit test

- Không phải cách hiệu quả để tìm kiếm bug/ phát hiện hồi quy(detect regression).

## 2. Integration Test

### 2.1. Định nghĩa

Integration test kết hợp các thành phần của một ứng dụng và kiểm tra như một ứng dụng đã hoàn thành. Trong khi Unit Test kiểm tra các thành phần và Unit riêng lẻ thì Intgration Test kết hợp chúng lại với nhau và kiểm tra sự giao tiếp giữa chúng.

### 2.2. Mục đích

- Phát hiện lỗi giao tiếp xảy ra giữa các Unit
- Tích hợp các Unit đơn lẻ thành các hệ thống con (subsystem) và cuối cùng là hệ thống hoàn chỉnh (system) chuẩn bị cho kiểm tra ở mức hệ thống (System Test)

### 2.3. Các loại Integration Test

- Kiểm tra cấu trúc (structure): Tương tự White Box Test (kiểm tra nhằm bảo đảm các thành phần bên trong của một chương trình chạy đúng), chú trọng đến hoạt động của các thành phần cấu trúc nội tại của chương trình chẳng hạn các lệnh và nhánh bên trong.
- Kiểm tra chức năng (functional): Tương tự Black Box Test (kiểm tra chỉ chú trọng đến chức năng của chương trình, không quan tâm đến cấu trúc bên trong), chỉ khảo sát chức năng của chương trình theo yêu cầu kỹ thuật.
- Kiểm tra hiệu năng (performance): Kiểm tra việc vận hành của hệ thống.
- Kiểm tra khả năng chịu tải (stress): Kiểm tra các giới hạn của hệ thống.

## 3. Testing trong Python

### 3.1. Nguyên tắc

- Testing unit nên tập trung chỉ vào một unit nhỏ và chứng mình được nó chính xác.
- Mỗi test unit phải hoàn toàn tách biệt. Mỗi test có thể được chạy tách biệt, và có thể chạy trong bộ phận kiểm tra, bất kể thứ tự được gọi. Việc thực thi nguyên tắc này nghĩa là mỗi test phải được load với 1 dữ liệu mới và có thể phải thực hiện việc clean sau đó. Được xử lý bởi 2 pt setUp() và tearDown().
- Cố gắng làm cho test chạy nhanh nhất có thể. Nếu có những heavier test cần được để tách biệt.
- Tìm hiểu các công cụ.
- Luôn chạy kiểm tra full test suite trước khi code, và chạy lại sau đó.
- Sử dụng teên dài và mô tả được chức năng cần test. Ví dụ: test_square_of_number_2()

### 3.2. Cơ bản

- Unittest: Module cơ bản trong bộ thư viện Python chuẩn. Tạo test case là lớp con của unittest.TestCase.
- Doctest: Module tìm kiếm từng phần của text

### 3.3. Các công cụ

- Py.test.
- Nose.
- Tox.
- Unittest2.
- Mock.

## 4. Thư viện Unit Test trong Python

### 4.1. Workflow chuẩn

- You define your own class derived from unittest.TestCase.
- Then you fill it with functions that start with ‘test_’.
- You run the tests by placing unittest.main() in your file, usually at the bottom.

### 4.2. Một số định nghĩa quan trọng

- *test fixture- : cho biết mọi sự chuẩn bị cần thiết để thực hiện các bài test.
- *test case- : đơn vị(unit) test nhỏ nhất, kiểm tra response cụ thể cho tập các đầu vào.  `unittest` cung cấp 1 class cơ bản, `TestCase`, được sử dụng để tạo ra các test cases.
- *test suite- : tập hợp các test cases, test suite hoặc cả 2. Thường được sử dụng khi có những test cần kết hợp cùng nhau.
- *test runner- : thành phần điều phối việc thực hiện test và biểu diễn kết quả cho user. Runner có thể có giao diện đồ họa, giao diện văn bản hoặc đơn thuần trả về một giá trị đặc biệt để cho biết kết quả thực hiện các test.

![Core classes in unittest.](http://twimgs.com/ddj/images/article/2014/0114/PythonUnitTest1.gif)

### 4.3. Ví dụ bắt đầu

Module `unittest` cung cấp tập các công cụ cho việc xây dựng và chạy tests.

Ví dụ:

  ```python
    import unittest

    class FooTest(unittest.TestCase):
        """Sample test case"""

        # preparing to test
        def setUp(self):
            """ Setting up for the test """
            print "FooTest:setUp_:begin"
            ## do something...
            print "FooTest:setUp_:end"

        # ending the test
        def tearDown(self):
            """Cleaning up after the test"""
            print "FooTest:tearDown_:begin"
            ## do something...
            print "FooTest:tearDown_:end"

        # test routine A
        def testA(self):
            """Test routine A"""
            print "FooTest:testA"

        # test routine B
        def testB(self):
            """Test routine B"""
            print "FooTest:testB"
  ```

![FooTest behavior](http://twimgs.com/ddj/images/article/2014/0114/PythonUnitTest3.gif)

- testcase được tạo ra bằng cách kế thừa `unittest.TestCase`.
- Phương thức bắt đầu bằng tiền tố test_.
- Phần then chốt là việc gọi đến các phương thức `assert*()`.
- Phương thức `setUp()` và `tearDown()` cho phép định nghĩa hướng dẫn sẽ được thực hiện trước và sau mỗi phương thức test.
- `unittest.main()` để chạy test.

### 4.4. Giao diện Command-Line

Có thể sử dụng giao diện command-line để chạy test từ modules, lớp hoặc từng phương thức test bất kỳ:

  ```bash
    python -m unittest test_module1 test_module2
    python -m unittest test_module.TestClass
    python -m unittest test_module.TestClass.test_method
  ```

Các options: -b, -c, -f có thể thấy được khi chạy:

  ```bash
    python -m unittest -h
  ```

### 4.5. Test Discovery

Unittest hỗ trợ test discorvery đơn giản - cho phép chạy nhiều test cùng một lúc.

### 4.6. Tổ chức test code

- Như đã nói ở trên, test cases được biểu diễn bởi nittest.TestCase` instances. Vì vậy, mọi test case đều phải kế thừa `TestCase` hoặc `FunctionTestCase`.
- Subclass đơn giản của `TestCase` chỉ là thực thi 1 phương thức test (test_*).

  ```python
    import unittest

    class DefaultWidgetSizeTestCase(unittest.TestCase):
        def test_default_widget_size(self):
            widget = Widget('The widget')
            self.assertEqual(widget.size(), (50, 50))
  ```

- Test có thể là số nhiều, được lặp lại. Sử dụng `setUp()` để định nghĩa các đối tượng đầu vào sử dụng trong test(kiểu như tạo môi trường cho test). Ví dụ, ở đây có thể *widget- được sử dụng trong nhiều phương thức test(trong cùng 1 test case) --> cần tối ưu hóa bằng việc thiết lập 1 đối tượng*widget- chung. Nếu `setUp()` raise 1 ngoại lệ khi test đang chạy --> Lỗi, test không được thực hiện.

  ```python
    import unittest

    class SimpleWidgetTestCase(unittest.TestCase):
        def setUp(self):
            self.widget = Widget('The widget')

        def test_default_widget_size(self):
            self.assertEqual(self.widget.size(), (50,50),
                             'incorrect default size')

        def test_widget_resize(self):
            self.widget.resize(100,150)
            self.assertEqual(self.widget.size(), (100,150),
                             'wrong size after resize')
  ```

- Tương tự, ta có `tearDown()` để dọn dẹp, xóa bỏ môi trường test. Nếu `setUp()` chạy thành công, `tearDown()` sẽ được chạy bất kể phương thức test có thành công hay không.
- Test case instances được nhóm lại với nhau dựa trên feature chúng test. `unittest` cung cấp cơ chế: *test suite*- - `unittest.TestSuite`. Trong phần lớn trường hợp, gọi `unittest.main()` sẽ thu thập các module test case và thực thi.
- Muốn tự xây dựng bộ test suite? Có thể sử dụng cách sau:

  ```python
    def suite():
        suite = unittest.TestSuite()
        suite.addTest(WidgetTestCase('test_default_size'))
        suite.addTest(WidgetTestCase('test_resize'))
        return suite
  ```

- Và tốt nhất, nên chia test ra module riêng.

### 4.7. Sử dụng lại test code

### 4.8. Bỏ qua test và dự kiến lỗi

- Unittest cho phép việc bỏ qua phương thức test và có thể cả lớp test. Thêm vào đó, unittest hỗ trợ đánh dấu 1 test chấp nhận lỗi, nếu test đó fail cũng không tính như là 1 failure trong `TestResult`.
- Sử dụng decorator.

    | Decorator                               | Giải thích                                                                     |
    | --------------------------------------- | ------------------------------------------------------------------------------ |
    | @unittest.skip(reason)                  | Bỏ qua vô điều kiện test, reason nên mô tả lí do bỏ qua.                       |
    | @unittest.skipIf(condition, reason)     | Bỏ qua test, nếu condition trả về True                                         |
    | @unittest.skipUnless(condition, reason) | Bỏ qua test trừ khi condition trả về True                                      |
    | @unittest.expectedFailure               | Đánh dấu test là chấp nhận Failure, nếu test fail sẽ không bị tính vào failure |

**Các lớp và hàm*- _ [Here](https://docs.python.org/3.4/library/unittest.html#classes-and-functions)

| Method                    | Checks that      | New in |
| ------------------------- | ---------------- | ------ |
| assertEqual(a, b)         | a == b           |        |
| assertNotEqual(a, b)      | a != b           |        |
| assertTrue(x)             | bool(x) is True  |        |
| assertFalse(x)            | bool(x) is False |        |
| assertIs(a, b)            | a is b           | 3.1    |
| assertIsNot(a, b)         | a is not b       | 3.1    |
| assertIsNone(x)           | x is None        | 3.1    |
| assertIsNotNone(x)        | x is not None    | 3.1    |
| assertIn(a, b)            | a in b           | 3.1    |
| assertNotIn(a, b)         | a not in b       | 3.1    |
| assertIsInstance(a, b)    | isinstance(a, b) | 3.2    |
| assertNotIsInstance(a, b) |                  | 3.2    |

| Method                                        | Checks that                                                    | New in |
| --------------------------------------------- | -------------------------------------------------------------- | ------ |
| assertRaises(exc, fun, *args, **kwds)         | fun(*args, **kwds) raises exc                                  |        |
| assertRaisesRegex(exc, r, fun, *args, **kwds) | fun(*args, **kwds) raises exc and the message matches regex r  | 3.1    |
| assertWarns(warn, fun, *args, **kwds)         | fun(*args, **kwds) raises warn                                 | 3.2    |
| assertWarnsRegex(warn, r, fun, *args, **kwds) | fun(*args, **kwds) raises warn and the message matches regex r | 3.2    |
| assertLogs(logger, level)                     | The with block logs on logger with minimumlevel                | 3.4    |

| Method                     | Checks that                                                                  | New in |
| -------------------------- | ---------------------------------------------------------------------------- | ------ |
| assertAlmostEqual(a, b)    | round(a-b, 7) == 0                                                           |        |
| assertNotAlmostEqual(a, b) | round(a-b, 7) != 0                                                           |        |
| assertGreater(a, b)        | a > b                                                                        | 3.1    |
| assertGreaterEqual(a, b)   | a >= b                                                                       | 3.1    |
| assertLess(a, b)           | a < b                                                                        | 3.1    |
| assertLessEqual(a, b)      | a <= b                                                                       | 3.1    |
| assertRegex(s, r)          | r.search(s)                                                                  | 3.1    |
| assertNotRegex(s, r)       | not r.search(s)                                                              | 3.2    |
| assertCountEqual(a, b)     | a and b have the same elements in the same number, regardless of their order | 3.2    |

| Method                     | Used to compare    | New in |
| -------------------------- | ------------------ | ------ |
| assertMultiLineEqual(a, b) | strings            | 3.1    |
| assertSequenceEqual(a, b)  | sequences          | 3.1    |
| assertListEqual(a, b)      | lists              | 3.1    |
| assertTupleEqual(a, b)     | tuples             | 3.1    |
| assertSetEqual(a, b)       | sets or frozensets | 3.1    |
| assertDictEqual(a, b)      | dicts              | 3.1    |

## 5. Thư viện Mock trong Python

### 5.1. Mocks aren't stubs

#### 5.1.1. Regular Tests

Ở testing bình thường, chủ yếu sử dụng `state verification`: chúng ta sẽ xác định ra phương thức test chạy bằng việc kiểm tra trạng thái - state của SUT(System Under Test) và collaborators sau khi phương thức được thực thi. Mock object cho phép tiếp cận vấn đề bằng phương pháp `behavior verification`.

#### 5.1.2. Test với Mock objects

Mock sử dụng `behavior verification`, cho biết mock điều chúng ta mong đợi đạt được khi thiết lập và yêu cầu mock xác minh lại chính nó trong quá trình xác minh(verification).

Về sự khác nhau giữa `state verification` và `behavior verification`:

- State verification: có 1 đối tượng được test 1 hành động nào đó, sau khi được chuẩn bị, cung cấp tất cả các collaborators cần thiết. Sau khi test hoàn thành, kiểm tra trạng thái/state của đối tượng và/hoặc collaborators, và xác minh xem nó có phải kết quả mong đợi không.
- Behavior verification: xác định chính xác những phương thức sẽ được SUT gọi đến trong collaborators, việc xác minh sẽ không phải là xác minh trạng thái kết thúc là chính xác, mà sẽ là trình tự các bước được thực hiện chính xác.

#### 5.1.3. Sự khác nhau giữa Mocks và Stubs

4 kiểu Test Double:

- *Dummy- object được pass, tuy nhiên không bao giờ được dùng thực sự. Thông thường chỉ được sử dụng để điền vào danh sách tham số.
- *Stubs- cung cấp câu trả lời được "đóng lại" để gọi trong lúc test, thường không phản hồi lại bất cứ thứ gì ngoài những thứ đã được lập trình sẵn trong test. Stubs cũng có thể ghi lại bản ghi thông tin về những lần gọi đến, chẳng hạn như 1 email gateway stub có thể ghi nhớ lại msgs mà nó gửi đi, hoặc số msgs nó gửi đi. Nói cách khác, stub biểu diễn 1 tập các phương thức interfaces cho test subject(tập các phương thức tương tự có thể thấy trong subject thực sự?). Khi test subject gọi đến phương thức stub, stub sẽ phản hồi lại với tập các kết quả đã định trước. Nó có thể sinh ra lỗi hoặc ngoại lệ, điều này cũng đã được định trước. Stub có thể theo dõi sự tương tác của nó với test subject, tuy nhiên chỉ trong phạm vi chương trình test.
- *Fake- object thực sự được sử dụng, tuy nhiên thường có 1 số shortcut khiến nó không thích hợp cho việc sản xuất ???(memory database). Fake biểu diễn 1 tập các phương thức interfaces, theo dõi sự tương tác với test subject. Không giống stub, fake thực xử lý dữ liệu đầu vào từ test subject, và đưa ra được kết quả dựa trên dữ liệu đó. __In short, a fake is a functional, but non-production version of the actual test resource. It lacks the checks and balances found in resource?__ Sử dụng thuật toán đơn giản, hiếm khi hoặc không bao giờ lưu trữ và dịch chuyển dữ liệu.
--> Với fake và stub, có thể test xem test subject gọi đúng phương thức với đầu vào đúng. Có thẻ test làm thế nào subject xử lý kết quả và lỗi/ngoại lệ. --> `state verification`.
--> Nếu muốn biết nếu test subject gọi đến cùng 1 phương thức 2 lần, hoặc phương thức được thực hiện đúng thứ tự? --> `behavior verification`
- *Mock- : đối tượng được xác định những kì vọng cần đạt được.

With fakes and stubs, you can test if the test subject called the right method with the right input. You can test how the subject handles the result and how it reacts to an error or exception. These tests are known as state verification. But what if you want to know if the test subject called the same method twice? What if you want to know if it called several methods in the proper order? Such tests are known as behavior verification, and to do them, you need mocks.

#### 5.1.4. Classical and Mockist Testing

- `Classical TDD` sử dụng đối tượng thực khi nào có thể, và đối tượng đúp (double) khi việc sử dụng đối tượng thực gặp vấn đề.
- `Mockist TDD` lúc nào cũng sử dụng mock cho bất kỳ đối tượng nào.

### 5.2. Mock trong Python

*Note: `mock` có trong bộ thư viện chuẩn từ Python3.3. Còn từ 3.3 đổ về 2.7, có trong thư viện `unittest.mock*

- Sử dụng Decorator, tuy nhiên phải chú ý đến thứ tự, theo chiều ngược lại. Ví dụ:

  ```python
      @mock.patch('mymodule.sys')
      @mock.patch('mymodule.os')
      @mock.patch('mymodule.os.path')
      def test_something(self, mock_os_path, mock_os, mock_sys):
          pass
  ```

- Hoặc có thể sử dụng `mock.create_autospec` để tạo ra 1 instance cho lớp được cung cấp.
- Hoặc [mock.Mock](http://www.voidspace.org.uk/python/mock/mock.html), [mock.MagicMock](http://www.voidspace.org.uk/python/mock/magicmock.html#magic-mock). Khi cần đưa ra sự lựa chọn giữa `mock.Mock`, `mock.MagicMock` và `mock.create_autospec`, luôn ưu tiên sử dụng auto-spec.

### 5.3. Mock class

![Mock class](http://twimgs.com/ddj/images/article/2014/0514/Python3.gif)

### 5.4. Cấu trúc cơ bản của Mock class

![Basic structure](http://twimgs.com/ddj/images/article/2014/0514/Python2.gif)

`Mock` class(green) có 2 lớp cha `NoneCallableMock` và `CallableMixin`. `NoneCallableMock` xác định ra routine cần thiết bằng các mock object. Nó sẽ ghi đè 1 số magic methods, cho chúng behavior mặc định? Và nó cũng cung cấp assert routines nhằm theo dõi, lần theo behavior của mock.  Đối với `CallableMixin`, nó cập nhật các magic methods giúp cho mock object có thể gọi được.

## 6. Tài liệu tham khảo

- [Unit test và Function test - Blog Duyet Dev](http://blog.duyetdev.com/2015/12/unit-test-va-function-test.html#.V2ZjaGh97IU)
- [Unit test và kinh nghiệm viết unit test](https://techmaster.vn/posts/33618/unit-test-dung-de-lam-gi-va-kinh-nghiem-viet-unit-test-tot-nhat)
- [Testing your code](http://docs.python-guide.org/en/latest/writing/tests/)
- [Unit test python](https://docs.python.org/3.4/library/unittest.html)
- [Mock Aren't Stubs](http://martinfowler.com/articles/mocksArentStubs.html)
- [Improve Your Python: Understanding Unit Testing](https://jeffknupp.com/blog/2013/12/09/improve-your-python-understanding-unit-testing/)
- [Introduction to Mocking in Python](https://www.toptal.com/python/an-introduction-to-mocking-in-python)
- [Using Mocks in Python](http://www.drdobbs.com/testing/using-mocks-in-python/240168251)
- [Python Mocking 101: Fake It Before You Make It](https://blog.fugue.co/2016-02-11-python-mocking-101.html)
