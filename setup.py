try:
    from setuptools import setup
except ImportError:
    # can't have the entry_points option here.
    from distutils.core import setup


required = []
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='tfchain',
      version='1.0.0',
      author="Ahmed T. Youssef",
      author_email="xmonader@gmail.com",
      description='pythonic tfchain client',
      long_description='pythonic tfchain client',
      packages=['tfchain'],
      url="https://github.com/xmonader/pytfchain",
      license='BSD 3-Clause License',
      install_requires=required,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
      ],
      )
