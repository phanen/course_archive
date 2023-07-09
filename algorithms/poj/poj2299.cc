
// #include "../gallery.h"
#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;

long long ct = 0;
vector<int> buf;

void merge_sort_re(vector<int> &a, int l, int r) {
  if (r - l <= 1)
    return;
  int m = l + ((r - l) >> 1);
  merge_sort_re(a, l, m);
  merge_sort_re(a, m, r);

  // 归并
  int p1 = l, p2 = m, pb = l;
  while (p1 < m || p2 < r) {
    if (p2 >= r || (p1 < m && a[p1] <= a[p2]))
      buf[pb++] = a[p1++];
    else
      buf[pb++] = a[p2++];
  }
  for (int i = l; i < r; ++i)
    a[i] = buf[i];
}

void merge_sort(int a[], int l, int r, int buf[]) {
  if (r - l <= 1)
    return;
  int m = l + ((r - l) >> 1);
  merge_sort(a, l, m, buf);
  merge_sort(a, m, r, buf);

  // 归并
  int p1 = l, p2 = m, pb = l;
  while (p1 < m || p2 < r) {
    if (p2 >= r || (p1 < m && a[p1] <= a[p2]))
      buf[pb++] = a[p1++];
    else
      buf[pb++] = a[p2++];
  }
  for (int i = l; i < r; ++i)
    a[i] = buf[i];
}

void merge_sort(vector<int> &a) {
  if (a.size() == 1)
    return;
  buf.resize(max(buf.size(), a.size()));
  merge_sort_re(a, 0, a.size());
}

// 能进行任意 swap, 求最小的 swap 数
// int clac_min_swap(vector<int> &a) {

//   if (a.size() == 1)
//     return 0;

//   int ret = a.size();
//   // 离散化
//   vector<int> rank(a.size());
//   vector<int> a_c = a;
//   std::sort(a.begin(), a.end());
//   for (int i = 0; i < a_c.size(); ++i)
//     rank[i] = std::lower_bound(a.begin(), a.end(), a_c[i]) - a.begin();

//   // 标记该数所在的环是否被访问
//   vector<bool> visited(rank.size(), 0);

//   // DFS 遍历所有的置换环, 计数置换环的数量
//   for (int i = 0; i < rank.size(); ++i) {
//     if (visited[i])
//       continue;
//     while (!visited[i]) { // DFS 遍历一个置换环
//       visited[i] = 1;
//       i = rank[i];
//     }
//     --ret;
//   }
//   cout << rank << endl;
//   return ret;
// }

void poj2299() {
  int m;
  while (1) {
    cin >> m;
    if (!m)
      break;
    vector<int> a(m);
    for (int i = 0; i < m; ++i)
      cin >> a[i];
    ct = 0;
    merge_sort(a);
    cout << ct << endl;
  }
}

//
void poj2299_2() {

  int m;
  while (1) {
    cin >> m;
    if (!m)
      break;
    vector<int> a(m);
    for (int i = 0; i < m; ++i)
      cin >> a[i];
    ct = 0;
    merge_sort(a);
    cout << ct << endl;
  }
}
int main() {
  //  poj2299();
}
