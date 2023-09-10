import hashlib
from random import randint


class Point:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z


class CurveFp:
    def __init__(self, A, B, P, N, Gx, Gy):
        self.A = A
        self.B = B
        self.P = P
        self.N = N
        self.G = Point(Gx, Gy)  # G(Gx,Gy,0)


# y²=x³+7 %p    p=2^256-2^32-7 ,  模数为F_P ,  素数阶为  N , Gx,Gy 为基点的坐标
secp256k1 = CurveFp(
    A=0x0,
    B=0x7,
    P=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
    N=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
    Gx=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    # x^3+7%p=0
    Gy=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    # y^2%p=0
)

A = 0x0
P = secp256k1.P
N = secp256k1.N
G = secp256k1.G


class Math:
    @classmethod
    def multiply(cls, p, n):
        global A, N, P
        return cls._fromJacobian(cls._jacobianMultiply(cls._toJacobian(p), n))

    @classmethod
    def add(cls, p, q):
        global A, N, P
        return cls._fromJacobian(
            cls._jacobianAdd(cls._toJacobian(p), cls._toJacobian(q))
        )

    @classmethod
    def inv(cls, x, n):
        if x == 0:
            return 0

        lm, hm = 1, 0
        low, high = x % n, n
        while low > 1:
            r = high // low
            nm, new = hm - lm * r, high - low * r
            lm, low, hm, high = nm, new, lm, low
        return lm % n

    @classmethod
    def _toJacobian(cls, p):  # Jacobian coordinates
        return Point(p.x, p.y, 1)

    @classmethod
    def _fromJacobian(cls, p):
        global P
        z = cls.inv(p.z, P)
        return Point((p.x * z**2) % P, (p.y * z**3) % P)

    @classmethod
    def _jacobianDouble(cls, p):
        global A, P
        if not p.y:
            return Point(0, 0, 0)
        ysq = (p.y**2) % P
        S = (4 * p.x * ysq) % P
        M = (3 * p.x**2 + A * p.z**4) % P
        nx = (M**2 - 2 * S) % P
        ny = (M * (S - nx) - 8 * ysq**2) % P
        nz = (2 * p.y * p.z) % P
        return Point(nx, ny, nz)

    @classmethod
    def _jacobianAdd(cls, p, q):
        global A, P
        if not p.y:
            return q
        if not q.y:
            return p

        U1 = (p.x * q.z**2) % P
        U2 = (q.x * p.z**2) % P
        S1 = (p.y * q.z**3) % P
        S2 = (q.y * p.z**3) % P

        if U1 == U2:
            if S1 != S2:
                return Point(0, 0, 1)
            return cls._jacobianDouble(p)

        H = U2 - U1
        R = S2 - S1
        H2 = (H * H) % P
        H3 = (H * H2) % P
        U1H2 = (U1 * H2) % P
        nx = (R**2 - H3 - 2 * U1H2) % P
        ny = (R * (U1H2 - nx) - S1 * H3) % P
        nz = (H * p.z * q.z) % P

        return Point(nx, ny, nz)

    @classmethod
    def _jacobianMultiply(cls, p, n):  # 雅可比乘法
        global A, P, N
        if p.y == 0 or n == 0:
            return Point(0, 0, 1)
        if n == 1:
            return p
        if n < 0 or n >= N:
            return cls._jacobianMultiply(p, n % N)
        if (n % 2) == 0:
            return cls._jacobianDouble(cls._jacobianMultiply(p, n // 2))
        # (n % 2) == 1:
        return cls._jacobianAdd(
            cls._jacobianDouble(cls._jacobianMultiply(p, n // 2)), p
        )


class PublicKey:
    def __init__(self, point, curve):
        self.point = point
        self.curve = curve


class PrivateKey:
    def __init__(self, curve=secp256k1, secret=None):
        self.curve = curve
        self.secret = secret or randint(1, curve.N - 1)

    def publicKey(self):
        curve = self.curve
        publicPoint = Math.multiply(curve.G, self.secret)
        return PublicKey(publicPoint, curve)


class VOPRF:
    def __init__(self, privateKey, publicKey):
        self.privateKey = privateKey
        self.publicKey = publicKey or privateKey.publicKey()

    def H1(self, x):
        curve = self.privateKey.curve
        return Math.multiply(curve.G, t)

    def H2(self, T_tilde, f_k, A, B):
        curve = self.privateKey.curve
        pk = self.publicKey.point
        data = bytes(
            str(curve.G.x)
            + str(curve.G.y)
            + str(pk.x)
            + str(pk.y)
            + str(T_tilde.x)
            + str(T_tilde.y)
            + str(f_k.x)
            + str(f_k.y)
            + str(A.x)
            + str(A.y)
            + str(B.x)
            + str(B.y),
            "utf-8",
        )
        hash_value = hashlib.sha256(data).digest()
        mapped_value = int.from_bytes(hash_value, "big") % curve.N
        return mapped_value

    def blind(self, t):
        curve = self.privateKey.curve
        T = self.H1(t)
        r = randint(1, curve.N - 1)
        T_tilde = Math.multiply(T, r)
        return T_tilde, r

    def sign(self, T_tilde):
        f_k = Math.multiply(T_tilde, self.privateKey.secret)
        return f_k

    def proof(self, T_tilde, f_k):
        curve = self.privateKey.curve
        t = randint(1, curve.N - 1)
        A1 = Math.multiply(curve.G, t)
        B1 = Math.multiply(T_tilde, t)
        c = self.H2(T_tilde, f_k, A1, B1)
        s = (t - c * self.privateKey.secret) % curve.N
        return c, s

    def unblind(self, f_k, r):
        curve = self.privateKey.curve
        r_inverse = Math.inv(r, curve.N)
        Tk = Math.multiply(f_k, r_inverse)
        return Tk

    def verify(self, T_tilde, f_k, s, c):
        curve = self.privateKey.curve
        pk = self.publicKey.point
        A2 = Math.add(Math.multiply(curve.G, s), Math.multiply(pk, c))
        B2 = Math.add(Math.multiply(T_tilde, s), Math.multiply(f_k, c))
        c1 = self.H2(T_tilde, f_k, A2, B2)
        return c1


privateKey = PrivateKey()
voprf = VOPRF(privateKey, privateKey.publicKey())

# Client
t = randint(1, secp256k1.N - 1)
T_tilde, r = voprf.blind(t)

# send T_tilde to Server

# Server
f_k = voprf.sign(T_tilde)
c1, s = voprf.proof(T_tilde, f_k)
print("c1 ", c1)
# print("s ",s)

# send f_k to Client

# Client
c2 = voprf.verify(T_tilde, f_k, s, c1)
token = voprf.unblind(f_k, r)
print("c2 ", c2)
if c1 == c2:
    token = voprf.unblind(f_k, r)
    print("VOPRF verification successful")
    print("({}, {})".format(token.x, token.y))
else:
    print("VOPRF verification failed")
