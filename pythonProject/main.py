# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from requests.api import request
import json


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
def a():
    r = request('GET','http://www.baidu.com')
    r.json
    print(r.text)
    print(r.status_code)
    print(r.content)
    print(r.json('status_code'))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    a()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
