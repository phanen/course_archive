#include <iostream>
#include <cstring>
#include <vector>
using namespace std;

int n; 
int g[101][101];
int dist[101];

void solve() {
  for (int k = 1; k <= n; ++k) 
    for (int i = 1; i <= n; ++i) 
      for (int j = 1; j <= n; ++j) 
        g[i][j] = min(g[i][j], g[i][k] + g[k][j]);
}

int main() {
  while (1) {
    cin >> n; if (!n) break;
    memset(g, 0x3f, sizeof g);
    for (int i = 1; i <= n; ++i) {
      int m, to, w;
      cin >> m;
      while (m--) {
        cin >> to  >> w;
        g[i][to] = w;
      }
      g[i][i] = 0; 
    }
    solve();
    int s = 0, d = 0x3f3f3f3f;
    for (int i = 1; i <= n; ++i) {
      int cur = 0;
      for (int j = 1; j <= n; ++j) cur = max(cur, g[i][j]); 
      if (cur < d) {
        d = cur; s = i;
      }
    }
    if (!s) cout << "disjoint" << endl;
    else cout << s << ' ' << d << endl;
  }
}
