================================================
    SBC - Sistema Balaceador de Carga
================================================

* Requires: Python 2.6 or 2.7

----

:Dev: `git repo <http://github.com/flazcano/SBC>`_

----

***********************
    Docs / Instructions
***********************

please visit: http://github.com/flazcano/SBC

*******************
    Install / Setup
*******************

SBC can be installed from `PyPI <http://pypi.python.org/pypi/SBC>`_ using `pip <http://www.pip-installer.org>`_::
    
    pip install -U SBC

... or download the `source distribution from PyPI <http://pypi.python.org/pypi/SBC#downloads>`_, unarchive, and run::

    python setup.py install

... then use ``SBC`` or ``AOC`` to run the Server or Client.

****************************
    Detailed Install / Setup
****************************

These instructions are for Debian/Ubuntu Linux.  For other 
platforms, the setup is generally the same, with the exeption of 
installing system dependencies.  

-----------------------
    SBC Server install
-----------------------

* install dependencies on Debian/Ubuntu::

    $ sudo apt-get install python-argparse python-smtplib python-email python-xmpp
    
* install SBC from PyPI using Pip::

    $ sudo pip install -U SBC
	
	or from source
	
	$ tar zxvf SBC.tgz
    
* configure the SBC Server::

    $ nano SBC/sbc.conf
	
* Load the Kernel Modules for IPTABLES

	$ modprobe ip_conntrack
	$ modprobe ip_conntrack_ftp
	$ modprobe iptable_nat

* initialize the SBC Data Base::

    $ SBC --createdb

* run the SBC Server::

    $ SBC

   
-----------------------
    AOC Client install
-----------------------


* install dependencies on Debian/Ubuntu::

    $ sudo apt-get install 
    
* install SBC from PyPI using Pip::

    $ sudo pip install -U SBC
	
	or from source
	
	$ tar zxvf SBC.tgz

* configure the AOC Client::

	$ nano SBC/aoc.conf

* run the AOC Client::

    $ AOC


-----------------------------------------------
    pip install latest dev branch from git repo
-----------------------------------------------

::

    pip install -e git+http://github.com/flazcano/SBC.git#egg=SBC