import argparse
import time
import threading
from reader.file_reader import SimpleFileReader

log_pattern = r'(?P<thread_id>\d+) \[(?P<thread_name>[^\]]+)\] (?P<level>[A-Z]+) +(?P<timestamp>.*) (?P<class_name>[^\s]+) \[\] - (?P<message>[^\n]+)(?:\n(?P<traceback>.*))?' 

def parse_args():
    parser = argparse.ArgumentParser(description="Read log files")
    parser.add_argument("filename", type=str, help="The file to read")
    return parser.parse_args()

def write_log_data(filename):
    log_data = '''2735 [main] INFO  2024-10-03T13:02:01.048 class.name [] - Error on java.lang.NullPointerException
Exception in thread "main" java.lang.NullPointerException
    at com.example.MyClass.myMethod(MyClass.java:23)
    at com.example.MyClass.main(MyClass.java:10)
Caused by: java.lang.IllegalArgumentException: Argument 'foo' must not be null
    at com.example.MyOtherClass.anotherMethod(MyOtherClass.java:15)
    at com.example.MyClass.myMethod(MyClass.java:22)
    ... 1 more
'''
    with open(filename, 'w') as _file:
        while True:
            _file.write(log_data)
            _file.flush()
            time.sleep(4)
            

def write_log_data_in_thread(filename):
    pass
    #threading.Thread(target=write_log_data, args=(filename,)).start()


def main():
    args = parse_args()
    simple_file_reader = SimpleFileReader(args.filename, log_pattern, line_pattern=r'(\d+).*')
    write_log_data_in_thread(args.filename)
    for log_entry in simple_file_reader.read():
        print(log_entry.data)

if __name__ == "__main__":
    main()