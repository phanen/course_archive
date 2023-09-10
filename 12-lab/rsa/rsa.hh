#include <NTL/ZZ.h>
#include <tuple>

// n = p * q
// enc(m) -> m^e mod n
// dec(c) -> c^d mod n
namespace rsa {
using namespace NTL;
struct RSAKey {
  ZZ p, q, n, e, d;
  void keygen(size_t t);
};

ZZ crt(const ZZ &m, const ZZ &d, const ZZ &p, const ZZ &q);
ZZ enc(const ZZ &m, const ZZ &e, const ZZ &n);
ZZ dec(const ZZ &c, const ZZ &d, const ZZ &n);
} // namespace rsa
