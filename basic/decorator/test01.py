import time


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"func {func.__name__} took {end - start} seconds")
        return result
    return wrapper


@timer
def test01():
    time.sleep(2)
    return "test01"


example = test01()
print(example)




# 带参数的装饰器
def repeat(num):
    """
    :param num: 重复次数
    :return:
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(num):
                print(f"{i} times")
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def test02(name: str):
    time.sleep(2)
    return f"hello {name}"

result = test02('ZhangSan')

print(result)


