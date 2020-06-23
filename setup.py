from setuptools import setup

setup(
    name='jsonate',
    version='0.7.0',
    
    author='James Robert',
    author_email='jiaaro@gmail.com',
    
    description=('Django library that can make ANYTHING into json'),
    long_description=open('README.markdown').read(),
    long_description_content_type="text/markdown",
    
    license='MIT',
    keywords='django json templatetags',
    
    url='http://jsonate.com',
    
    install_requires=[
        "django>=2.0",
    ],
    
    packages=[
        'jsonate', 
        'jsonate.templatetags',
    ],
    
    include_package_data=True,
    
    classifiers=[
    	'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ]
)
