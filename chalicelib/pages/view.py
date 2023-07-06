import os
import jinja2
from chalice.app import Response
from chalicelib import file
from chalicelib.utils import build_api_endpoint
from . import bp, logger


def render(templ_path, context):
    path, filename = os.path.split(templ_path)
    return jinja2.Environment(loader=jinja2.FileSystemLoader(path or "./")).get_template(filename).render(context)


@bp.route('/', methods=['GET'])
def index():
    """Start homepage"""
   
    # url links
    links = {
        'link1' : {'name' : 'Email', 'url' : 'https://mail.myners.net'},
        'link2' : {'name' : 'Calendar', 'url' : 'https://calendar.myners.net'},
        'link3' : {'name' : 'Drive', 'url' : 'https://drive.myners.net'},
        'link4' : {'name' : "Myners' Days", 'url' : 'http://days.myners.net'},
        'link5' : {'name' : 'Tech Note', 'url' : 'http://t.creast.win'}
    }

    # send image base64Url to front-end
    context = {
        'links' : links,
        'icon1' : file.get_img_base64Url('icon1.png'),
        'icon2' : file.get_img_base64Url('icon2.png'),
        'icon3' : file.get_img_base64Url('icon3.png'),
        'icon4' : file.get_img_base64Url('icon4.png'),
        'icon5' : file.get_img_base64Url('icon5.png'),
        'icon_left' : file.get_img_base64Url('icon_left'),
        'icon_left1' : file.get_img_base64Url('icon_left1'),
        'icon_right' : file.get_img_base64Url('icon_right'),
        'icon_right1' : file.get_img_base64Url('icon_right1'),
    }

    return Response(
        body = render('chalicelib/pages/index.html', context),
        status_code = 200, 
        headers={"Content-Type": "text/html"}
    )


@bp.route("/css/{file_name}", methods=["GET"])
def get_static_css(file_name):
    """Get Web CSS Endpoint"""
    css_file = file_name+'.css'
    logger.info(f"Endpoint: Get CSS : {css_file} static file")
    try:
        content = file.get_static_file(file_name=css_file)
        return Response(
            body=content, 
            status_code=200,
            headers={"Content-Type": "text/css"},
        )
    except Exception as ex:
        return Response(
            body=f"Failed request: {css_file}. {ex}",
            status_code=404,
            headers={"Content-Type": "text/html"},
        )


@bp.route("/js/{file_name}", methods=["GET"])
def get_static_js(file_name):
    """Get Javascript Endpoint"""
    js_file = file_name+'.js'
    logger.info(f"Endpoint: Get JS : {js_file} static file")
    try:
        content = file.get_static_file(file_name=js_file)
        return Response(
            body=content, 
            status_code=200,
            headers={"Content-Type": "application/javascript; charset=utf-8"},
        )
    except Exception as ex:
        return Response(
            body=f"Failed request: {js_file}. {ex}",
            status_code=404,
            headers={"Content-Type": "text/html"},
        )

@bp.route("/icon/{file_name}", methods=["GET"])
def get_icons(file_name):
    """
    Get icon image
    AWS Lambda cannot use this method to return image file directly, and you may encounter the following error:
    [ERROR] Runtime.MarshalError: Unable to marshal response: 'utf-8' codec can't decode byte 0xc1 in position 76: invalid start byte
    """
    logger.info(f"Endpoint: Get JS : {file_name} static file")
    try:
        img = file.get_static_media(file_name=file_name)
        return Response(
            # return the image in Base64 encoding
            body=img, 
            status_code=200,
            headers={"Content-Type": "image/png"}
        )
    except Exception as ex:
        return Response(
            body=f"Failed request: {file_name}. {ex}",
            status_code=404,
            headers={"Content-Type": "text/html"},
        )

@bp.route("/favicon.ico", methods=["GET"])
def get_favicon():
    """Get favicon image"""
    file_type='image/vnd.microsoft.icon'
    try:
        imgurl = file.get_img_base64Url(file_name='favicon.ico', file_type=file_type)
        icon = f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 32 32"><image width="32" height="32" xlink:href="{imgurl}"/></svg>'
        return Response(
            body=icon,
            status_code=200,
            headers={"Content-Type": "image/svg+xml"}
        )
    except Exception as ex:
        return Response(
            body=f"Failed request: favicon.ico. {ex}",
            status_code=404,
            headers={"Content-Type": "text/html"},
        )
