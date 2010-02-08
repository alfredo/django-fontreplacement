from distutils.core import setup

setup(name='django-fontreplacement',
      version='0.1-alpha',
      description='static image replacement for the templates',
      author='Alfredo Ramirez Aguirre',
      author_email='alfredo.django@gmail.com',
      url='http://github.com/alfredo/',
      packages=['fontreplacement', 'fontreplacement.templatetags'],
      classifiers=['Development Status :: 0.1 Alpha',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
      )
