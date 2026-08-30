#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int t; cin >> t;
    while (t--) {
        int n; cin >> n;
        ll ans = 0;
        for (int i = 0; i < n; i++) {
            ll x; cin >> x;
            if (ans > x) ans += x;
            else ans = x;
        }
        cout << ans << "\n";
    }
    return 0;
}
