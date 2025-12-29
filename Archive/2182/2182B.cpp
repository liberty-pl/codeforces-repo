#include <bits/stdc++.h>
using namespace std;
using i64 = long long;
using u64 = unsigned long long;
using u32 = unsigned;

using u128 = unsigned __int128;
using i128 = __int128;

void solve() {
    i64 a, b, temp1 = 1, temp3 = 1, max1 = 0, max2 = 0, max3 = 0, max4 = 0;
    cin >> a >> b;
    while(a >= temp1){
        temp3 *= 4;
        temp1 = temp1 + temp3;
        max1++;
    }
    temp1 = 2;
    temp3 = 2;
    while(a >= temp1){
        temp3 *= 4;
        temp1 = temp1 + temp3;
        max2++;
    }
    temp1 = 1;
    temp3 = 1;
    while (b >= temp1)
    {
        temp3 *= 4;
        temp1 = temp1 + temp3;
        max3++;
    }
    
    temp1 = 2;
    temp3 = 2;
    while (b >= temp1)
    {
        temp3 *= 4;
        temp1 = temp1 + temp3;
        max4++;
    }
    i64 t=0, m=0;
    if (max1 == max4)
    {
        t = max4 * 2;
    }
    else
    {
        t = min(max1, max4) * 2;
        if(max1 > max4)
            t++;
    }
    if (max2 == max3)
    {
        m = max3 * 2;
    }
    else
    {
        m = min(max2, max3) * 2;
        if(max3>max2)
            m++;
    }
    cout << max(t, m) << '\n';
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