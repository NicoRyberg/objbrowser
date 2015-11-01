
import logging
logger = logging.getLogger(__name__)

from .bindings import QtGui


def in_ipython():
    """ Returns True if IPython is running, False for the regular Python.
    """
    try:
        from IPython.core.getipython import get_ipython
    except ImportError:
        return False
    else:
        return get_ipython() is not None


def get_qapp(*args, **kwargs):
    """ Gets the global Qt application object. Creates one if it doesn't exist.
        If IPython is running, it uses the IPython functions so that user
        interaction is possible. See:
        http://ipython.readthedocs.org/en/stable/api/generated/IPython.lib.guisupport.html
    """
    if in_ipython():
        logger.debug("IPython detected. Using IPython QApplication")
        from IPython.lib.guisupport import get_app_qt4
        return get_app_qt4(*args, **kwargs)
    else:
        qApp = QtGui.QApplication.instance()
        if qApp:
            logger.debug("Returning existing QApplication")
            return qApp
        else:
            logger.debug("Creating new QApplication")
            return QtGui.QApplication(*args, **kwargs)
            
        
    
def start_qt_event_loop(qApp):
    """ If IPython is running, the event loop is started
    """
    if in_ipython():
        try:
            logger.debug("IPython detected")
            from IPython.lib.guisupport import is_event_loop_running_qt4, start_event_loop_qt4
            if is_event_loop_running_qt4(qApp):
                logger.info("IPython event loop already running. GUI integration possible.")
            else:
                # No gui integration
                logger.info("Starting (non-interactive) IPython event loop")
                start_event_loop_qt4(qApp) # exit code alway 0
            return    
        except Exception as ex:
            logger.warning("Unable to start IPython Qt event loop: {}".format(ex))
            logger.warning("Falling back on non-interactive event loop: {}".format(ex))

    logger.info("Starting (non-interactive) event loop")
    return qApp.exec_()