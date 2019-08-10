
import argparse

if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("-u", "--url-pattern", type=str, help="Url")
    parse.add_argument("-s", "--start-index", default=1, type=int, help="Start Index default 1")
    parse.add_argument("-e", "--end-index", default=0, type=int, help="End Index default 0")
    parse.add_argument("-o", "--output", default="./pics", type=str, help="The output dir")
    parse.add_argument("--timeout", default=60, type=int, help="Timeout")

    args = parse.parse_args()
    if args.url_pattern != "":
        print("url_pattern args:", args.url_pattern)
    print("args:", args)
    print("args dict:", args.__dict__)

    print("list all args")
    for name in args.__dict__:
        print("%s:%s" % (name, args.__dict__[name]))