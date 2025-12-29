#include <bits/stdc++.h>
using namespace std;
using i64 = long long;
using u64 = unsigned long long;
using u32 = unsigned;

using u128 = unsigned __int128;
using i128 = __int128;

void solve() {
    int n;
    cin >> n;
    vector <i64> v(n);
    for (i64 i = 0; i < n; i++)
    {
        cin >> v[i];
    }
    for (i64 i = 0; i < n; i++)
    {
        for (i64 j = i+1; j < n; j++)
        {
            if((v[j]%v[i]) % 2 == 0){
                cout << v[i] << ' ' << v[j] << '\n';
                return;
            }
        }
        
    }
    cout << -1 << '\n';
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