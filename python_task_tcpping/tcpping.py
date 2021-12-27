import sys
import socket
import time
import argparse
from timeit import default_timer as timer
from statistics import mean

parser = argparse.ArgumentParser()

parser.add_argument("host", type=str, help="Host for tcp ping",
                    metavar="HOST")

parser.add_argument("-p", "--port", type=str, help="Port for tcp ping (default=53)", required=False,
                    default=53, metavar="PORT")

parser.add_argument("-c", "--count", type=int, help="max count of ping request (default=10000)", required=False,
                    default=3, metavar='MAX_COUNT')

parser.add_argument("-t", "--timeout", type=float, help="ping timeout in seconds (default=1)", required=False,
                    default=1, metavar='TIME')

parser.add_argument("-i", "--interval", type=float, help="interval (default=1)", required=False,
                    default=1, metavar='INTERVAL')

args = parser.parse_args()

host = args.host
port = args.port
maxCount = args.count
timeout = args.timeout
interval = args.interval
count = 0

passed = 0
failed = 0
list_time = []


def get_results(times):
    lRate = 0
    if failed != 0:
        lRate = failed / count * 100

    min_time = "%.2f" % times[0]
    max_time = "%.2f" % times[-1]
    average = "%.2f" % mean(times)

    print("TCP Ping Results: Connections (Total/Pass/Fail): [{:}/{:}/{:}] (Passed: {:}%), "
          "Min time = {:}ms, Max time = {:}ms, Average time = {:}ms".
          format(count, passed, failed, str(100 - lRate), min_time, max_time, average))


while count < maxCount:
    count += 1
    s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s_start = timer()
    try:
        s.connect((host, int(port)))
        s.shutdown(socket.SHUT_RD)
        time_1 = (1000 * (timer() - s_start))
        list_time.append(time_1)
        print("Connected to %s[%s]: tcp_seq = %s time = %sms" % (host, port, count,
                                                                 "%.2f" % time_1))

        passed += 1
    except socket.timeout:
        print("Connection timed out!")
        failed += 1
    except OSError as e:
        print("OS Error:", e)
        failed += 1
    if count < maxCount:
        time.sleep(interval)

list_time.sort()
time.sleep(1)
get_results(list_time)
