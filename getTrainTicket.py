# coding: utf-8

"""命令行火车票查看器

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 武汉 上海 2017-11-20
    tickets -dg 北京 南京 2017-11-20
"""
from docopt import docopt
from TrainsCollection import TrainsCollection
def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    print(type(arguments['<date>']))
    print(arguments['<date>'])
    # tc = TrainsCollection()
    # tc.getFormatData(arguments['<from>'],arguments['<to>'], arguments['<date>'])

def test():
    tc = TrainsCollection()
    tc.getFormatData('成都', '麻城', '2020-05-15')

if __name__ == '__main__':
    cli()
    # test()