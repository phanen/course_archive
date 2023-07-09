#include <cstdio>
#include <cstring>
#include <iostream>
#include <algorithm>

using namespace std;

const int N = 1010, M = 2000010, INF = 1000000000;

int n, m;
int g[N][N], dist[N];   
bool st[N];     

void dijkstra()
{
    memset(dist, 0x3f, sizeof dist);
    dist[1] = 0;
    st[1] = 1;
    int id_prv = 1, id;
    for (int i = 0; i < n - 1; i++)
    {
        int id, mind = INF;
        for (int j = 1; j <= n; j++)
        {
            if (!st[j] && dist[j] < mind)
            {
                mind = dist[j];
                id = j;
            }
            dist[j] = min(dist[j], dist[id_prv] + g[id_prv][j]);
        }
        st[id_prv = id] = 1;
    }
}

int main()
{
    cin >> m >> n;
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++)
            g[i][j] = INF;
    for (int i = 0; i < m; i++)
    {
        int a, b, c;
        cin >> a >> b >> c;
        g[a][b] = g[b][a] = min(g[a][b], c);
    }
    dijkstra();
    cout << dist[n] << endl;
    return 0;
}

