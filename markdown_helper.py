import markdown2
import base64

def decode_markdown(data):
    try:
        return markdown2.markdown(base64.b64decode(data))
    except Exception as e:
        print (e)
        return ""
