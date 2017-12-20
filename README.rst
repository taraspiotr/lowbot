=========================
 lowbot project
=========================



Licenses
========

The code which makes up this Python project template is licensed under the MIT/X11 license. Feel free to use it in your free software/open-source or proprietary projects.

The template also uses a number of other pieces of software, whose licenses are listed here for convenience. It is your responsibility to ensure that these licenses are up-to-date for the version of each tool you are using.

+------------------------+----------------------------------+
|Project                 |License                           |
+========================+==================================+
|Python itself           |Python Software Foundation License|
+------------------------+----------------------------------+
|argparse (now in stdlib)|Python Software Foundation License|
+------------------------+----------------------------------+
|Sphinx                  |Simplified BSD License            |
+------------------------+----------------------------------+
|Paver                   |Modified BSD License              |
+------------------------+----------------------------------+
|colorama                |Modified BSD License              |
+------------------------+----------------------------------+
|flake8                  |MIT/X11 License                   |
+------------------------+----------------------------------+
|mock                    |Modified BSD License              |
+------------------------+----------------------------------+
|pytest                  |MIT/X11 License                   |
+------------------------+----------------------------------+
|tox                     |MIT/X11 License                   |
+------------------------+----------------------------------+

Issues
======

Please report any bugs or requests that you have using the GitHub issue tracker!

Development
===========

If you wish to contribute, first make your changes. Then run the following from the project root directory::

    source internal/test.sh

This will copy the template directory to a temporary directory, run the generation, then run tox. Any arguments passed will go directly to the tox command line, e.g.::

    source internal/test.sh -e py27

This command line would just test Python 2.7.

Authors
=======

* Sean Fisk
* Benjamin Schwarze
