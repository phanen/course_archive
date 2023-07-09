#include <iostream>
#include <vector>
using namespace std;
int m, n;
vector<int> dp, a;

int solve() {
  int ret = 0;
  for (int i = 0; i < dp.size(); ++i) {
    int k = -1;
    for (int j = 0; j < i; ++j) {
      if (a[j] < a[i] && (k == -1 || dp[j] > dp[k])) k = j;
    }
    dp[i] = k == -1 ? 1 : 1 + dp[k];
    ret = max(ret, dp[i]); 
  }
  return ret;
}

int solve2() {
  dp[0] = a[0];
  int ret = 0; // 当前数组的尾部
  for (int i = 1; i < a.size(); ++i) {
    if (dp[ret] < a[i]) dp[++ret] = a[i];
    else *lower_bound(dp.begin(), dp.begin() + ret, a[i]) = a[i];
  }
  return ret + 1; 
}

void poj3903 () {
  while (cin >> m) {
    dp.resize(m);
    a.resize(m);
    for (int i = 0; i < m; ++i) cin >> a[i];
    cout << solve2() << endl;
  }
}

int main () {
  ios_base::sync_with_stdio(0);
  cin.tie(0);
  cout.tie(0);
  poj3903();
}
