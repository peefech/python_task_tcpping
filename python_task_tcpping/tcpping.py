import sys
import socket
import time
import argparse
from attempt import Attempt
from timeit import default_timer as timer
from statistics import mean

parser = argparse.ArgumentParser()

parser.add_argument("hosts", type=str, help="Host for tcp ping",
                    metavar="HOSTS", nargs="+")

parser.add_argument("-p", "--ports", type=str, help="Port for tcp ping (default=53)", required=False,
                    default=53, metavar="PORT", nargs="+")

parser.add_argument("-c", "--count", type=int, help="max count of ping request (default=10)", required=False,
                    default=10, metavar='MAX_COUNT')

parser.add_argument("-t", "--timeout", type=float, help="ping timeout in seconds (default=1)", required=False,
                    default=1, metavar='TIME')

parser.add_argument("-i", "--interval", type=float, help="interval (default=1)", required=False,
                    default=1, metavar='INTERVAL')

args = parser.parse_args()

hosts = args.hosts
ports = args.ports
maxCount = args.count
timeout = args.timeout
interval = args.interval
count = 0

attempts = []
result = []


def get_results(current_attempts):
    passed = 0
    failed = 0
    times = []

    for attempt in current_attempts:
        if attempt.passed:
            passed += 1
            times.append(attempt.time)
        else:
            failed += 1

    times.sort()

    min_time = 0
    max_time = 0
    average = 0
    lRate = 0

    if passed != 0:
        lRate = passed / (passed + failed) * 100

    if passed != 0:
        min_time = "%.2f" % times[0]
        max_time = "%.2f" % times[-1]
        average = "%.2f" % mean(times)

    return (f"TCP Ping Results for port {port} and host {host}: Connections (Total/Pass/Fail): "
            f"[{passed + failed}/{passed}/{failed}] (Passed: {lRate}%), "
            f"Min time = {min_time}ms, Max time = {max_time}ms, Average time = {average}ms")


for host in hosts:
    for port in ports:
        while count < maxCount:
            count += 1
            new_attempt = Attempt(host, port, count)
            attempts.append(new_attempt)

            s = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            s_start = timer()

            try:
                s.connect((host, int(port)))
                s.shutdown(socket.SHUT_RD)
                time_1 = (1000 * (timer() - s_start))

                new_attempt.time = time_1

                print("Connected to %s[%s]: tcp_seq = %s time = %sms" % (host, port, count,
                                                                         "%.2f" % time_1))

                new_attempt.passed = True

            except socket.timeout:
                print("Connection timed out!")
            except OSError as e:
                print("OS Error:", e)
            if count < maxCount:
                time.sleep(interval)

        result.append(get_results(attempts))

        attempts = []
        count = 0
        if port != ports[-1]:
            print("------------------------------------------------------")

        time.sleep(1)

    print("======================================================")
    time.sleep(1)

for res in result:
    print(res)
