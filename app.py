import logging
from chalice import Chalice
from chalicelib import pages


# Set application name
app = Chalice(app_name='Start-Page')

# set Global CORS
# app.api.cors = True

# Register blueprint
app.register_blueprint(pages.bp, name_prefix='webui')

# Set logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
