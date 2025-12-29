#include <bits/stdc++.h>
using namespace std;
using i64 = long long;
using u64 = unsigned long long;
using u32 = unsigned;

using u128 = unsigned __int128;
using i128 = __int128;

void solve() {
    string a;
    int t;
    cin >> t >> a;
    auto it1 = a.find("2026");
    auto it2 = a.find("2025");
    if(it1!=string::npos){
        cout << 0 << '\n';
        return;
    }
    if (it2 != string::npos)
    {
        cout << 1 << '\n';
    }
    else
    {
        cout << 0 << '\n';
    }
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int t;
    std::cin >> t;

    while (t--) {
        solve();
    }

    return 0;
}