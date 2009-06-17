This buildout relates the configuration of the application zope instance of the CommunesPlone central server.

The included external products are listed in buildout.cfg :
    - section [productdistros] (release form)
    - section [svnproducts] (svn form)

The directory 'parts/omelette/Products' contains (as links) all the used products. 

A "zope_add.conf" extends the generated zope.conf to add mount_points definition for example. 

The install process is described in the file : INSTALL.txt
