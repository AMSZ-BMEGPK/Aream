## Output data:
# Area: A
# Second moments of area: Ix, Iy
# Product moment of area: Ixy
# Section moduli: Kx, Ky
# (Plus in case of circularly symmetric cross-section:
#   Polar moment of area: Ip
#   Polar modulus: Kp)
from re import S
from telnetlib import IP
import numpy as np
import math
def transform(func):
    def inner(*args, **kwargs):
        print(args,kwargs)
        if len(args) >3:
            ans = func(*args[:-3])
            if not kwargs['rad']: #conversion if the default unit isnt radian
                phi= math.radians(args[-1])
            else:
                phi = args[-1]
            ans["Ixi"], ans["Ieta"], ans["Ixieta"], ans["Ip2"] = Iarbitraryaxis(**ans, x=args[-3],y=args[-2], phi=phi)

        else:
            ans = func(*args)
        return ans
    return inner

@transform
def Circle(d, t = 0):
    if t == 0:
        A = d ** 2 * np.pi / 4
        Ix = d ** 4 * np.pi / 64
        Iy = d ** 4 * np.pi / 64
        Ixy = 0
        Kx = d ** 3 * np.pi / 32
        Ky = d ** 3 * np.pi / 32
        Ip = d ** 4 * np.pi / 32
        Kp = d ** 3 * np.pi / 16
        I1 = Ix
        I2 = I1
        properties = {
            "A": A,
            "Ix": Ix,
            "Iy": Iy,
            "Ixy": Ixy,
            "Kx": Kx,
            "Ky": Ky,
            "Ip": Ip,
            "Kp": Kp,
            "alpha": 0,
            "I1": I1,
            "I2": I2
        }
    else:
        di = d - t
        A = (d ** 2 - di ** 2) * np.pi / 4
        Ix = (d ** 4 - di ** 4) * np.pi / 64
        Iy = (d ** 4 - di ** 4) * np.pi / 64
        Ixy = 0
        Kx = (d ** 4 - di ** 4) * np.pi / (32 * d)
        Ky = (d ** 4 - di ** 4) * np.pi / (32 * d)
        Ip = (d ** 4 - di ** 4) * np.pi / 32
        Kp = (d ** 4 - di ** 4) * np.pi / (16 * d)
        I1 = Ix
        I2 = I1
        
        properties = {
            "A": A,
            "Ix": Ix,
            "Iy": Iy,
            "Ixy": Ixy,
            "Kx": Kx,
            "Ky": Ky,
            "Ip": Ip,
            "Kp": Kp,
            "alpha": 0,
            "I1": I1,
            "I2": I2
        }
    return properties

@transform
def Rectangle(w, h, t = 0):
    if t == 0:
        A = w * h
        Ix = w * h ** 3 / 12
        Iy = w ** 3 * h / 12
        Ip = Ix + Iy
        Ixy = 0
        Kx = 2 * Ix / h
        Ky = 2 * Iy / w
        if Iy > Ix:
            alpha = np.pi / 2
            I1 = Iy
            I2 = Ix
        else:
            alpha = 0
            I1 = Ix
            I2 = Iy

        properties = {
            "A": A,
            "Ix": Ix,
            "Iy": Iy,
            "Ip": Ip,
            "Ixy": Ixy,
            "Kx": Kx,
            "Ky": Ky,
            "alpha": alpha,
            "I1": I1,
            "I2": I2
        }
    else:
        properties = RectangularHS(w, h, w-2*t, h-2*t)
    return properties


def RectangularHS(w2, h2, w1, h1):
    A = (w2 * h2) - (w1 * h1)
    Ix = (w2 * h2 ** 3 - w1 * h1 ** 3) / 12
    Iy = (w2 ** 3 * h2 - w1 ** 3 * h1) / 12
    Ip = Ix + Iy
    Ixy = 0
    Kx = 2 * Ix / h2
    Ky = 2 * Iy / w2
    if Iy > Ix:
        alpha = np.pi / 2
        I1 = Iy
        I2 = Ix
    else:
        alpha = 0
        I1 = Ix
        I2 = Iy

    properties = {
        "A": A,
        "Ix": Ix,
        "Iy": Iy,
        "Ip": Ip,
        "Ixy": Ixy,
        "Kx": Kx,
        "Ky": Ky,
        "alpha": alpha,
        "I1": I1,
        "I2": I2
    }
    return properties

