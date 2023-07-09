#include <iostream>
#include <string>
using namespace std;

// 方括号转成大括号
string sq2b(const string &s) {
  string ret(s);
  for (auto &c : ret) {
    if (c == '[')
      c = '{';
    else if (c == ']')
      c = '}';
  }
  return ret;
}

int main() {
  string ii;
  // = "[[0,1],[1,1],[0,0]]";
  cin >> ii;
  cout << "我是说" << endl;
  cout << sq2b(ii) << endl;
}