# Tips & tricks

## 1. Retrieve a module's path

```python
import a_module
# Returns the path to the pyc file that was loaded.
print(a_module.__file__)
```

## 2. Requests SSL error

Have you ever faced this kind of error?

```shell
    raise SSLError(e, request=request)
requests.exceptions.SSLError: HTTPSConnectionPool(host='xxxx', port=443): Max retries exceeded with url: xxxxxx (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:997)')))
```

This is a common and annoying issue. If you do a quick search, you might end up with something like this:

```python
requests.get("https://...", verify=False)
# or
requests.get("https://...", verify ='/path / to / certfile)
```

It's work, but it's more like a workaround. Beside that, if you use a library/framework, you can't update source code like this. In my case, stay behind proxy with certificate, then execute program in virtual environment, the root cause is the missing ceriticate in virtual environment. I've fixed with the following:

```shell
cat cert.pem >> <your-venv>/lib/python3.X/site-packages/certifi/cacert.pem
```
