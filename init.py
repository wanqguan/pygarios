# from cairo import Gradient


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16)/255.0 for i in range(0, lv, lv // 3))



PlayerColor = hex_to_rgb("#73c8a9")
BackColor = hex_to_rgb("#b2bec3")
BlockColor = hex_to_rgb("#0984e3")

