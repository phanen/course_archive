#include <cstdio>
#include <cstring>
#include <iostream>
#include <vector>
#include <algorithm>
// #include "../gallery.h"
using namespace std;


using vv = vector<vector<int>>;
string a, b;

vv gen_dp() {
  vv dp(a.size() + 1, vector<int>(b.size() + 1, 0));
  
  for (int i = 0; i <= a.size(); ++i) {
    dp[i][0] = 0;
  }
 
  for (int i = 0; i <= b.size(); ++i) {
    dp[0][i] = 0;
  }
 
  for (int i = 1; i <= a.size(); ++i) for (int j = 1; j <= b.size(); ++j)
    dp[i][j] = a[i - 1] == b[j - 1] ? dp[i - 1][j - 1] + 1 : max(dp[i - 1][j], dp[i][j - 1]);

  return dp;
}

using vs = vector<string>;
vs dfs(vv& dp, int x, int y) {
  if (x == 0 || y == 0) return {""};
  vs ret;
  if (a[x - 1] == b[y - 1]) {
    for (auto & each : dfs(dp, x - 1, y - 1))
      ret.emplace_back(each + a[x - 1]);
  }
  else { 
    if (dp[x][y - 1] >= dp[x - 1][y])
      ret = dfs(dp, x, y - 1);
    if (dp[x][y - 1] <= dp[x - 1][y]) {
      for (auto & each : dfs(dp, x - 1, y))
        ret.emplace_back(each);
    }
  }
  return ret;
}

void poj1934() {
  cin >> a >> b;
  vv dp = gen_dp();
  // cout << dp << endl;
  auto de = dfs(dp, a.size(), b.size());
  sort(de.begin(), de.end());
  // unique  
  for (int i = 1; i < de.size(); ++i) {
    if (de[i] == de[i - 1])
      de[i - 1] = "";
  }
  for (auto & each : de) if (!each.empty()) cout << each << endl;


}


int main () {
  poj1934();
}
