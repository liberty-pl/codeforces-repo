#include <bits/stdc++.h>
using namespace std;
using i64 = long long;
using u64 = unsigned long long;
using u32 = unsigned;

using u128 = unsigned __int128;
using i128 = __int128;

void solve() {
    int n;
    i64 ans1 = 0, ans2 = 0, ans3 = 0;
    cin >> n;
    vector<int> a(n),b(n),c(n);
    for (int i = 0; i < n; i++)
    {
        cin >> a[i];
    }
    for (int i = 0; i < n; i++)
    {
        cin >> b[i];
    }
    for (int i = 0; i < n; i++)
    {
        cin >> c[i];
    }
    bool f = true;
    for (int i = 0; i < n; i++)
    {
        f = true;
        for (int j = 0; j < n; j++)
        {
            if(a[j] >= b[(j+i)%n]){
                f = false;
            }
        }
        if(f){
            ans1++;
        }
    }
    f = true;
    for (int i = 0; i < n; i++)
    {

        f = true;
        for (int j = 0; j < n; j++)
        {
            if (b[j] >= c[(j + i) % n])
            {
                f = false;
            }
        }
        if (f)
        {
            ans2++;
        }
    }
    cout << ans2 * ans1 * n << '\n';
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