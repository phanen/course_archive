
# lab 2: 密码学基础知识


## 2.1 秘密共享协议实验
- 编程实现 Shamir 秘密共享协议, 并调试通过.
- 利用 Shamir 秘密共享协议对某一数据文件进行单次分享和重构操作.
- 界面简洁, 友好, 便于操作

### 基本原理

Shamir密钥分享算法最早在1970年基于Lagrange插值和矢量方法提出的, 基本思想是分发着通过秘密多项式, 将秘密s分解为n个秘密, 分发给持有者, 其中任意不少于t个秘密均能恢复密文, 而任意少于t个秘密均无法得到密文的任何信息.

对 `(n, t)` 的 share, 将其分为 `n` 份, 至少由 `t` 方重构, 过程简述如下:
- share: 对秘密 `s`, 任取 `t-1` 个随机数, 构造系数多项式(要求常数项为 `s`), 任取 `n` 个数带入多项式, 得到 `n` 长向量, 每个元素为 `(x_i, f(x_i))`, 可将其分发到 `n` 个服务器
- reconstruct: 任取 `t` 方的数据, 待定系数求解得到原多项式 `f`, 则 `f(0)`, 一般可以直接用 lagrange 公式.

### 代码实现

c++ 实现, 使用 ntl 库
```cc
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
```
- 使用 ntl 库用于大素数的生成和大数计算
- `evaluate_poly` 使用 lagrange 法根据 shares 计算多项式的常数项
- `gen_coeff` 用于生成多项式 (相比示例略做优化)

### 运行效果

