import re

# Regex pattern to capture logs with optional multiline tracebacks
log_pattern = re.compile(
    r'(?P<thread_id>\d+) \[(?P<thread_name>[^\]]+)\] (?P<level>[A-Z]+) +(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}) '
    r'(?P<class_name>[^\s]+) \[\] - (?P<message>[^\n]+)'  # Capture message until end of line
    r'(\n(?P<traceback>(?!\d+ \[).+?))*(?=\n\d+ \[|$)',  # Capture traceback until the next log line or end of input
    re.DOTALL
)

def parse_logs_with_traceback(logs):
    log_entries = []
    
    # Find all matches in the logs
    for match in log_pattern.finditer(logs):
        log_dict = match.groupdict()
        log_entries.append(log_dict)
    
    return log_entries


# Example logs with and without tracebacks
logs = '''2735 [main] INFO  2024-10-03T13:02:01.048 class.name [] - This is a test message
2736 [main] INFO  2024-10-03T13:02:01.049 class.name [] - Another message with no traceback
2737 [main] ERROR 2024-10-03T13:02:01.050 class.name [] - An error occurred
Some additional error details
2738 [main] INFO  2024-10-03T13:02:01.051 class.name [] - Yet another log
This is a continuation of an error that doesn't have a stack trace.
2739 [main] INFO  2024-10-03T13:02:01.052 class.name [] - Last log without issues'''

parsed_logs = parse_logs_with_traceback(logs)

for entry in parsed_logs:
    print("Log Entry:", entry['thread_id'], entry['message'])
    print("Traceback:", entry['traceback'])
    print("---")
