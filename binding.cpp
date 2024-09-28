#include <bits/stdc++.h>

#include "leetcode.cpp"

using namespace std;

template<class T, char delim = ' '> auto print(T const &x) -> decltype(std::cout << x, void()) { std::cout << x << delim; }
template<class T> auto print(T const &x) -> typename std::enable_if<!std::is_constructible<decltype(x), std::string>::value && !std::is_constructible<std::string, decltype(x)>::value, decltype(std::begin(x), std::end(x), void())>::type {
    for (auto &&i: x) print(i);
}

int main() {
    // Python script will add correct function calls and arguments
    Solution solution;
	print(solution.maxArea({1,8,6,2,5,4,8,3,7}));std::cout<<std::endl;
	print(solution.maxArea({1,1}));std::cout<<std::endl;
return 0;
}