
def yprpb_to_rgb(y, pb, pr) -> tuple:
    """
    Used to create color palette for calendargrid
    """
    rgb_norm = [y + pr * 1.402,
                y + pb * -0.344 + pr * -0.714,
                y + pb * 1.772]
    return tuple([max(0, min(255, round(c * 255, 0))) for c in rgb_norm])

def rgb_to_hex(rgb: tuple) -> str:
    return '#%02x%02x%02x' % tuple(rgb)
