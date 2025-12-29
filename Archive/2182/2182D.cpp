#include <bits/stdc++.h>
using namespace std;
using i64 = long long;
using u64 = unsigned long long;
using u32 = unsigned;

using u128 = unsigned __int128;
using i128 = __int128;

i64 MOD = 998244353;

i64 factorial(int n)
{
    if (n >= MOD)
        return 0;
    i64 res = 1;
    for (int i = 1; i <= n; ++i)
    {
        res = (res * i) % MOD;
    }
    return res;
}

void solve() {
    int n;
    i64 sum = 0;
    cin >> n;
    vector<i64> v(n+1);
    for (int i = 0; i < n+1; i++)
    {
        cin >> v[i];
    }
    for (int i = 0; i < n+1; i++)
    {
        sum = sum + v[i];
    }
    i64 q = sum / n;
    i64 r = sum % n;
    int k = 0;
    for (int i = 1; i <= n; ++i)
    {
        if (v[i] > q + 1)
        {
            cout << 0 << "\n";
            return;
        }
        if (v[i] == q + 1)
        {
            k++;
        }
    }
    if (k > r)
    {
        cout << 0 << "\n";
        return;
    }
    i64 ans = 1;
    for (int i = 0; i < k; ++i)
    {
        ans = ans * (r - i) % MOD;
    }
    for (int i = 1; i <= n - k; ++i)
    {
        ans = ans * i % MOD;
    }
    cout << ans << "\n";
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