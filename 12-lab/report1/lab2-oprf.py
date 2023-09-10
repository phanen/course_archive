from cryptography.hazmat.primitives.asymmetric import rsa
import hashlib
import random


def mod_inverse(a, m):  # return a_inverse = a^{-1} mod m
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1


# Generate RSA keys for Server
server_private_key = rsa.generate_private_key(
    public_exponent=65537,  # Choose the public exponent
    key_size=2048,  # Choose the key size (e.g., 2048 or 4096)
)

# Extract Server's public key
server_public_key = server_private_key.public_key()

# Server's RSA parameters
N = server_private_key.private_numbers().public_numbers.n  # Modulus
# p = server_private_key.private_numbers().p    # Prime Factor 1
# q = server_private_key.private_numbers().q    # Prime Factor 2
e = server_private_key.private_numbers().public_numbers.e  # Public Exponent
d = server_private_key.private_numbers().d  # Private Exponent
# print("Server's RSA Parameters:")

# Client's input
M = b"Hello, Crypto!"

# Step 1: Client selects a random number r from Z_N*
r = random.randint(1, N - 1)

# Step 2: Client calculates x = H(M) * r^d mod N
h = hashlib.sha256(M).digest()  # Calculate the hash of the input message M
h_int = int.from_bytes(h, byteorder="big")  # Convert the hash to an integer
x = (h_int * pow(r, e, N)) % N

# Step 3: Client sends x to Server(We ignore it here)

# Step 4: Server calculates y = x^e mod N
y = pow(x, d, N)

# Step 5: Server sends y to Client(We ignore it here)

# Step 6: Client calculates z = y * r^(-1) mod N
# Calculate the modular multiplicative inverse of r
r_inverse = mod_inverse(r, N)
z = (y * r_inverse) % N

# Client now has the final result z as the OPRF output
print("Client's OPRF Output:", z % N)
print("PRF    H(M)^d mod N = ", pow(h_int, d, N))
