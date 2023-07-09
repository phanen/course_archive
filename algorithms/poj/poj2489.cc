#include <iostream>
#include <vector>
#include <cstring>
#include <algorithm>

using namespace std;

const int INF = 0x3f3f3f3f;

int n;
vector<string> ss;
int g[501][501];
int dist[501];
int st[501];

int solve()
{
  int ret = 0;
  dist[1] = 0; st[1] = 1; 
  int cur = 1;
  for (int i = 1; i < n; ++i) {
    for (int j = 1; j <= n; j++) dist[j] = min(dist[j], g[cur][j]);
    
    cur = 0;
    for (int j = 1; j <= n; ++j)
      if (!st[j] && dist[cur] > dist[j]) cur = j;
    
    st[cur] = 1;
    ret = max(ret, dist[cur]); 
  }
  return ret;
}


int main()
{
  ios_base::sync_with_stdio(0);
  cin.tie(0); cout.tie(0);
  int t; cin >> t;
  while (t--) {
    memset(g, 0x3f, sizeof(g));
    memset(st, 0, sizeof st);
    memset(dist, 0x3f, sizeof dist);
    ss.clear();  

    cin >> n;
    for (int i = 1; i <= n; ++i) for (int j = 1; j <= n; ++j) 
        cin >> g[i][j]; 
    cout << solve() << endl; 
  }
}