![img:lab2-shamir1](https://i.imgur.com/gn4prsO.png)
![img:lab2-shamir2](https://i.imgur.com/wUw7Cmr.png)

## 2.2 可验证秘密共享 VSS 协议与公开可验证秘密共享 PVSS 协议实验
- 编程实现  VSS (如Feldman-VSS, Pedersen-VSS 等)和  PVSS(如Schoenmakers-PVSS, Stadler-PVSS 等)  协议, 并调试通过.
- 利用  VSS  和  PVSS  协议对某一数据文件进行单次分享和重构操作.
- 界面简洁, 友好, 便于操作

### 基本原理
在 share share 的基础上, 上一步预计算承诺.

计算方式:
```cc
// make commitments
for (size_t i = 0; i < degree; ++i) {
  comms.emplace_back(PowerMod(g, coeffs[degree - 1 - i], p));
}
```

验证承诺:
```cc
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
```


### 代码实现

```cc
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

```


### 运行效果

![img:lab2-vss](https://i.imgur.com/JEo1cf6.png)


## 2.3

## 2.4


# lab3: 网络侦查技术

## 3.1 站点信息查询

- 获得目标站点的相关信息(尽可能包含所有项): 域名服务注册信息, 包括: 注册商名称及  IP  地址, 注册时间, 域名分配的  IP  地址(段), 注册人联系信息(姓名, 邮箱, 电话, 办公地址); 相关  IP  地址信息, 如  DNS, 邮件服务器, 网关的  IP  地址.
- 站点所属机构的相关信息(尽可能包含所有项): 业务信息, 主要负责人信息(姓  名, 邮箱, 电话, 办公地址, 简历等), 有合作关系的单位名称及网址.
- 所有查询输入及结果均需截图, 并写入实验报告中

### whois 查询

![img:lab3.1-baidu1](https://i.imgur.com/iNjbt3c.png)
![img:lab3.1-baidu2](https://i.imgur.com/O1qpI8J.png)

有用信息如下:
```
Domain Name: BAIDU.COM
Registry Domain ID: 11181110_DOMAIN_COM-VRSN
Registrar WHOIS Server: whois.markmonitor.com
Registrar URL: http://www.markmonitor.com
Updated Date: 2022-09-01T03:54:43Z
Creation Date: 1999-10-11T11:05:17Z
Registry Expiry Date: 2026-10-11T11:05:17Z
Registrar: MarkMonitor Inc.
Registrar IANA ID: 292
Registrar Abuse Contact Email: abusecomplaints@markmonitor.com
Registrar Abuse Contact Phone: +1.2086851750
Domain Status: clientDeleteProhibited https://icann.org/epp#clientDeleteProhibited
Domain Status: clientTransferProhibited https://icann.org/epp#clientTransferProhibited
Domain Status: clientUpdateProhibited https://icann.org/epp#clientUpdateProhibited
Domain Status: serverDeleteProhibited https://icann.org/epp#serverDeleteProhibited
Domain Status: serverTransferProhibited https://icann.org/epp#serverTransferProhibited
Domain Status: serverUpdateProhibited https://icann.org/epp#serverUpdateProhibited
Name Server: NS1.BAIDU.COM
Name Server: NS2.BAIDU.COM
Name Server: NS3.BAIDU.COM
Name Server: NS4.BAIDU.COM
Name Server: NS7.BAIDU.COM
DNSSEC: unsigned
URL of the ICANN Whois Inaccuracy Complaint Form: https://www.icann.org/wicf/

Domain Name: baidu.com
Registry Domain ID: 11181110_DOMAIN_COM-VRSN
Registrar WHOIS Server: whois.markmonitor.com
Registrar URL: http://www.markmonitor.com
Updated Date: 2022-09-01T03:29:31+0000
Creation Date: 1999-10-11T11:05:17+0000
Registrar Registration Expiration Date: 2026-10-11T07:00:00+0000
Registrar: MarkMonitor, Inc.
Registrar IANA ID: 292
Registrar Abuse Contact Email: abusecomplaints@markmonitor.com
Registrar Abuse Contact Phone: +1.2086851750
Domain Status: clientUpdateProhibited (https://www.icann.org/epp#clientUpdateProhibited)
Domain Status: clientTransferProhibited (https://www.icann.org/epp#clientTransferProhibited)
Domain Status: clientDeleteProhibited (https://www.icann.org/epp#clientDeleteProhibited)
Domain Status: serverUpdateProhibited (https://www.icann.org/epp#serverUpdateProhibited)
Domain Status: serverTransferProhibited (https://www.icann.org/epp#serverTransferProhibited)
Domain Status: serverDeleteProhibited (https://www.icann.org/epp#serverDeleteProhibited)
Registrant Organization: Beijing Baidu Netcom Science Technology Co., Ltd.
Registrant State/Province: Beijing
Registrant Country: CN
Registrant Email: Select Request Email Form at https://domains.markmonitor.com/whois/baidu.com
Admin Organization: Beijing Baidu Netcom Science Technology Co., Ltd.
Admin State/Province: Beijing
Admin Country: CN
Admin Email: Select Request Email Form at https://domains.markmonitor.com/whois/baidu.com
Tech Organization: Beijing Baidu Netcom Science Technology Co., Ltd.
Tech State/Province: Beijing
Tech Country: CN
Tech Email: Select Request Email Form at https://domains.markmonitor.com/whois/baidu.com
Name Server: ns2.baidu.com
Name Server: ns4.baidu.com
Name Server: ns1.baidu.com
Name Server: ns3.baidu.com
Name Server: ns7.baidu.com
DNSSEC: unsigned
```

注册商信息
- 域名: BAIDU.COM
- 注册域名ID: 11181110_DOMAIN_COM-VRSN
- Whois 服务器: whois.markmonitor.com
- 注册URL: http://www.markmonitor.com
- 更新日期: 2022-09-01T03:54:43Z
- 创造日期: 1999-10-11T11:05:17Z
- 注册截止日期: 2026-09-13T07:00:00Z
- 注册商名称: MarkMonitor, Inc.
- 注册商 IANA 编号: 292
- 注册商域名滥用举报邮箱: abusecomplaints@markmonitor.com
- 注册商域名滥用举报电话: +1.2086851750
-
域名服务器
- ns1.baidu.com
- ns2.baidu.com
- ns3.baidu.com
- ns4.baidu.com
- ns7.baidu.com

> 域名信息, 包括注册人信息, 管理人信息, 技术信息.

注册人信息:
- 注册组织: Beijing Baidu Netcom Science Technology Co., Ltd.
- 注册州/省: Beijing
- 注册国家: CN(中国)
- 注册邮箱: https://domains.markmonitor.com/whois/baidu.com

管理人信息
- 管理组织: Beijing Baidu Netcom Science Technology Co., Ltd.
- 管理州/省: Beijing
- 管理国家: CN(中国)
- 管理邮箱: https://domains.markmonitor.com/whois/baidu.com

技术信息
- 技术组织: Beijing Baidu Netcom Science Technology Co., Ltd.
- 技术州/省: Beijing
- 技术国家: CN(中国)
- 技术邮箱: https://domains.markmonitor.com/whois/baidu.com

### ip 查询

![img:lab3.1-ip](https://i.imgur.com/wondeuI.png)
- 可以查得 baidu.com 的 ip 为 39.156.66.10
- 归属地(纯真数据): 北京市 移动
- 归属地(ipip): 中国 北京 北京

### DNS 查询

![img:lab3.1-dns](https://i.imgur.com/3M1i93w.png)

### 爱企查

![img:lab3.1-aiqi1](https://i.imgur.com/0ZygTlB.png)
![img:lab3.1-aiqi2](https://i.imgur.com/9FQzJYV.png)
- 法定代表人: 梁志祥
- 网址: www.baidu.com
- 年报: 北京百度网讯科技有限公司2022年度报告
- 地址: 北京市海淀区上地十街10号百度大厦2层
- 主营业务: 一般项目: 技术服务, 技术开发, 技术咨询, 技术交流, 技术转让, 技术推广; 计算机软硬件及辅助设备零售; 软件开发; 计算机系统服务; 信息系统集成服务; 数据处理服务; 数字内容制作服务(不含出版发行); 软件销售; 计算机软硬件及辅助设备批发; 电子产品销售; 电子元器件批发; 电子元器件零售; 机械设备租赁; 广告制作; 广告发布; 广告设计, 代理; 专业设计服务; 市场营销策划; 会议及展览服务; 信息技术咨询服务; 企业管理咨询; 社会经济咨询服务; 家用电器销售; 机械设备销售; 五金产品零售; 五金产品批发; 玩具, 动漫及游艺用品销售; 游艺用品及室内游艺器材销售; 针纺织品销售; 照相机及器材销售; 化妆品批发; 化妆品零售; 个人卫生用品销售; 体育用品及器材批发; 体育用品及器材零售; 服装服饰零售; 服装服饰批发; 鞋帽零售; 鞋帽批发; 日用品销售; 日用品批发; 珠宝首饰批发; 珠宝首饰零售; 工艺美术品及礼仪用品销售(象牙及其制品除外); 工艺美术品及收藏品批发(象牙及其制品除外); 钟表销售; 眼镜销售(不含隐形眼镜); 玩具销售; 办公用品销售; 摩托车及零配件零售; 摩托车及零配件批发; 仪器仪表销售; 家具销售; 塑料制品销售; 建筑材料销售; 通讯设备销售; 食品销售(仅销售预包装食品); 保健食品(预包装)销售; 货物进出口; 技术进出口; 进出口代理; 汽车零配件批发; 汽车零配件零售; 汽车零部件及配件制造; 汽车销售; 健康咨询服务(不含诊疗服务); 票务代理服务; 翻译服务; 第一类医疗器械销售; 第二类医疗器械销售; 教育咨询服务(不含涉许可审批的教育培训活动); 人力资源服务(不含职业中介活动, 劳务派遣服务). (除依法须经批准的项目外, 凭营业执照依法自主开展经营活动)许可项目: 第一类增值电信业务; 第二类增值电信业务; 网络文化经营; 出版物零售; 出版物批发; 演出经纪; 职业中介活动; 广播电视节目制作经营; 信息网络传播视听节目; 互联网新闻信息服务; 测绘服务. (依法须经批准的项目, 经相关部门批准后方可开展经营活动, 具体经营项目以相关部门批准文件或许可证件为准)(不得从事国家和本市产业政策禁止和限制类项目的经营活动.)

## 3.2 联网设备查询
- 查找指定地域内有弱口令, 可匿名登录的网络设备 (路由器, 网关, Server 等) 并返回其  IP  地址.
- 查找指定地域内网络摄像头, 并返回其  IP  地址.
- 实验过程中只允许浏览搜索结果. 对搜索到的可远程控制的设备, 应禁止学生对这些设备进行远程控制.
- 所有查询输入及结果均需截图, 并写入实验报告中.

搜索中国境内有弱口令(default password), 可匿名登录(anonymous login)的网络设备(路由器, 网关, Server 等: router gateway server default password anonymous login country:cn

![img:lab3.2-netcam1](https://i.imgur.com/2IPuc2f.png)
无结果

搜索中国北京的网络摄像头: netcam country:cn city:beijing
![img:lab3.2-netcam2](netcam country:cn city:beijing)

共两个
- 129.28.164.36
- 129.28.197.213

# lab 4: 网络扫描技术

## 4.1 主机扫描 1

使用  Nmap  工具互相扫描对方主机, 进行端口扫描和操作系统识别. 根据扫描结果分析主机开放的端口类型和对应的服务程序, 查看主机的详细信息. 通过"控制面板"的"管理工具"中的"服务"配置, 尝试关闭或开放目标主机上的部分服务, 重新扫描, 观察扫描结果的变化. 扫描过程中, 要求至少更改 2 次 Nmap 扫描选项进行扫描, 并观察不同选项下 Nmap 扫描结果的变化


<!-- 宿主机 archlinux, 方便起见,  vagrant 创建了另一个 archlinux (virualbox 虚拟机), 开启 ssh 映射到宿主机端口 2222, 从而能访问. -->

<!-- vagrant 虚拟机扫描宿主机 -->
<!-- ![img:lab4-vm](https://i.imgur.com/Ka4o9Wz.png) -->
<!-- 宿主机扫描 vagrant 虚拟机 -->

## 4.2 主机扫描 2
