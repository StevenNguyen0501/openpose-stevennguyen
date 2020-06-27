try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


class S3Url(object):
    def __init__(self, url):
        self._parsed = urlparse(url, allow_fragments=False)

    @property
    def bucket(self):
        return self._parsed.netloc

    @property
    def key(self):
        if self._parsed.query:
            return self._parsed.path.lstrip('/') + '?' + self._parsed.query
        else:
            return self._parsed.path.lstrip('/')

    @property
    def url(self):
        return self._parsed.geturl()

if __name__ == '__main__':
    s3_object = S3Url("https://fashion-shop-dev.s3.amazonaws.com/product/process/product_1588604019758.png")
    print(s3_object.key)