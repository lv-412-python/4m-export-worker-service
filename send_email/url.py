"""Create URL"""
import urllib.parse

URL = "http://localhost:5000/download/"

def create_url(data):
    """Generate url"""
    return URL + urllib.parse.urlencode(data)


EMAIL_TEMPLATE = """
    <!DOCTYPE html>
    <html>
        <body>
            <h1 style = "color:SlateGray;">Greeting.
You can download file with answers for form <a href={url}>here</a>.</h1>
        </body>
    </html>
    """
