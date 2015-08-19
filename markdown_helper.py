import mistune
import base64

def decode_markdown(data):
    try:
        return mistune.markdown(base64.b64decode(data))
    except Exception as e:
        print (e)
        return ""
