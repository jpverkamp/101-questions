import requests


def makeMethod(name, f):

    def method(url, **kwargs):
        url = ('http://localhost:10177' + url).format(**kwargs)
        print('{name} {url} -- {data}'.format(
                name = name,
                url = url,
                data = kwargs['data'] if 'data' in kwargs else None
        ))

        if 'data' in kwargs:
                result = f(url, kwargs['data'])
        else:
                result = f(url)

        print('[{code}] {text}\n'.format(code = result.status_code, text = result.text))
        return result

    return method

get = makeMethod('GET', requests.get)
post = makeMethod('POST', requests.post)
put = makeMethod('PUT', requests.put)
delete = makeMethod('DELETE', requests.delete)

def parseFrequency(str):

    
