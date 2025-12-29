#include <bits/stdc++.h>
using namespace std;
using i64 = long long;
using u64 = unsigned long long;
using u32 = unsigned;

using u128 = unsigned __int128;
using i128 = __int128;

void solve() {
    i64 n, ans = -2e18;
    cin >> n;
    vector<i64> v(n), s(n), sj(n);
    for (int i = 0; i < n; i++)
    {
        cin >> v[i];
    }
    s[0] = v[0];
    sj[0] = v[0];
    for (int i = 1; i < n; i++)
    {
        s[i] = s[i - 1] + v[i];
        sj[i] = sj[i - 1] + abs(v[i]);
    }
    for (int i = 1; i < n; i++)
    {
        i64 temp = sj[i - 1] - (s[n - 1] - s[i]);
        ans = max(ans, temp);
    }
    ans = max(-(s[n - 1] - s[0]), ans);
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