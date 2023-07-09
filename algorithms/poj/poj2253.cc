#include<iostream>
#include<cmath>
#include<iomanip>
using namespace std;

const int INF = 0x3f3f3f3f;
int n;
int x[201], y[201];

double dist[201];
double g[201][201];
bool st[201];

double dijkstra() {
  double ret = 1e10;   
  for (int i = 1; i <= n; ++i) {
    dist[i] = INF; st[i] = 0; 
  }
  dist[1] = 0; st[1] = 1;
  for (int id = 1, id_prv = id; id != 2; id_prv = id) {
    int mind = INF;
    for (int j = 1; j <= n; ++j)  
      if (!st[j]) {
        dist[j] = min(dist[j], max(dist[id_prv], g[id_prv][j]));
        if (dist[j] < mind) {
          id = j; mind = dist[j];
        } 
      }
    st[id] = 1; 
  }
  return dist[2];
}

int main()
{
  int cnt = 1;
  cout << setiosflags(ios::fixed);
  cout << setprecision(3);
  while(1)
  {
    cin >> n; if(!n) break;
    for (int i = 1; i <= n; ++i) cin >> x[i] >> y[i];
    for (int i = 1; i <= n; ++i) for (int j = i + 1; j <= n; ++j) g[i][j] = g[j][i] = sqrt(
        (x[i] - x[j]) * (x[i] - x[j]) + (y[i] - y[j]) * (y[i] - y[j])
        );
    cout << "Scenario #" << cnt++ << endl
      << "Frog Distance = " << dijkstra() << endl << endl;
  }
  return 0;
}
