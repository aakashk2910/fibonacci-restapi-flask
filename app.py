from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_caching import Cache

config = {
    "DEBUG": True,           # some Flask specific configs
    "CACHE_TYPE": "simple",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
api = Api(app)
app.config.from_mapping(config)
cache = Cache(app)


@cache.cached(timeout=50, key_prefix='fibonacci')
def fibonacci(n):
    result = []
    a, b = 0, 1
    while b < n:
        if b >= 2:
            result.append(b)
        a, b = b, a + b
    return result


def findCombinations(arr, index, num, reducedNum, resultArr, fb):
    # Base condition
    if reducedNum < 0:
        return

    # If combination is found, add to subArr[] and later to resultArr[]
    if reducedNum == 0:
        for i in range(index):
            if arr[i] in fb:
                flag = 0
            else:
                flag = 1
                break
        if flag == 0:
            subArr = []
            for i in range(index):
                subArr.append(arr[i])
            resultArr.append(subArr)
        return

    # Find the previous number stored in arr[] which will help to maintain increasing order
    prev = 1 if (index == 0) else arr[index - 1]

    # loop starts from previous number, at array location index - 1
    for k in range(prev, num + 1):
        # next element of array is k
        arr[index] = k

        # call recursively with
        # reduced number
        findCombinations(arr, index + 1, num, reducedNum - k, resultArr, fb)


# Function to find out all combinations of numbers that add upto given input. It uses findCombinations()
#@cache.cached(timeout=50, key_prefix='main')
def main(n):
    # array to store the combinations
    # It can contain max n elements
    arr = [0] * n
    resultArr = []
    # find all combinations
    fb = fibonacci(n)
    findCombinations(arr, 0, n, n, resultArr, fb)
    return "["+','.join([str(elem) for elem in resultArr])+"]"


@app.route('/')
def welcome():
    return 'Welcome to Fibonnaci REST API'


@app.route('/fib/<int:n>')
def fib(n):
    return main(n)


@app.route('/health')
def healthcheck():
    return {'message': 'Healthy'}


if __name__ == '__main__':
    app.run(debug=True)
