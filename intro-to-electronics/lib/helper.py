def interpolate(x, in_min, in_max, out_min, out_max, rounded=True):
    x = clamp(x, in_min, in_max)
    result = out_min + (x - in_min) * (out_max - out_min) / (in_max - in_min)
    if rounded: result = round(result)
    return result

def clamp(x, in_min, in_max):
    # Clamps the input to prevent out-of-bounds scaling
    if x < in_min: x = in_min
    if x > in_max: x = in_max
    return x
