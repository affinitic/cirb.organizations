README
======
Development buildout use a Oracle DB. For this, install (on Ubuuntu) libaio-dev::

  sudo apt-get install libaio-dev

After, it's a classical buildout install::

  $ git clone git@github.com:CIRB/cirb.organizations.git
  $ cd cirb.organizations
  $ virtualenv-2.6 .
  $ ./bin/python bootstrap.py
  $ ./bin/buildout -Nt 5
  $ ./bin/instance fg

Finaly create; go on http://localhost:8080, and add a plone site with the package *gscetterbeek.policy*