@transform
def Ellipse(a, b, t = 0):
    if t == 0:
        A = a * b * np.pi
        Ix = a * b ** 3 * np.pi / 4
        Iy = a ** 3 * b * np.pi / 4
        Ip = Ix + Iy
        Ixy = 0
        Kx = Ix / b
        Ky = Iy / a
        if Iy > Ix:
            alpha = np.pi / 2
            I1 = Iy
            I2 = Ix
        else:
            alpha = 0
            I1 = Ix
            I2 = Iy
    else:
        a2 = a
        b2 = b
        a1 = a - t
        b1 = b - t
        A = (a2 * b2 - a1 * b1) * np.pi
        Ix = (a2 * b2 ** 3 - a1 * b1 ** 3) * np.pi / 4
        Iy = (a2 ** 3 * b2 - a1 ** 3 * b1) * np.pi / 4
        Ip = Ix + Iy
        Ixy = 0
        Kx = Ix / b2
        Ky = Iy / a2
        if Iy > Ix:
            alpha = np.pi / 2
            I1 = Iy
            I2 = Ix
        else:
            alpha = 0
            I1 = Ix
            I2 = Iy

    properties = {
        "A": A,
        "Ix": Ix,
        "Iy": Iy,
        "Ixy": Ixy,
        "Ip": Ip,
        "Kx": Kx,
        "Ky": Ky,
        "alpha": alpha,
        "I1": I1,
        "I2": I2
    }
    return properties

@transform
def IsoscelesTriangle(w, h, t = 0):
    if t == 0:
        A = w * h / 2
        Ix = w * h ** 3 / 36
        Iy = w ** 3 * h / 48
        Ip = Ix + Iy
        Ixy = 0
        Kx = 3 * Ix / 2 / h
        Ky = 2 * Iy / w
        if Iy > Ix:
            alpha = np.pi / 2
            I1 = Iy
            I2 = Ix
        else:
            alpha = 0
            I1 = Ix
            I2 = Iy
    else:
        w2 = w
        h2 = h

        phi = np.arctan(h / (w / 2))
        u = t / np.sin(phi)
        v = t / np.tan(phi)
        w1 = w - 2 * (u + v)
        h1 = h * (w1 / w)
        A = (w2 * h2 - w1 * h1) / 2

        A2 = w2*h2 / 2
        A1 = w1*h1 / 2

        Sy2 = h2 / 3
        Sy1 = t + h1 / 3

        Sy = (A2*Sy2 - A1*Sy1) / (A2 - A1)
        
        dy2 = Sy2 - Sy
        dy1 = Sy1 - Sy

        Ixs2 = w2 * h2**3 / 36 
        Ixs1 = w1 * h1**3 / 36

        Ix2 = Ixs2 + A2 * dy2**2
        Ix1 = Ixs1 + A1 * dy1**2

        Ix = Ix2 - Ix1
        Iy = (w2 ** 3 * h2 - w1 ** 3 * h1) / 48
        Ip = Ix + Iy
        Ixy = 0
        Kx = 3 * Ix / 2 / h2
        Ky = 2 * Iy / w2
        if Iy > Ix:
            alpha = np.pi / 2
            I1 = Iy
            I2 = Ix
        else:
            alpha = 0
            I1 = Ix
            I2 = Iy
        
    properties = {
            "A": A,
            "Ix": Ix,
            "Iy": Iy,
            "Ip": Ip,
            "Ixy": Ixy,
            "Kx": Kx,
            "Ky": Ky,
            "alpha": alpha,
            "I1": I1,
            "I2": I2
        }
    return properties

