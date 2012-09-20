.. SBC manual, creado por flazcano el miércoles, 19 de septiembre del 2012.

============================================
    Manual SBC - Sistema Balaceador de Carga
============================================

* Requisitos: Python 2.6 o 2.7 y psutil 0.6 o superior

----

:Desarrollo: `git repo <http://github.com/flazcano/SBC>`_
:Fuentes: `sources code <https://github.com/flazcano/SBC/tarball/master>`_

----

*********************************
    Documentación / Instrucciones
*********************************

favor visite: https://github.com/flazcano/SBC/tree/master/doc

*******************************
    Instalación / Configuración
*******************************

SBC puede ser instalado desde `PyPI <http://pypi.python.org/pypi/SBC>`_ usando `pip <http://www.pip-installer.org>`_::
    
    pip install -U SBC

... o descargando el `código fuente desde PyPI <http://pypi.python.org/pypi/SBC#downloads>`_, descomprima, y ejecute::

    python setup.py install

... a continuación utilice ``sh SBC.sh`` o ``sh AOC.sh`` para ejecutar el Servidor o Cliente.

*****************************************
    Instalación Detallada / Configuración
*****************************************

These instructions are for Debian/Ubuntu Linux.  For other 
platforms, the setup is generally the same, with the exeption of 
installing system dependencies.  

----------------------------
    SBC Instalación Servidor
----------------------------

* instale las dependencias en Debian/Ubuntu::

    $ sudo aptitude install python python-argparse python-email python-xmpp
    
* instale SBC desde PyPI using Pip::

    $ sudo pip install -U SBC

* o instale desde el `código fuente https://github.com/flazcano/SBC/tarball/master` y descomprima::

	$ tar zxvf SBC.tar.gz
    
* configure el Servidor SBC::

    $ nano SBC/sbc.conf
	
* cargue los Modulos del Kernel para IPTABLES::

	$ modprobe ip_conntrack
	$ modprobe ip_conntrack_ftp
	$ modprobe iptable_nat

* inicialize la Base de Datos de SBC::

    $ cd SBC/ && sh SBC.sh --createdb

* y ejecute el Servidor SBC::

    $ cd SBC/; sh SBC.sh

* ingrese a http://$IPSBC:DJANGOPORT/instalar y lo cual lo redirijirá a http://$IPSBC:DJANGOPORT/admin/Web con lo cual está configurada la administración Web:

:Usuario: `admin`_
:Clave: `4dm1n15tr4t0r`_
   
---------------------------
    AOC Instalación Cliente
---------------------------


* instale las dependencias en Debian/Ubuntu::

    $ sudo aptitude install python python-dev python-setuptools gcc
	
* instale psutil 0.6 o superior::
	
	$ sudo easy_install python-psutil

* instale SBC desde PyPI usando Pip::

    $ sudo pip install -U SBC
	
* o instale desde el `código fuente https://github.com/flazcano/SBC/tarball/master` y decomprima::
	
	$ tar zxvf SBC.tar.gz

* configure el Cliente AOC::

	$ cd SBC/ && nano SBC/aoc.conf

* y ejecute el Cliente AOC::

    $ cd SBC/; sh AOC.sh
