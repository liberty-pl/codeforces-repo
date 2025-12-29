#include <iostream>

using namespace std;

void solve()
{
    long long a, b;
    cin >> a >> b;

    if (b % 2 != 0)
    {
        if (a % 2 != 0)
        {
            cout << a * b + 1 << endl;
        }
        else
        {
            cout << -1 << endl;
        }
    }
    else
    {
        bool f = false;
        if (a % 2 == 0)
        {
            f = true;
        }
        else
        {
            if (b % 4 == 0)
                f = true;
        }

        if (f)
        {
            cout << a * (b / 2) + 2 << endl;
        }
        else
        {
            cout << -1 << endl;
        }
    }
}

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int t;
    cin >> t;
    while (t--)
    {
        solve();
    }
    return 0;
}