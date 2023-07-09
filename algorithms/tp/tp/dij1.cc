#include <cstdio>
#include <cstring>
#include <iostream>
#include <algorithm>

using namespace std;

const int N = 1010, M = 2000010, INF = 1000000000;

int n, m;
int g[N][N], dist[N];   // g[][]存储图的邻接矩阵, dist[]表示每个点到起点的距离
bool st[N];     // 存储每个点的最短距离是否已确定

void dijkstra()
{
	for (int i = 1; i <= n; i++) dist[i] = INF;
	dist[1] = 0;
	for (int i = 0; i < n; i++)
	{
		int id, mind = INF;
		for (int j = 1; j <= n; j++)
			if (!st[j] && dist[j] < mind)
			{
				mind = dist[j];
				id = j;
			}
		st[id] = 1;
		for (int j = 1; j <= n; j++) dist[j] = min(dist[j], dist[id] + g[id][j]);
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

