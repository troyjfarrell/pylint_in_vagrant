=================
Pylint In Vagrant
=================

Pylint is a great tool for keeping your Python code in order.  When using
Vagrant_ to develop an app inside a virtual machine, it is desirable to run
Pylint_ inside the virtual machine.  Pylint in Vagrant helps you do that.

.. _Vagrant: https://www.vagrantup.com/
.. _Pylint: http://pylint.pycqa.org/

Installation
============

Pylint in Vagrant installs like any other Python package, e.g., ``pip install
pylint_in_vagrant``.  It provides a command ``pylint-in-vagrant``.

Usage
=====

Common uses of Pylint in Vagrant include running it from the command line, from
pre-commit_ hooks and using it for developing Python applications for
Sandstorm_.

.. _pre-commit: https://pre-commit.com/
.. _Sandstorm: https://sandstorm.io/

Command-line Use
----------------

After installing Pylint in Vagrant into your Python environment, note a few
important values:
  - the directory where your code appears inside the virtual machine,
  - the directory where your ``Vagrantfile`` is located on your workstation and
  - the path to Pylint inside the virtual machine.

If you have a Vagrantfile in the current directory, Pylint in your path and you
want to lint a file at ``$HOME/path/to/python/module/file.py``, then you can
run ``pylint-in-vagrant pylint path/to/python/module/file.py``.

Pre-commit Use
--------------

To use Pylint in Vagrant with pre-commit, add a configuration like this::

    - repo: https://github.com/troyjfarrell/pylint_in_vagrant
      rev: v0.0.1
      hooks:
      - id: pylint_in_vagrant
        args: [/usr/local/bin/pylint]

The ``args`` list should include all arguments except for the list of files.
It must include the path to Pylint.

Pre-commit With Sandstorm
-------------------------

To use Pylint in Vagrant with pre-commit to develop a Sandstorm application,
try a configuration like this::

    - repo: https://github.com/troyjfarrell/pylint_in_vagrant
      rev: v0.0.1
      hooks:
      - id: pylint_in_vagrant
        args: [--prefix=/opt/app, --vagrant-dir=.sandstorm, /opt/app/venv/bin/pylint]

You may need to adjust the path to Pylint or the ``--prefix`` if your code is
in a different location.

How It Works
============

Pylint in Vagrant uses Vagrant's ``ssh`` command to run Pylint inside your
virtual machine.  You should use the command line arguments to specify the
appropriate paths.
