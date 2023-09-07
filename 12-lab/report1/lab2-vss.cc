#include <NTL/ZZ.h>
#include <algorithm>
#include <cassert>
#include <iostream>
#include <iterator>
#include <random>
#include <set>
#include <vector>

using namespace std;
using namespace NTL;

using Share = pair<ZZ, ZZ>;

ZZ p, q, g;
size_t bits = 16;

long witness(const ZZ &n, const ZZ &x) {
  ZZ m, y, z;
  long j, k;

  if (x == 0)
    return 0;

  // compute m, k such that n-1 = 2^k * m, m odd:

  k = 1;
  m = n / 2;
  while (m % 2 == 0) {
    k++;
    m /= 2;
  }

  z = PowerMod(x, m, n); // z = x^m % n
  if (z == 1)
    return 0;

  j = 0;
  do {
    y = z;
    z = (y * y) % n;
    j++;
  } while (j < k && z != 1);

  return z != 1 || y != n - 1;
}

long prime_test(const ZZ &n, long t) {
  if (n <= 1)
    return 0;

  // first, perform trial division by primes up to 2000

  PrimeSeq s; // a class for quickly generating primes in sequence
  long p;

  p = s.next(); // first prime is always 2
  while (p && p < 2000) {
    if ((n % p) == 0)
      return (n == p);
    p = s.next();
  }

  // second, perform t Miller-Rabin tests

  ZZ x;
  long i;

  for (i = 0; i < t; i++) {
    x = RandomBnd(n); // random number between 0 and n-1

    if (witness(n, x))
      return 0;
  }

  return 1;
}

// b = a^-1 mod m
void mod_inverse(ZZ &b, ZZ a, ZZ m) {
  ZZ m0, x0, x1;
  m0 = m, x0 = 0, x1 = 1;
  while (a > 1) {
    ZZ q = a / m;
    ZZ a0 = a;
    a = m;
    m = a0 % m;

    ZZ x00 = x0;
    x0 = x1 - q * x0;
    x1 = x00;
  }
  b = x1 < 0 ? x1 + m0 : x1;
}

// f = v + a1x + a2x^2 ... % q
void gen_coeff(vector<ZZ> &coeffs, ZZ v, size_t t) {
  assert(coeffs.size() == 0);

  ZZ rnd;
  for (size_t i = 0; i < t - 1; ++i) {
    RandomBits(rnd, bits);
    rnd %= q;
    coeffs.emplace_back(rnd);
  }
  coeffs.emplace_back(v);
}

// f = f(x) % q
void evaluate_poly(ZZ &f, const vector<ZZ> &coeffs, const ZZ &x) {
  f = 0;
  ZZ m(1);

  // for (auto c : std::ranges::views::reverse(coeffs)) {
  for (auto it = coeffs.rbegin(); it != coeffs.rend(); ++it) {
    auto c = *it;
    f += m * c;
    m = m * x;
  }
  f %= q;
}

// genrate shares and commitments
void vss_share(vector<Share> &shares, vector<ZZ> &comms, const ZZ &secret,
               size_t share_num, size_t degree) {
  assert(shares.size() == 0);

  vector<ZZ> coeffs;
  // generator a `t-1` degree polynomial
  gen_coeff(coeffs, secret, degree);

  // cout << "coefficients: " << endl;
  // for (auto c : coeffs) {
  //   cout << "\t" << c << endl;
  // }
  // cout << endl;

  // make commitments
  for (size_t i = 0; i < degree; ++i) {
    comms.emplace_back(PowerMod(g, coeffs[degree - 1 - i], p));
  }

  // get n shares
  for (size_t i = 0; i < share_num; ++i) {
    ZZ x, f;

    // generate a random value
    RandomBits(x, bits);
    x %= q;

    // evaluate out f on x
    evaluate_poly(f, coeffs, x);
    shares.push_back(make_pair(x, f));
  }
}

