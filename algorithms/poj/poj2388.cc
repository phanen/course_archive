
#include <iostream>
#include <vector>
using namespace std;

void quicksort(vector<int> &arr, int l, int r) {
  if (r - l <= 1)
    return;
  int L = l, R = r;
  ++l;                          // 腾出一个空位, 给 pivot
  while (r - l > 0) {           // 判断 当前 arr[l] 属于哪个区间
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

void poj2388() {
  int n;
  cin >> n;
  int m = n;
  vector<int> arr(n);
  while (n--)
    cin >> arr[n];
  quicksort(arr, 0, arr.size());
  // (n >> 1 - 1 + n >> 1)
  // n >> 1
  if (m & 1) {
    cout << arr[m >> 1] << endl;
  } else {
    m >>= 1;
    cout << (arr[m - 1] + arr[m]) / 2. << endl;
  }
}

int main() { poj2388(); }
