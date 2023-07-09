#include <cstdio>
#include <cstring>
#include <iostream>
#include <algorithm>
#include <queue>

using namespace std;

const int N = 1010, M = 2000010, INF = 1000000000;

int n, m;
int dist[N], q[N];      // dist表示每个点到起点的距离, q 是队列
int h[N], e[M], v[M], ne[M], idx;       // 邻接表
bool st[N];     // 存储每个点是否在队列中

void add(int a, int b, int c)
{
    e[idx] = b, v[idx] = c, ne[idx] = h[a], h[a] = idx++;
}

void spfa()
{
    int hh = 0, tt = 0;
    for (int i = 1; i <= n; i++) dist[i] = INF;
    dist[1] = 0;
    q[tt++] = 1, st[1] = 1;
    while (hh != tt)
    {
        int t = q[hh++];
        st[t] = 0;
        if (hh == n) hh = 0;
        for (int i = h[t]; i != -1; i = ne[i])
            if (dist[e[i]] > dist[t] + v[i])
            {
                dist[e[i]] = dist[t] + v[i];
                if (!st[e[i]])
                {
                    st[e[i]] = 1;
                    q[tt++] = e[i];
                    if (tt == n) tt = 0;
                }
            }
    }
}

int main()
{
    memset(h, -1, sizeof h);
    cin >> m >> n;
    for (int i = 0; i < m; i++)
    {
        int a, b, c;
        cin >> a >> b >> c;
        add(a, b, c);
        add(b, a, c);
    }
    spfa();
    cout << dist[n] << endl;
    return 0;
}
