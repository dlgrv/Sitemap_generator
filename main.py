from multiprocessing import Process
from pysitemap import crawler
from asyncio import events, windows_events
import matplotlib.pyplot as plt
import sys
import logging
import time

links = {
    'craw': {'link': 'http://crawler-test.com/', 'time': 0, 'count_links': 0},
    'goog': {'link': 'http://google.com/', 'time': 0, 'count_links': 0},
    'vk': {'link': 'https://vk.com/', 'time': 0, 'count_links': 0},
    #'yndx': {'link': 'https://yandex.ru/', 'time': 0, 'count_links': 0},
    'stckovrfl': {'link': 'https://stackoverflow.com/', 'time': 0, 'count_links': 0}
}


def sitemap_gen(link, link_key):
    if '--iocp' in sys.argv:
        sys.argv.remove('--iocp')
        logging.info('using iocp')
        el = windows_events.ProactorEventLoop()
        events.set_event_loop(el)
    root_url = f'{link}'
    crawler(root_url, out_file=f'sitemap_{link_key}.xml')


def count_lines(filename, chunk_size=1<<13):
    with open(filename, encoding="utf-8") as file:
        return sum(chunk.count('\n')
                   for chunk in iter(lambda: file.read(chunk_size), ''))


if __name__ == '__main__':
    procs = []
    list_link_keys = links.keys()

    for link_key in list_link_keys:
        proc = Process(target=sitemap_gen, args=(links[link_key]['link'], link_key))
        start_time = time.time()
        proc.start()
        proc.join()
        stop_time = time.time()
        links[link_key]['time'] = format(stop_time - start_time, '.2f')

    '''
    # Данный способ гораздо эффективнее, но при нем я не понимаю, какой использовать метод для подсчета времени _(^^)_-
    for link_key in links:
        proc = Process(target=sitemap_gen, args=(links[link_key]['link'], link_key))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
    '''

    col_labels = ['URL сайта', 'Время обработки (сек)', 'Кол-во найденных ссылок', 'Имя файла с результатом']
    data = []

    fig, ax = plt.subplots()
    ax.set_axis_off()
    for link_key in list_link_keys:
        links[link_key]['count_links'] = count_lines(f'sitemap_{link_key}.xml') - 2
        data.append([links[link_key]['link'],
                     f"{links[link_key]['time']}",
                     links[link_key]['count_links'],
                     f'sitemap_{link_key}.xml'])

    the_table = ax.table(cellText=data,
                         rowLoc='right',
                         colLabels=col_labels,
                         loc='center')

    plt.savefig('result.png',
                dpi=150)

    plt.show()