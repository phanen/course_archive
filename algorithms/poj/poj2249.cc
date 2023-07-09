#include <iostream>
#include <cstring>
#include <map>
using namespace std;

int n; 
double g[31][31];

bool solve() {
  for (int k = 1; k <= n; ++k) 
    for (int i = 1; i <= n; ++i) 
      for (int j = 1; j <= n; ++j) 
        g[i][j] = max(g[i][j], g[i][k] * g[k][j]);
  bool flag = 0;
  for (int i = 1; !flag && i <= n; ++i) if (g[i][i] > 1) flag = 1;
  return flag;
}

map<string, int> str2id;


int main() {

  int id = 1;
  while (1) {
    cin >> n; if (!n) break;
    string a, b, c;
    for (int i = 1; i <= n; ++i) {
      cin >> a;
      str2id[a] = i;
      g[i][i] = 1;
    }
    int m; cin >> m;
    double r;
    for (int i = 0; i < m; ++i) {
      cin >> a >> r >> b;
      g[str2id[a]][str2id[b]] = r;
    }
    solve();
    cout << "Case " << id++ << ( solve() ? ": Yes" : ": No" ) << endl; 
  }
}
