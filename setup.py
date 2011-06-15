from setuptools import setup, find_packages
    
setup(
    name = 'django-dotpay',
    version = '0.1',
    author = 'Krzysztof Hoffmann',
    author_email = 'krzysiekpl@gmail.com',
    url = 'http://hoffmannkrzysztof.pl/',
    packages = ['dotpay',],
    zip_safe = False,
    install_requires = ['django',],
    license = 'MIT')