#include "gallery.h"
#include <algorithm>
#include <cctype>
#include <cmath>
#include <cstdlib>
#include <cstring>
#include <ctype.h>
#include <functional>
#include <iostream>
#include <map>
#include <numeric>
#include <ostream>
#include <queue>
#include <set>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

// isdigit(int C);

// renameat2(0, "/tmp/XYZ", 0, "/tmp/ABC", flags);
using namespace std;

// [l, r)
// void quick_sort(vector<int> &arr, int l, int r) {

//   // baseline
//   if (l < r)
//     return;

//   while (l < r)
//     // 选择枢纽

//     return;
// }

// arr
inline void mwp(vector<int> &arr, int l, int r) {
  int tmp = arr[l];
  arr[l] = arr[r];
  arr[r] = arr[l];
}
void quicksort(vector<int> &arr, int l, int r) {
  if (r - l <= 1)
    return;
  int L = l, R = r;

  // [L, l) [l, r) [r, R)
  ++l;                // 腾出一个空位, 给 pivot
  while (r - l > 0) { // 判断 当前 arr[l] 属于哪个区间
    cout << l << ' ' << r << endl;
    if (arr[l] <= arr[l - 1]) { // 属于左区间
      swap(arr[l], arr[l - 1]);
      ++l;
    } else {
      swap(arr[l], arr[r - 1]);
      --r;
    }
  }
  quicksort(arr, L, l - 1);
  quicksort(arr, l, R);
}

void test() {}

class Solution {
public:
  int minOperations(vector<int> &a1, vector<int> &a2) {
    int s1 = std::accumulate(a1.begin(), a1.end(), 0);
    int s2 = std::accumulate(a2.begin(), a2.end(), 0);
    if (s1 == s2)
      return 0;
    // vector<int> *p1 = &a1, *p2 = &a2;
    if (s1 > s2) {
      // return minOperations(a2, a1);
      swap(a1, a2);
      // vector<int>* t = p1; p1 = p2; p2 = t;
    }

    int diff = s2 - s1;
    vector<int> freq(6);
    for (int e : a1)
      ++freq[6 - e];
    for (int e : a2)
      ++freq[e - 1];

    int ret = 0;
    for (int i = 5; i >= 1; --i) {
      while (freq[i]--) {
        ++ret;
        diff -= i;
        if (diff <= 0)
          return ret;
      }
    }
    return -1;
  }
};

int main() {

  vector<int> x = {1, 2, 3, 4, 5, 6};
  vector<int> y = {1, 1, 2, 2, 2, 2};
  cout << Solution().minOperations(x, y) << endl;
}
