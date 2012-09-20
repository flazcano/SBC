.. SBC documentacion, creada por flazcano el Martes 11 de Septiembre del 2012.

=====================================
    SBC - Sistema Balaceador de Carga
=====================================

* Requires: Python 2.6 or 2.7 and psutil 0.6 or later

----

:Dev: `git repo <http://github.com/flazcano/SBC>`_
:Source: `sources code <https://github.com/flazcano/SBC/tarball/master/LEEME.rst>`_

----

***********************
    Docs / Instructions
***********************

please visit: https://github.com/flazcano/SBC/tree/master/doc

*******************
    Install / Setup
*******************

SBC can be installed from `PyPI <http://pypi.python.org/pypi/SBC>`_ using `pip <http://www.pip-installer.org>`_::
    
    pip install -U SBC

... or download the `source distribution from PyPI <http://pypi.python.org/pypi/SBC#downloads>`_, unarchive, and run::

    python setup.py install

... then use ``sh SBC.sh`` or ``sh AOC.sh`` to run the Server or Client.

****************************
    Detailed Install / Setup
****************************

These instructions are for Debian/Ubuntu Linux.  For other 
platforms, the setup is generally the same, with the exeption of 
installing system dependencies.  

----------------------
    SBC Server Install
----------------------

* install dependencies on Debian/Ubuntu::

    $ sudo aptitude install python python-argparse python-email python-xmpp
    
* install SBC from PyPI using Pip::

    $ sudo pip install -U SBC

* or install from `sources https://github.com/flazcano/SBC/tarball/master` and unarchive::

	$ tar zxvf SBC.tar.gz
    
* configure the SBC Server::

    $ nano SBC/sbc.conf
	
* load the Kernel Modules for IPTABLES::

	$ modprobe ip_conntrack
	$ modprobe ip_conntrack_ftp
	$ modprobe iptable_nat

* initialize the SBC Data Base::

    $ cd SBC/ && sh SBC.sh --createdb

* and run the SBC Server::

    $ cd SBC/; sh SBC.sh

* browse http://$IPSBC:DJANGOPORT/instalar and this redirect to http://$IPSBC:DJANGOPORT/admin/Web which is configured the Admin Web

:User: `admin`_
:Password: `4dm1n15tr4t0r`_

----------------------
    AOC Client Install
----------------------


* install dependencies on Debian/Ubuntu::

    $ sudo aptitude install python python-dev python-setuptools gcc
	
* install psutil 0.6 or later::
	
	$ sudo easy_install python-psutil
    
* install SBC from PyPI using Pip::

    $ sudo pip install -U SBC
	
* or install from `sources https://github.com/flazcano/SBC/tarball/master`::
	
	$ tar zxvf SBC.tar.gz

* configure the AOC Client::

	$ cd SBC/ && nano SBC/aoc.conf

* and run the AOC Client::

    $ cd SBC/; sh AOC.sh
