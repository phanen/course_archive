#include <iostream>
#include <cstring>
#include <queue>
using namespace std;


const int INF = 0x3f3f3f3f;
int m, n;
int g[101][101]; // g[i][j] 表示物品 i 替换 j 的价格
int rk[101]; // 每件物品的等级 
int rep[101]; // 每件物品的 替代品的数量

int dist[101];
bool st[101];

void dijkstra()
{
  for (int i = 1; i <= n; ++i) dist[i] = g[0][i]; // 物品价格
  for (int i = 0; i < n; i++)
  {
    int id = 0, mind = INF;
    for (int j = 1; j <= n; j++)
    {
      if (!st[j] && dist[j] < mind)
      {
        mind = dist[j]; id = j;
      }
    }
    if (!id) break; // 遍历完成
    st[id] = 1;
    for (int j = 1; j <= n; ++j) 
      if (!st[j] && g[id][j]) dist[j] = min(dist[j], dist[id] + g[id][j]);
  }
}


int main() {
  cin >> m >> n;
  for (int i = 1; i <= n; ++i) { // 每件物品
    cin >> g[0][i] >> rk[i] >> rep[i];  
    for (int j = 1; j <= rep[i]; ++j) { // 每件替代品
      int rep_id; cin >> rep_id;
      cin >> g[rep_id][i];
    }
  }


  int ret = INF;
  for (int i = 1; i <= n; ++i) { // 枚举起点
    for (int j = 1; j <= n; ++j)
      st[j] = (rk[j] > rk[i] || rk[i] - rk[j] > m);
    dijkstra();
    ret = min(ret, dist[1]);
  }
  cout << ret << endl;
}
