# structural-signatures-2.0
Leaner, faster, better structural signatures generator

To start, untar the tar.gz file in the database folder and run structural-signatures-2.0.sh.

Next export the `homed` variable to be the installation directory of structural signatures, add it to your `.bashrc` if you want it automatically done, you can use the follow command on linux systems (Ubuntu, WSL) 

`$ pwd | sed -E "s/(.+)/export homed='\1'/gi"  >> ~/.bashrc`

## Dependancies
R >=3.0

Rscript

Perl >=5.22.8

Perl DBI

Perl Parrallel Fork Manager

sqlite >3.0
