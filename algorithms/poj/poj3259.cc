#include <iostream>
#include <cstring>
#include <queue>
using namespace std;

const int N = 1515, M = 5210;

int f, n, m, w;

int h[N]; // 每个顶点的 邻接表头
int e[M], ne[M], we[M]; // 存储所有边

int ct = 1; 
void add(int u,int v,int w){ // u 到 v 权 we
    e[ct] = v, we[ct] = w;
    ne[ct] = h[u], h[u] = ct++;
}

int dist[N];
bool iq[N]; // 在队列中 
int cnt[N]; // 计数边数判环

// 判断负环
bool spfa(){
  queue<int> q;
  for(int i = 1; i <= n;i ++){ 
    q.push(i); iq[i] = 1; 
  }
  while(!q.empty()){ 
    int t = q.front(); q.pop();
    iq[t] = 0;
    for (int i = h[t]; i; i = ne[i]) {
      int j = e[i];
      if(dist[j] > dist[t] + we[i]){
        dist[j] = dist[t] + we[i];
        cnt[j] = cnt[t] + 1; if(cnt[j] >= n) return 1;
        if(!iq[j]){
          q.push(j); iq[j] = 1;
        }
      }
    }
  }
  return 0; 
}


void solve() {
  memset(iq, 0, sizeof iq);
  memset(cnt, 0, sizeof cnt);
  memset(h, 0, sizeof h);
  cin >> n >> m >> w; 
  int a, b, c;
  ct = 1; 
  for(int i = 0; i < m; i++){ // 双向正边
    cin >> a >> b >> c; add(a, b, c); add(b, a, c);
  } 
  for(int i = 0; i < w; i++){ // 单向负边
    cin >> a >> b >> c; add(a, b, -c);
  }
  cout << (spfa() ? "YES" : "NO") << endl; 
}

int main(){
  int f; cin >> f;
  while(f--) solve();
}

