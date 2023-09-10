#include "rsa.hh"
#include <iostream>
#include <stdio.h>
#include <tuple>
#include <vector>

namespace rsa {

namespace {
ZZ inv_mod(ZZ n1, ZZ n2) {
  ZZ x1 = ZZ(0), x2 = ZZ(1), y1 = x1, y2 = x2;
  ZZ q, x, y, z, inv = ZZ(1), sav = n2;
  if (n2 != 0) {
    while (n2 > 0) {
      q = n1 / n2;
      x = n1;
      y = x2;
      z = y2;
      n1 = n2;
      n2 = x - q * n2;
      x2 = x1;
      x1 = y - q * x1;
      y2 = y1;
      y1 = z - q * y1;
      if (n2 == 1) {
        inv = x1;
        if (inv < 1)
          inv += sav;
      }
    }
  }
  return inv;
}
ZZ mod_pow(ZZ a, ZZ e, ZZ n) {
  ZZ mod_p = ZZ(1);
  while (e > 0) {
    if ((e & 1) > 0)
      mod_p = (mod_p * a) % n;
    e >>= 1;
    a = (a * a) % n;
  }
  return mod_p;
}

ZZ mod(ZZ num, ZZ mod) {
  ZZ num_div_mod = num / mod;
  ZZ r = (num < 0) ? (num - (num_div_mod - 1) * mod) : num - num_div_mod * mod;
  return r;
}

} // namespace

void RSAKey::keygen(size_t t) {
  GenPrime(p, t);
  do {
    GenPrime(q, t);
  } while (p == q);

  n = p * q;
  ZZ y_n = (p - 1) * (q - 1);
  do {
    e = RandomBits_ZZ(t) % y_n + 2;
  } while (GCD(e, y_n) != 1);
  d = inv_mod(e, y_n);
  /*std::cout << p << ' ' << q << '\n';
  std::cout << n << ' ' << y_n <<'\n';
  std::cout << d << ' ' << e <<'\n';*/
}

ZZ enc(ZZ m, ZZ e, ZZ n) { return PowerMod(m, e, n); }

ZZ dec(ZZ c, ZZ d, ZZ n) {
  return PowerMod(c, d, n);
  // m1 = m^d mod p
  // m2 = m^d mod q
  // h = (q mod p) * (m1 - m2) mod p
  // m2 + h * q mod n
  // ZZ m1 = mod_pow(c, mod(d, p - 1), p);
  // ZZ m2 = mod_pow(c, mod(d, q - 1), q);
  // ZZ h = mod(inv_mod(q, p) * (m1 - m2), p);
  // return mod(m2 + (h * q), p * q);
}

} // namespace rsa
