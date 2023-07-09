
#include <iostream>
#include <ostream>
#include <vector>

struct TreeNode {
  int val;
  TreeNode *left;
  TreeNode *right;
  TreeNode() : val(0), left(nullptr), right(nullptr) {}
  TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
  TreeNode(int x, TreeNode *left, TreeNode *right)
      : val(x), left(left), right(right) {}
};

// template <typename T>
// std::ostream &operator<<(std::ostream &out, const std::vector<T> &v) {
//   if (!v.empty()) {
//     out << '[';
//     std::copy(v.begin(), v.end(), std::ostream_iterator<T>(out, ", "));
//     out << "\b\b]";
//   }
//   return out;
// }

template <class T>
std::ostream &operator<<(std::ostream &os, const std::vector<T> &arr) {
  os << '[';
  for (auto &each : arr) {
    os << each << ", ";
  }
  os << ']' << std::endl;
  return os;
}

// template <class T>
// std::ostream &operator<<(std::ostream &os, std::vector<T> &arr) {
//   for (auto &each : arr) {
//     os << each << ' ';
//   }
//   os << std::endl;
//   return os;
// }