#include <iostream>
#include <vector>
#include <cstring>
#include <algorithm>
#include <queue>
using namespace std;

const int N = 105;

int n;
int g[N][N];
int dist[N];
int st[N];

int prim()
{
  memset(dist, 0x3f, sizeof dist);
  memset(st, 0, sizeof st);
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

string mp[51];
pair<int, int> p[N];
int x, y;
int h[4] = {-1, 1, 0, 0};
int v[4] = {0, 0, 1, -1};
int vis[51][51];
int p2id[51][51];

inline bool check(int i, int j) {
  return !(i <= 0 || i > x || j <= 0 || j > y || mp[i][j - 1] == '#' || vis[i][j]);
}
struct Point {
  int x, y, d;
  Point(int x, int y, int d) : x(x), y(y), d(d) {};
};

void bfs(int a,int b) {
  memset(vis, 0, sizeof vis);
  int s = p2id[a][b];
  vis[a][b] = 1;
  int rem = n - 1; 
  g[s][s] = 0;
  queue<Point> q; q.push(Point(a, b, 0));
  while(!q.empty()) {
    Point cur = q.front(); q.pop();
    // cout << cur.x << ' ' << cur.y << ' ' << cur.d << endl;
    for(int k = 0; k < 4; k++) {
      int tx = cur.x + h[k], ty = cur.y + v[k];
      if (!check(tx, ty)) continue;
      // cout << " " << tx << ' ' << ty << endl;
      vis[tx][ty] = 1;
      int to = p2id[tx][ty];
      if(to) {
        g[s][to] = cur.d + 1;
        --rem; if (!rem) return;
      }
      q.push(Point(tx, ty, cur.d + 1));
    }
  }  
}

int main()
{
  // ios_base::sync_with_stdio(0);
  // cin.tie(0); cout.tie(0);
  int t; cin >> t; 
  while (t--) {
    memset(p2id, 0, sizeof p2id);
    cin >> y >> x; // x 行 y 列
    n = 0; getline(cin, mp[0]);
    for (int i = 1; i <= x; ++i) { 
      getline(cin, mp[i]);
      for (int j = 1; j <= y; ++j) 
        if (mp[i][j - 1] == 'A' || mp[i][j - 1] == 'S') {
          p[++n] = make_pair(i, j); p2id[i][j] = n;
        }
    }
  memset(g, 0, sizeof g);
    for (int k = 1; k <= n; ++k) bfs(p[k].first, p[k].second);
    cout << prim() << endl;
  }
}