@transform
def RightTriangle(w, h, t = 0):
    if t == 0:
        A = w * h / 2
        Ix = w * h ** 3 / 36
        Iy = w ** 3 * h / 36
        Ip = Ix + Iy
        Ixy = w**2 * h**2 / 72
        Kx = Ix / (2/3 * h)
        Ky = Ix / (2/3 * w)
        I1 = (Ix+Iy)/2 + 0.5*np.sqrt((Ix-Iy)**2 + 4* Ixy**2)
        I2 = (Ix+Iy)/2 - 0.5*np.sqrt((Ix-Iy)**2 + 4* Ixy**2)
        if Ix != Iy and Ixy !=0:
            alpha = np.arctan((Ix-I1)/Ixy)
        else:
            alpha = np.pi/4
    else:
        w2 = w
        h2 = h

        phi = np.arctan(h2/w2)
        u = t / np.sin(phi)
        v = t / np.tan(phi)

        p = t / np.cos(phi)
        q = t * np.tan(phi)

        w1 = w2 - t - u - v
        h1 = h2 - t - p - q

        A = (w2 * h2 - w1 * h1) / 2

        A2 = w2 * h2 / 2
        A1 = w1 * h1 / 2

        Sx2 = w2 / 3
        Sy2 = h2 / 3
        
        Sx1 = t + w1 / 3
        Sy1 = t + h1 / 3

        Sx = (A2*Sx2 - A1*Sx1) / (A2 - A1)
        Sy = (A2*Sy2 - A1*Sy1) / (A2 - A1)
        
        dx2 = Sx - Sx2
        dy2 = Sy - Sy2
        dx1 = Sx - Sx1
        dy1 = Sy - Sy1

        Ixs2 = w2 * h2**3 / 36
        Ixs1 = w1 * h1**3 / 36

        Iys2 = w2**3 * h2 / 36
        Iys1 = w1**3 * h1 / 36

        Ixys2 = w2**2 * h2**2 / 72
        Ixys1 = w1**2 * h1**2 / 72

        Ix = (Ixs2 + A2*dy2**2) - (Ixs1 + A1*dy1**2)
        Iy = (Iys2 + A2*dx2**2) - (Iys1 + A1*dx1**2)
        Ixy = (Ixys2 + A2*dx2*dy2) - (Ixys1 + A1*dx1*dy1)

        Ip = Ix + Iy

        Kx = 3 * Ix / 2 / h2
        Ky = 2 * Iy / w2
        
        I1 = (Ix+Iy)/2 + 0.5*np.sqrt((Ix-Iy)**2 + 4* Ixy**2)
        I2 = (Ix+Iy)/2 - 0.5*np.sqrt((Ix-Iy)**2 + 4* Ixy**2)

        if Ix != Iy and Ixy !=0:
            alpha = np.arctan((Ix-I1)/Ixy)
        else:
            alpha = np.pi/4

    properties = {
            "A": A,
            "Ix": Ix,
            "Iy": Iy,
            "Ip": Ip,
            "Ixy": Ixy,
            "Kx": Kx,
            "Ky": Ky,
            "alpha": alpha,
            "I1": I1,
            "I2": I2
        }
    return properties

def Iarbitraryaxis(A, Ix, Iy, Ixy, x, y, phi, *args, **kwargs):
    Ix2 = Ix + x ** 2 * A
    Iy2 = Iy + y ** 2 * A
    Ip2 = Ix2 + Iy2
    Ix2y2 = Ixy + x * y * A
    Ixi = Ix2 * np.cos(phi) ** 2 + Iy2 * np.sin(phi) ** 2 - Ix2y2 * np.sin(2 * phi)
    Ieta = Ix2 * np.sin(phi) ** 2 + Iy2 * np.cos(phi) ** 2 + Ix2y2 * np.sin(2 * phi)
    Ixieta = (Ix2 - Iy2) / 2 * np.sin(2 * phi) + Ix2y2 * np.cos(2 * phi)
    return Ixi, Ieta, Ixieta, Ip2
