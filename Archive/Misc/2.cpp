#include <bits/stdc++.h>
using namespace std;
using i64 = long long;
using u64 = unsigned long long;
using u32 = unsigned;

using u128 = unsigned __int128;
using i128 = __int128;

void solve() {
    string a;
    cin >> a;
    int ans = 0;
    if (a[0] == 'u'){
        ans++;
        a[0] = 's';
    }
    if(a[a.size()-1] == 'u'){
        ans++;
        a[a.size() - 1] = 's';
    }
    for (int i = 1; i < a.size()-1; i++)
    {
        if(a[i] == 'u' && a[i-1] != 's' ){
            ans++;
            a[i - 1] = 's';
        }
        if (a[i] == 'u' && a[i + 1] != 's')
        {
            ans++;
            a[i + 1] = 's';
        }
    }
    cout << ans << '\n';
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