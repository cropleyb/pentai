pushd ../build/python/lib/

zip -d python27.zip "*xml*" "*pydoc*" "*tarfile*" "*wininst*" "tarfile*" "mailbox*""plat-mac*" "decimal*" "distutils*"
zip -d python27.zip smtplib.pyo aifc.pyo rfc822.pyo ftplib.pyo mhlib.pyo 
zip -d python27.zip httplib.pyo 
zip -d python27.zip imaplib.pyo "compiler*" locale.pyo cookielib.pyo optparse.pyo difflib.pyo argparse.pyo
zip -d python27.zip "*sql*"
zip -d python27.zip "*plat-mac*"

# ZODB 
zip -d python27.zip "*tests*" "*.rej" "*.py" "*.pyc" "*.c" "*.so.libs" "*.so.o"
zip -d python27.zip "*.txt" "*.test" "*.h" "*.so"

popd
