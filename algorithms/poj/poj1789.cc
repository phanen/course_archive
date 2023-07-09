#include <iostream>
#include <vector>
#include <memory.h>
#include <string>
#include <algorithm>

using namespace std;

const int INF = 0x3f3f3f3f;

int n;
vector<string> ss;
int g[2001][2001];
int dist[2001];
int st[2001];

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

    if (dist[cur] == INF) return INF;
    ret += dist[cur]; 
  }
  return ret;
}

int main()
{
  while (1) {
    memset(g, 0x3f, sizeof(g));
    memset(st, 0, sizeof st);
    memset(dist, 0x3f, sizeof dist);
    ss.clear();  

    cin >> n; if (!n) break;
    for (int i = 0; i < n; ++i) { // 初始化图
      string s; cin >> s;
      for (int j = 0; j < ss.size(); ++j) {
        int diff = 0;
        for (int k = 0; k < 7; ++k) if (s[k] != ss[j][k]) ++diff;
        g[j + 1][i + 1] = g[i + 1][j + 1] = diff;
      }
      ss.push_back(s);
    }

    cout << "The highest possible quality is 1/" << solve() <<"."<< endl;
  }
}
