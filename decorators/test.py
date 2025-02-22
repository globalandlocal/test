import requests
import time
import re
from random import randint
import functools

BOOK_PATH = 'https://www.gutenberg.org/files/2638/2638-0.txt'
def benchmark(func):
    """
    Декоратор, выводящий время, которое заняло выполнение декорируемой функции
    """
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args,**kwargs)
        end = time.perf_counter()
        print(f'Время выполнения функции {func.__name__}: {end-start}')
        print()
        return res
    return wrapper

def logging(func):
    """
    Декоратор, который выводит параметры с которыми была вызвана функция
    """

    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print('Функция вызвана с параметрами:')
        print(args,kwargs)
        print()
        return res

    return wrapper

def counter(func):
    """
    Декоратор, считающий и выводящий количество вызовов декорируемой функции
    """
    def wrapper(*args, **kwargs):
        wrapper.calls +=1
        res = func(*args, **kwargs)
        print(f'Функция была вызвана: {wrapper.calls} раз')
        print()
        return res
    wrapper.calls=0
    return wrapper

def memo(func):
  """
  Декоратор, запоминающий результаты исполнения функции func, чьи аргументы args должны быть хешируемыми
  """
  cache = {}
  @functools.lru_cache()
  def fmemo(*args):
      res = func(*args)
      return res
  fmemo.cache = cache
  return fmemo

def memo(func):
  """
  Декоратор, запоминающий результаты исполнения функции func, чьи аргументы args должны быть хешируемыми
  """
  cache = {}
  @functools.lru_cache
  def fmemo(*args):
      cache[hash(*args)] = func(*args)
      return func(*args)
  fmemo.cache = cache
  return fmemo


@counter
@logging
@benchmark
def word_count(word, url=BOOK_PATH):
    """
    Функция для посчета указанного слова на html-странице
    """

    # отправляем запрос в библиотеку Gutenberg и забираем текст
    raw = requests.get(url).text

    # заменяем в тексте все небуквенные символы на пробелы
    processed_book = re.sub(r'\W+' , ' ', raw).lower()

    # считаем
    cnt = len(re.findall(word.lower(), processed_book))

    return f"Cлово {word} встречается {cnt} раз"

print(word_count('whole'))
print()

def fib(n):
    if n < 2:
        return n
    return fib(n-2) + fib(n-1)

start = time.perf_counter()
fib(30)
end = time.perf_counter()
print(f'Время выполнения функции fib: {end - start}')

@memo
def fib(n):
    if n < 2:
        return n
    return fib(n-2) + fib(n-1)

start = time.perf_counter()
fib(30)
end = time.perf_counter()
print(f'Время выполнения функции fib: {end - start}')