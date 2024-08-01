import time
from functools import wraps


def timer(func):
    def wrapper(*args, **kwargs):
        print(f"@@{timer.__name__}@@ running")
        print(f"func {func.__name__}:{func.__doc__}")
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"func {func.__name__} took {end - start} seconds")
        return result
    return wrapper


@timer
def test01():
    '''
    test function test01
    :return:
    '''
    time.sleep(2)
    return "test01"


example = test01()
print(example)


print("#############test02#############")

# 带参数的装饰器
def repeat(num):
    """
    :param num: 重复次数
    :return:
    """
    def decorator(func):

        # 使用wraps装饰器，如果不使用wraps装饰器，则装饰器中的函数名会丢失
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"@@{repeat.__name__}@@ running")
            print(f"func {func.__name__}:{func.__doc__}")
            for i in range(num):
                print(f"{i} times")
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@timer
@repeat(3)
def test02(name: str):
    """
    test function test02
    :param name:
    :return:
    """
    time.sleep(2)
    return f"hello {name}"


# 如果没有functools.wraps，则装饰器中的函数名会丢失
print(f"test02 func name: {test02.__name__}")
print(f"test02 func doc: {test02.__doc__}")

result = test02('ZhangSan')

print(result)