// just lagrange...
void vss_recon(ZZ &v, vector<Share> shares) {

  size_t t = shares.size();
  v = 0;

  for (size_t j = 0; j < t; ++j) {
    auto &[xj, yj] = shares[j];
    ZZ prod(1);

    for (size_t i = 0; i < t; ++i) {
      auto xi = shares[i].first;
      if (i != j && (xi - xj) != 0) {
        ZZ tmp;
        mod_inverse(tmp, (xj - xi) % q, q);
        prod = (prod * ((-xi) * tmp)) % q;
      }
    }

    prod = (prod * yj) % q;
    v = (v + prod) % q;
  }
}

void vss_verify(const vector<Share> &shares, const vector<ZZ> comms,
            size_t share_num, size_t degree) {

  for (size_t i = 0; i < share_num; ++i) {
    ZZ Pi(1);
    for (size_t j = 0; j < degree; ++j) {
      Pi *= PowerMod(comms[j], power(shares[i].first, j), p);
    }

    if (Pi % p == PowerMod(g, shares[i].second, p)) {
      cout << "Verification successful for Participant " << i
           << ". The share is valid" << endl;
    } else {
      cout << "Verification failed for Participan " << i
           << ". The share is invalid." << endl;
    }
  }
}

void print_shares(vector<Share> shares) {
  for (auto &[x, f] : shares) {
    cout << "\t(" << x << ", " << f << ")" << endl;
  }
}

int main() {
  ZZ v;
  size_t n, t;

  // init paremeters: (n, t) share
  GenPrime(q, bits);
  // RandomBits(v, bits);
  // https://stackoverflow.com/questions/31386544/ntl-library-how-to-assign-a-big-integer-to-zz-p
  // v = conv<ZZ>("1234567890987654321234567890111222333444555666777888999");
  v = 1234;
  v %= q;
  // n = 15;
  // t = 10;
  n = 5;
  t = 3;

  // find prime p, q | p - 1, commitments in Fp
  size_t k = 1;
  while (1) {
    p = k * q + 1;
    if (prime_test(p, 10))
      break;
    k = k + 1;
  }

  // Compute elements of G_q = {h^k mod p | h in Z_p^*}
  // |G_q| = q ,G_q is the unique q-order subgroup of Z_p.
  ZZ m(1);
  // std::unordered_set<ZZ> S;
  // FIXME: unordered_set is enough
  std::set<ZZ> S;
  for (ZZ h(1); h < p; ++h) {
    S.insert(PowerMod(h, k, p));
    // G.emplace_back(tmp % p);
  }
  // rm dup
  vector<ZZ> G(S.begin(), S.end());
  std::sort(G.begin(), G.end());

  // random non-1 elements
  std::vector<ZZ> R;
  ZZ g;
  while (1) {
    std::sample(G.begin(), G.end(), std::back_inserter(R), 1,
                std::mt19937{std::random_device{}()});
    assert(R.size() != 0);
    g = R[0];
    if (g != 1)
      break;
  }

  cout << "paremeters:" << endl;
  cout << "\tq: " << q << endl;
  cout << "\tp: " << p << endl;
  // cout << "\tk: " << k << endl;
  cout << "\tg: " << g << endl;
  cout << "\tv: " << v << endl;
  // cout << "\tnum of shares: " << n << endl;
  // cout << "\tthreshold: " << t << endl << endl;
  cout << "order of G is " << G.size() << endl;

  // share to n parts
  vector<Share> shares;
  vector<ZZ> comms;
  vss_share(shares, comms, v, n, t);
  cout << "generate " << n << " shares:" << endl;
  print_shares(shares);

  // validation of shares
  vss_verify(shares, comms, n, t);

  // random sample `t` shares
  vector<Share> t_shares;
  sample(shares.begin(), shares.end(), std::back_inserter(t_shares), t,
         std::mt19937{std::random_device{}()});

  cout << "sample " << t << " shares" << endl;
  print_shares(t_shares);

  // resume to origin value
  ZZ out;
  vss_recon(out, t_shares);
  cout << "resume: " << out << endl;
  cout << "origin: " << v << endl;
}
