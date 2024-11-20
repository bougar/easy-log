from reader.file_reader import SimpleFileReader
import tempfile

def test_simple_file_reader_with_no_trace():
    log_pattern = r'(?P<thread_id>\d+) \[(?P<thread_name>[^\]]+)\] (?P<level>[A-Z]+) +(?P<timestamp>.*) (?P<class_name>[^\s]+) \[\] - (?P<message>.*)'
    log_data = '''2735 [main] INFO  2024-10-03T13:02:01.048 class.name [] - message'''
    expected_output = {
        'thread_id': '2735',
        'thread_name': 'main',
        'level': 'INFO',
        'timestamp': '2024-10-03T13:02:01.048',
        'class_name': 'class.name',
        'message': 'message',
    }
    temporary_file = tempfile.NamedTemporaryFile()
    with open(temporary_file.name, 'w') as file:
        file.write(log_data)
    simple_file_reader = SimpleFileReader(temporary_file.name, log_pattern)
    log_entry = next(simple_file_reader.read())
    simple_file_reader.close()
    assert log_entry.data == expected_output

def test_simple_file_reader_with_no_trace_with_more_than_one_line():
    log_pattern = r'(?P<thread_id>\d+) \[(?P<thread_name>[^\]]+)\] (?P<level>[A-Z]+) +(?P<timestamp>.*) (?P<class_name>[^\s]+) \[\] - (?P<message>.*)'
    log_data = '''2735 [main] INFO  2024-10-03T13:02:01.048 class.name [] - message'''
    expected_output = {
        'thread_id': '2735',
        'thread_name': 'main',
        'level': 'INFO',
        'timestamp': '2024-10-03T13:02:01.048',
        'class_name': 'class.name',
        'message': 'message',
    }
    temporary_file = tempfile.NamedTemporaryFile()
    with open(temporary_file.name, 'w') as file:
        file.write(log_data)
        file.write("\n")
        file.write(log_data)
        file.write("\n")
        file.write(log_data)
    simple_file_reader = SimpleFileReader(temporary_file.name, log_pattern)
    log_entry = next(simple_file_reader.read())
    assert log_entry.data == expected_output
    log_entry = next(simple_file_reader.read())
    assert log_entry.data == expected_output
    log_entry = next(simple_file_reader.read())
    simple_file_reader.close()
    assert log_entry.data == expected_output

def test_simple_file_reader_with_trace():
    log_pattern = r'(?P<thread_id>\d+) \[(?P<thread_name>[^\]]+)\] (?P<level>[A-Z]+) +(?P<timestamp>.*) (?P<class_name>[^\s]+) \[\] - (?P<message>[^\n]+)(\n(?P<traceback>.*))' 

    log_data = '''2735 [main] INFO  2024-10-03T13:02:01.048 class.name [] - message
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: division by zero'''
    expected_output = {
        'thread_id': '2735',
        'thread_name': 'main',
        'level': 'INFO',
        'timestamp': '2024-10-03T13:02:01.048',
        'class_name': 'class.name',
        'message': 'message',
        'traceback': 'Traceback (most recent call last):\n  File "<stdin>", line 1, in <module>\nZeroDivisionError: division by zero'
    }
    temporary_file = tempfile.NamedTemporaryFile()
    with open(temporary_file.name, 'w') as file:
        file.write(log_data)
    simple_file_reader = SimpleFileReader(temporary_file.name, log_pattern, line_pattern=r'(\d+).*')
    log_entry = next(simple_file_reader.read())
    simple_file_reader.close()
    assert log_entry.data == expected_output

def test_simple_file_reader_with_trace_multiple_times():
    log_pattern = r'(?P<thread_id>\d+) \[(?P<thread_name>[^\]]+)\] (?P<level>[A-Z]+) +(?P<timestamp>.*) (?P<class_name>[^\s]+) \[\] - (?P<message>[^\n]+)(\n(?P<traceback>.*))' 

    log_data = '''2735 [main] INFO  2024-10-03T13:02:01.048 class.name [] - message
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: division by zero'''
    expected_output = {
        'thread_id': '2735',
        'thread_name': 'main',
        'level': 'INFO',
        'timestamp': '2024-10-03T13:02:01.048',
        'class_name': 'class.name',
        'message': 'message',
        'traceback': 'Traceback (most recent call last):\n  File "<stdin>", line 1, in <module>\nZeroDivisionError: division by zero'
    }
    temporary_file = tempfile.NamedTemporaryFile()
    with open(temporary_file.name, 'w') as file:
        file.write(log_data)
        file.write("\n")
        file.write(log_data)
        file.write("\n")
        file.write(log_data)
        file.write("\n")
    simple_file_reader = SimpleFileReader(temporary_file.name, log_pattern, line_pattern=r'(\d+).*')
    log_entry = next(simple_file_reader.read())
    assert log_entry.data == expected_output
    log_entry = next(simple_file_reader.read())
    assert log_entry.data == expected_output
    log_entry = next(simple_file_reader.read())
    simple_file_reader.close()
    assert log_entry.data == expected_output