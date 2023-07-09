#include <iostream>
#include <set>
#include <unordered_set>
  using namespace std;


void test () {
  set<string> s;
  s.insert("aecde");
  s.insert("adcde");
  s.insert("aacde");
  s.insert("abcde");
  
  for (auto i : s) {
    cout << i << endl;
  }
}

int main() 
{
  string s;
  getline(cin, s);
  cout << s;
  getline(cin, s);
  cout << s;
  cout << cin.get();
}


