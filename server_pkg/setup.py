import sys

if sys.version_info[:2] < (3, 0):
    raise SystemExit("This package requires python3.")

try:
    import twisted
except ImportError:
    raise SystemExit("twisted not found.  Make sure you "
                     "have installed the Twisted core package.")

from distutils.core import setup

setup(
    name="watcher_server",
    version='0.0.1',
    author='Konjkov Vladimir',
    author_email='Konjkov.VV@gmail.com',
    url='https://github.com/Konjkov/SiberianPro',
    packages=['server', 'twisted.plugins'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: No Input/Output (Daemon)",
        "Programming Language :: Python",
    ]
)

# Make Twisted regenerate the dropin.cache, if possible.  This is necessary
# because in a site-wide install, dropin.cache cannot be rewritten by
# normal users.
try:
    from twisted.plugin import IPlugin, getPlugins
except ImportError:
    pass
else:
    list(getPlugins(IPlugin))
