import sys
import socket
import time
from timeit import default_timer as timer

host = None
port = 80

maxCount = 100
count = 0

try:
    host = sys.argv[1]
except IndexError:
    print("Usage: tcpping.py host [port] [maxCount]")
    sys.exit(1)

try:
    port = int(sys.argv[2])
except ValueError:
    print("Error: Port Must be Integer:", sys.argv[2])
    sys.exit(1)
except IndexError:
    pass

try:
    maxCount = int(sys.argv[3])
except ValueError:
    print("Error: Max Count Value Must be Integer", sys.argv[3])
    sys.exit(1)
except IndexError:
    pass

passed = 0
failed = 0


def get_results():
    print("TCP Ping Results: Connections (Total/Pass/Fail): [{:}/{:}/{:}]".format(count, passed, failed))


while count < maxCount:
    count += 1
    s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    s_start = timer()
    try:
        s.connect((host, int(port)))
        s.shutdown(socket.SHUT_RD)
        print("Connected to %s[%s]: tcp_seq = %s time = %sms" % (host, port, count,
                                                                 "%.2f" % (1000 * (timer() - s_start))))

        passed += 1
    except socket.timeout:
        print("Connection timed out!")
        failed += 1
    except OSError as e:
        print("OS Error:", e)
        failed += 1
    if count < maxCount:
        time.sleep(1)

get_results()
