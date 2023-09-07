import random
from Crypto.Util import number

# parameters setting
q = number.getPrime(16)  # prime q of bit-length 16


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


def generate_shares(num_shares, degree, secret):
    coefficients = coeff(degree, secret)
    shares = []
    xs = random.sample(range(0, q), num_shares)
    for i in range(0, num_shares):
        x = xs[i]
        shares.append((x, polynom(x, coefficients) % q))
    return shares


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


# Driver code
if __name__ == "__main__":
    # (3,5) sharing scheme
    threshold, num_shares = 3, 5
    degree = threshold
    secret = 12312
    print(q)
    print(f"Original Secret: {secret}")

    # Phase I: Generation of shares
    shares = generate_shares(num_shares, degree, secret)
    print(f'Shares: {", ".join(str(share) for share in shares)}')

    # Phase II: Secret Reconstruction
    # Picking degree shares randomly for
    # reconstruction
    pool = random.sample(shares, degree)
    print(f'Combining shares: {", ".join(str(share) for share in pool)}')
    print(f"Reconstructed  secret:  {reconstruct_secret(pool)}")
