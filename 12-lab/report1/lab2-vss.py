import random
from sympy import isprime
from Crypto.Util import number

# parameters setting
# prime q of bit-length 16, polynomial and shares in Fq
q = number.getPrime(16)
k = 1
while True:
    p = k * q + 1  # prime p ,q|p-1, commitments in Fp
    if isprime(p):
        break
    k = k + 1

# Compute elements of G_q = {h^k mod p | h in Z_p^*}
# |G_q| = q ,G_q is the unique q-order subgroup of Z_p.
G = []
for i in range(1, p):
    G.append(i**k % p)

G = list(set(G))
G.sort()
# print("G_q = ", G)
print("Order of G is " + str(len(G)) + " = q")

# Since the order of G_q is prime, any element of G_q except 1 is a generator
g = random.choice(list(filter(lambda g: g != 1, G)))  # g \in G_q
print("g = " + str(g))

# Not precise, but feasible.
"""
# y=u mod q
# 1、g^f(x) %p = g^{y %q} %p = g^u %p
# 2、(com[0]^x_0) * ... * (com[n-1]^x_n-1) %p = g^y %p = g^{u+tq} %p = g^u %p
if    g^q=1 mod p

g = random.randrange(2,p)
while(pow(g,q,p) != 1 ):
        g = random.randrange(2, p)
"""

print("q=", q, " g=", g, " p=", p)


def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1


def coeff(degree, secret):
    coefficients = []
    coefficients += [random.randrange(0, q) for _ in range(degree - 1)]
    coefficients.append(secret)
    print(coefficients)
    return coefficients


def polynom(x, coefficients):
    point = 0
    for coefficient_index, coefficient_value in enumerate(coefficients[::-1]):
        point += x**coefficient_index * coefficient_value
    return point


def generate_shares(num_shares, degree, secret, g):
    coefficients = coeff(degree, secret)
    print("coefficients ", coefficients)
    shares = []
    xs = random.sample(range(1, q), num_shares)  # 采取  num_shares  个随机数
    commitments = []
    for i in range(degree):
        commitments.append(pow(g, coefficients[degree - 1 - i], p))
    for i in range(0, num_shares):
        x = xs[i]
        shares.append((x, polynom(x, coefficients) % q))
    return shares, commitments


def reconstruct_secret(shares):
    sums = 0
    for j, share_j in enumerate(shares):
        xj, yj = share_j
        prod = 1
        for i, share_i in enumerate(shares):
            xi, _ = share_i
            if i != j and (xi - xj) != 0:
                prod = (prod * ((-xi) * mod_inverse((xj - xi) % q, q))) % q
        prod = (prod * yj) % q
        sums = (sums + prod) % q
    return sums


def Verify(degree, num_shares, shares):
    for i in range(num_shares):
        Pi = 1
        for j in range(degree):
            Pi *= pow(commitments[j], pow(shares[i][0], j), p) % p

        if Pi % p == pow(g, shares[i][1], p):
            print(
                f"Verification successful for Participant {i}. The share is valid")
        else:
            print("Verification failed. The share is invalid.")


if __name__ == "__main__":
    # (3,5) sharing scheme
    threshold, num_shares = 3, 5
    degree = threshold
    secret = 1234  # Fq
    print(f"Original Secret: {secret}")

    # Phase I: Generation of shares
    shares, commitments = generate_shares(num_shares, degree, secret, g)

    print(f'Shares: {", ".join(str(share) for share in shares)}')
    print("commitments", commitments)

    # Phase II: Validation of Shares
    Verify(degree, num_shares, shares)

    # Phase II: Secret Reconstruction
    # Picking degree shares randomly for
    # reconstruction
    pool = random.sample(shares, degree)
    print(f'Combining shares: {", ".join(str(share) for share in pool)}')
    print(f"Reconstructed secret: {reconstruct_secret(pool)}")
