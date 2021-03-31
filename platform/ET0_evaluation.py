'This script contains the formula for the evaluation of ET0 in both cases (wind = 0, wind >0)'

def ET0(delta, R_n, gamma, T = 0, wind=0, es=0, ea=0, G=0):
    if wind == 0:
        #complete formula for wind =!= 0
        ET = (0.408 * delta * (R_n - G))/(delta + gamma)
    else:
        ET = (0.408 * delta * (R_n - G) + (gamma * (900/T+273) * wind(es - ea)))/(delta + gamma(1 + (0.34*wind)))
    return ET
