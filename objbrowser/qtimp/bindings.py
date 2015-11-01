""" Loads PyQT or PySide. 
    If an IPython session is running that already has QT imported, that is used.
    
    TBD: how to force IPython2 to use the QT sip 2 API?
    Test cases:
        python2
        python3
        ipython2
        ipython3
        ipython2 gui=qt
        ipython3 qui=qt
        ipython3 qui=gtk
        ipython (interactive)
        
    1) detect running QT
    2) If not yet running: start QT
    3) If IPython check if event loop is running.

"""
#IPython.external.qt_for_kernel # has side effect of importing the QT
#IPython.lib.guisupport.get_app_qt4 # has side effect of importing the QT (import qt_for_kernel)
#from IPython.external.qt_for_kernel import QtGui
#from IPython.external.qt_for_kernel import get_options  
#from IPython.external.qt_loaders import loadQt, loaded_api

import os, sys
import logging
logger = logging.getLogger(__name__)

#from interactive import *

# Available APIs taken from IPython.external.qt_loaders
#QT_API_PYQT = 'pyqt'
#QT_API_PYQT5 = 'pyqt5'
#QT_API_PYQTv1 = 'pyqtv1'
#QT_API_PYQT_DEFAULT = 'pyqtdefault' # don't set SIP explicitly
#QT_API_PYSIDE = 'pyside'

ACTIVE_BINDINGS = None
BINDINGS_PYQT = 'pyqt'
BINDINGS_PYSIDE = 'pyside'
VALID_BINDINGS = (BINDINGS_PYQT, BINDINGS_PYSIDE)
    

def use_v2_api():
    import sip
    try:
        sip.setapi('QString', 2)
        sip.setapi('QVariant', 2)
    except ValueError as ex:
        raise ValueError("Unable to load PyQt4 ({}). ".format(ex) + 
            "Try setting the QT_API environment variable to 'pyqt'")
        
    # The following APIs are set to 1 by IPython2 regardles of the QT_API environment var.
    # Version 2 therefore cannot be used when using IPython2 GUI integration.
    #sip.setapi('QDate', 2)  
    #sip.setapi('QDateTime', 2)
    #sip.setapi('QTextStream', 2)
    #sip.setapi('QTime', 2)
    #sip.setapi('QUrl', 2)        


    
def determineQtBindings(bindings=None):
    """ Determines which Qt bindings to use.
    
        This is determined from (in order of precedence):
        1) If the bindings parameter is set (to 'pyqt' or 'pyside') it is ued.
        2) A --use-pyqt or --use-pyside is a command line option (from sys.argv)
        3) If one of the valid binding is already imported, this is used.
        4) If the QT_API environment variable is set, this is used.
        5) Try to import PyQt4, otherwise try to import PySide.
    
        Returns string: 'pyqt' or 'pyside'
    
        Returns the imported QtCore, QtGui and ACTIVE_BINDINGS as a tuple.
        Raises ImportError in case the bindings are not installed.
    """
    if bindings:
        logger.info("Loading {} (explicitly selected)".format(bindings))
        return bindings
        
    if '--use-pyqt' in sys.argv:
        logger.info("Loading pyqt (--use-pyqt command line option)")
        return BINDINGS_PYQT
    
    if '--use-pyside' in sys.argv:
        logger.info("Loading pyside (--use-pyside command line option)")
        return BINDINGS_PYSIDE
    
    # If one of the valid binding is already imported, use this.
    # If IPython is started with --gui=qt, the bindings will be present in sys.modules as well.
    # To keep it simple we therefore do not use IPython.external.qt_loaders.loaded_api 
    if 'PyQt4' in sys.modules:
        logger.info("Using {} (was already imported)".format(BINDINGS_PYQT))
        return BINDINGS_PYQT
    if 'PySide' in sys.modules:
        logger.info("Using {} (was already imported)".format(BINDINGS_PYSIDE))
        return BINDINGS_PYSIDE
    
    # Is checked after installed module because it would otherwise be difficult
    # to override. Calling loadQt from another program that doesn't check the QT_API 
    # environment variable would give conflicts.
    env_qt_api = os.environ.get('QT_API', None)
    if env_qt_api:
        if env_qt_api in VALID_BINDINGS:
            logger.info("Loading {} (from QT_API environment variable)".format(env_qt_api))
            return env_qt_api
        else:
            logger.warn("Ignored invalid QT_API environment variable: {}".format(env_qt_api))
            
    return None
    
    
detect_bindings = determineQtBindings(BINDINGS_PYSIDE) # TODO: remove
logger.debug("Importing Qt (selected bindings = {!r})".format(detect_bindings))
if detect_bindings == BINDINGS_PYQT:
    use_v2_api()        
    from PyQt4 import QtCore, QtGui
    ACTIVE_BINDINGS = BINDINGS_PYQT
    
elif detect_bindings == BINDINGS_PYSIDE:
    from PySide import QtCore, QtGui
    ACTIVE_BINDINGS = BINDINGS_PYSIDE
    
elif detect_bindings is None:
    logger.debug("No Qt bindings running or selected. Will try to use PyQt4 first, then PySide.")
    try:
        from PySide import QtCore, QtGui
        ACTIVE_BINDINGS = BINDINGS_PYSIDE    
    except ImportError:
        use_v2_api()        
        from PyQt4 import QtCore, QtGui
        ACTIVE_BINDINGS = BINDINGS_PYQT

else:
    raise ValueError("Invalid Qt bindings {!r}. Must be one of: {}"
                     .format(detect_bindings, VALID_BINDINGS))

logger.debug("Imported Qt: (bindings = {!r})".format(ACTIVE_BINDINGS))          
assert ACTIVE_BINDINGS, "ACTIVE_BINDINGS"


def main():

    fmt = '%(filename)25s:%(lineno)-4d : %(levelname)-7s: %(message)s'
    logging.basicConfig(level='DEBUG', format=fmt)
    
    logger.info("QT_API: {}".format(ACTIVE_BINDINGS))

    #api_version = qtapi_version()
    #logger.debug("PyQt API version: {!r}".format(api_version))

if __name__ == "__main__":
    main()
    
