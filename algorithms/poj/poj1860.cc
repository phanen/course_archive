#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;

// 单个边的结构
struct edge {
  int a, b;    // 起点和终点
  double r, c; // rate 和 commission
};

// 使用 bellman_ford 算法
bool bellman_ford(const vector<edge> &edges, vector<double> &dist) {
  // 松弛
  for (int i = 0; i < dist.size(); i++) {
    for (int j = 0; j < edges.size(); j++) { // 遍历每条边
      dist[edges[j].b] = max<double>(
          dist[edges[j].b], (dist[edges[j].a] - edges[j].c) * edges[j].r);
    }
  }
  for (int i = 0; i < edges.size(); i++) {
    if (dist[edges[i].b] < (dist[edges[i].a] - edges[i].c) * edges[i].r)
      return 1;
  }
  return 0;
}

void poj1860() {
  // 货币数量 交易点数 初始货币种类 初始货币量
  // 点数 边数 起点位置 初始货币量
  int n, m;
  double s, v;
  cin >> n >> m >> s >> v;
  int a, b;
  double Rab, Cab, Rba, Cba;

  // 每个交易点增加两条边
  vector<edge> edges(2 * m);
  // 存储所有的边的信息
  for (int i = 0; i < edges.size(); i += 2) {
    cin >> a >> b >> Rab >> Cab >> Rba >> Cba;
    edges[i].a = a - 1;
    edges[i].b = b - 1;
    edges[i].r = Rab;
    edges[i].c = Cab;
    edges[i + 1].a = b - 1;
    edges[i + 1].b = a - 1;
    edges[i + 1].r = Rba;
    edges[i + 1].c = Cba;
    // edges[i] = edge{a, b, Rab, Cab};
    // edges[i + 1] = edge{b, a, Rba, Cba};
  }

  // 初始化最短路径
  vector<double> dist(n, 0); // d 到所有边的
  dist[s - 1] = v;
  // 使用 bellman_ford 搜索路径
  cout << (bellman_ford(edges, dist) ? "YES" : "NO") << endl;
}

int main() { poj1860(); }
