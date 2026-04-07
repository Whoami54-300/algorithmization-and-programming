from collections import defaultdict, Counter

def parse_line(line):
    parts = line.split()

    ip = parts[0]

    # "GET /api/users HTTP/1.1"
    request = line.split('"')[1]
    method, path, protocol = request.split()

    status = int(parts[-3])
    size = int(parts[-2])

    return ip, path, status, size


def analyze_logs(file_path):
    ip_counter = Counter()
    status_counter = Counter()
    path_counter = Counter()
    total_size = 0

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            ip, path, status, size = parse_line(line)

            ip_counter[ip] += 1
            status_counter[status] += 1
            path_counter[path] += 1
            total_size += size

    return ip_counter, status_counter, path_counter, total_size

def print_results(ip_counter, status_counter, path_counter, total_size):
    total_requests = sum(ip_counter.values())

    print("Топ 5 IP:")
    for ip, count in ip_counter.most_common(5):
        percent = count / total_requests * 100
        print(f"{ip} - {count} ({percent:.1f}%)")

    print("\nСтатус-коды:")
    for status, count in status_counter.items():
        percent = count / total_requests * 100
        print(f"{status} - {count} ({percent:.1f}%)")

    print("\nТоп путей:")
    for path, count in path_counter.most_common(3):
        print(f"{path} - {count}")

    print(f"\nОбщий размер: {total_size}")