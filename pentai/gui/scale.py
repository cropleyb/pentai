
factor = 1.0
my_dp = 1.0

def set_scale_factor(f):
    global factor, my_dp
    factor = f
    my_dp = f

def dp(v):
    return int(v * factor)

def ps_dp():
    return my_dp

