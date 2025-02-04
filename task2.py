import os.path as path
import re
import timeit
from hyperloglog import HyperLogLog
import pandas as pd

def load_data(filepath):
    ip_addresses = []
    with open(filepath, 'rt') as file:
        for line in file:
            # Використовуємо регулярний вираз для витягнення IP-адреси
            match = re.search(r'\d+\.\d+\.\d+\.\d+', line)
            if match:
                ip_addresses.append(match.group(0))
    return ip_addresses

def generate_set(ip_addresses):
    return set(ip_addresses)

def generate_hll(ip_addresses):
    hll = HyperLogLog(0.01)
    for ip in ip_addresses:
        hll.add(ip)
    return hll

def exact_count(ip_set):
    return len(ip_set)

def count_ips_hll(hll):
    return len(hll)

def to_time(sec):
    return f'{(sec * 1000):.4f}'

if __name__ == "__main__":
    file_name = path.dirname(__file__) + '/lms-stage-access.log'
    
    # Завантаження даних із лог-файлу
    ip_addresses = load_data(file_name)
    
    # Точний підрахунок
    set_start_populate = timeit.default_timer()
    ip_set = generate_set(ip_addresses)
    ip_set_count = '{0:.4f}'.format(exact_count(ip_set))
    set_duration_populate = timeit.default_timer() - set_start_populate
    set_duration_count = timeit.timeit(lambda: exact_count(ip_set), number=100)
    set_duration_total = set_duration_populate + set_duration_count

    # Підрахунок за допомогою HyperLogLog
    hll_start_populate = timeit.default_timer()
    ip_hll = generate_hll(ip_addresses)
    ip_hll_count = '{0:.4f}'.format(count_ips_hll(ip_hll))
    hll_duration_populate = timeit.default_timer() - hll_start_populate
    hll_duration_count = timeit.timeit(lambda: count_ips_hll(ip_hll), number=100)
    hll_duration_total = hll_duration_populate + hll_duration_count

    # Виведення результатів у вигляді таблиці
    results = {
        'Метод': ['Точний підрахунок', 'HyperLogLog'],
        'Унікальні елементи': [ip_set_count, ip_hll_count],
        'Час виконання (сек.)': [to_time(set_duration_total), to_time(hll_duration_total)]
    }
    
    df = pd.DataFrame(results)
    print("Результати порівняння:")
    print(df)
