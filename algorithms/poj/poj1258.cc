#include <iostream>
#include <vector>
#include <cstring>
#include <algorithm>
#include <queue>
using namespace std;

const int INF = 0x3f3f3f3f;
const int N = 101;

int n;
int g[N][N];
int dist[N];
int st[N];

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
    ret += dist[cur]; 
  }
  return ret;
}


int main()
{
  ios_base::sync_with_stdio(0);
  cin.tie(0); cout.tie(0);
  while (cin >> n) {
    memset(g, 0x3f, sizeof(g));
    memset(st, 0, sizeof st);
    memset(dist, 0x3f, sizeof dist);

    for (int i = 1; i <= n; ++i) for (int j = 1; j <= n; ++j) 
        cin >> g[i][j]; 
    cout << solve() << endl; 
  }
}
