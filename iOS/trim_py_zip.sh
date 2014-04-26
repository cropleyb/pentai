pushd ../build/python/lib/
#cp python27.zip.bak python27.zip
zip -d python27.zip "*xml*" "*pydoc*" "*tarfile*" "*wininst*" "tarfile*" "mailbox*""plat-mac*" "decimal*" "distutils*"
zip -d python27.zip smtplib.pyo aifc.pyo rfc822.pyo ftplib.pyo mhlib.pyo 
zip -d python27.zip httplib.pyo 
zip -d python27.zip imaplib.pyo "compiler*" locale.pyo cookielib.pyo optparse.pyo difflib.pyo argparse.pyo

#zipfile.pyo subprocess.pyo "multiprocessing*" 
zip -d python27.zip "*sql*"
zip -d python27.zip "*plat-mac*"
popd
