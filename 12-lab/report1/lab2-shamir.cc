#include <NTL/ZZ.h>
#include <algorithm>
#include <cassert>
#include <iostream>
#include <iterator>
#include <random>
#include <vector>

using namespace std;
using namespace NTL;

using ShamirShare = pair<ZZ, ZZ>;

ZZ q;
size_t bits = 1024;

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

void shamir_share(vector<ShamirShare> &shares, const ZZ &secret,
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
void shamir_recon(ZZ &v, vector<ShamirShare> shares) {

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

void print_shares(vector<ShamirShare> shares) {
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
  v = conv<ZZ>("1234567890987654321234567890111222333444555666777888999");
  v %= q;
  // n = 15;
  // t = 10;

  n = 5;
  t = 3;
  cout << "paremeters:" << endl;
  cout << "\tprime: " << q << endl;
  cout << "\torigin secret: " << v << endl;
  // cout << "\tnum of shares: " << n << endl;
  // cout << "\tthreshold: " << t << endl << endl;

  // share to n parts
  vector<ShamirShare> shares;
  shamir_share(shares, v, n, t);
  cout << "generate " << n << " shares:" << endl;
  print_shares(shares);

  // random sample `t` shares
  vector<ShamirShare> t_shares;
  sample(shares.begin(), shares.end(), std::back_inserter(t_shares), t,
         std::mt19937{std::random_device{}()});

  cout << "sample " << t << " shares" << endl;
  print_shares(t_shares);

  // resume to origin value
  ZZ out;
  shamir_recon(out, t_shares);
  cout << "resume: " << out << endl;
  cout << "origin: " << v << endl;
}
