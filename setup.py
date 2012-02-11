from setuptools import setup, find_packages
    
setup(
    name = 'django-dotpay',
    version = '0.2.6',
    author = 'Krzysztof Hoffmann',
    author_email = 'krzysiekpl@gmail.com',
    license='BSD',
    url = 'https://github.com/krzysiekpl/django-dotpay/',
    packages = ['dotpay','dotpay.sms','dotpay.payment'],
    )
