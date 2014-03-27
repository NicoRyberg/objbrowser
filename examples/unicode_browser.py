""" 
    Shows all unicode characters and properties.
    
    The glyphs for some characters may not be available if the font is not installed.
    
    Note that the object browser replaces the carriage-return (#13) and line-feed (#10) 
    characters in the unicode column with an arrow (#8629) to prevent multiline rows 
    in the table. Their displayed glyphs are thus not correct.
"""
from __future__ import print_function

import sys, logging, copy, unicodedata
from codecs import encode
from objbrowser import browse, logging_basic_config
from objbrowser.attribute_model import (AttributeModel, safe_data_fn, 
                                        ATTR_MODEL_NAME, ATTR_MODEL_UNICODE, ATTR_MODEL_REPR)

logger = logging.getLogger(__name__)

SMALL_COL_WIDTH = 80
MEDIUM_COL_WIDTH = 200

        
def my_browse(*args, **kwargs):
    """ Creates and starts an ObjectBrowser with added sqrt columns.
    """
    # Use some standard columns with adjusted with
    attribute_columns = copy.deepcopy([ATTR_MODEL_NAME, ATTR_MODEL_UNICODE, ATTR_MODEL_REPR])
    for attr_col in attribute_columns:
        attr_col.width = SMALL_COL_WIDTH
    
    # Add columns from the Unicode database
    function_settings = [(unicodedata.name, True, 300), 
                         (unicodedata.decimal, False, SMALL_COL_WIDTH),
                         (unicodedata.digit, False, SMALL_COL_WIDTH),
                         (unicodedata.numeric, False, SMALL_COL_WIDTH),
                         (unicodedata.category, True, SMALL_COL_WIDTH),
                         (unicodedata.bidirectional, False, SMALL_COL_WIDTH),
                         (unicodedata.combining, False, SMALL_COL_WIDTH),
                         (unicodedata.east_asian_width, False, SMALL_COL_WIDTH),
                         (unicodedata.mirrored, False, SMALL_COL_WIDTH),
                         (unicodedata.decomposition, False, SMALL_COL_WIDTH)]
    
    for function, visible, width in function_settings:
        attr_model = AttributeModel(function.__name__, 
            doc         = "Character meta data from the {!r} function".format(function.__name__), 
            data_fn     = safe_data_fn(function),
            col_visible = visible,
            width       = width)
        
        attribute_columns.append(attr_model) 
    
    # TODO: attribute details.
    return browse(*args, 
                  attribute_columns = attribute_columns,
                  **kwargs)
    
  
def main():
    """ Main program 
    """
    logging_basic_config('DEBUG')
    logger.info('Started unicode browser.')
    logger.info('Using unicode database: {}'.format(unicodedata.unidata_version))

    logger.debug('Generating unicode map')
    unicode_chars = {}
    for i in xrange(2**16):
        unicode_chars[i] = unichr(i)
    
    logger.debug('Starting browser')
    exit_code = my_browse(unicode_chars,  
                          show_routine_attributes=False,
                          show_special_attributes=False, 
                          reset = True) # use to reset persistent settings

    logging.info('Done example')
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
    