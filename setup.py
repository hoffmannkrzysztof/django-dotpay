from setuptools import setup, find_packages
    
setup(
    name = 'django-dotpay',
    version = '0.2',
    author = 'Krzysztof Hoffmann',
    author_email = 'krzysiekpl@gmail.com',
    url = 'https://django-dotpay.googlecode.com/svn/trunk/',
    packages = ['dotpay','dotpay.sms','dotpay.payment'],
    zip_safe = False,
    install_requires = ['django',],
    license = 'MIT')
