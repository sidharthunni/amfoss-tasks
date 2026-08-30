#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int t; cin >> t;
    while (t--) {
        int n, c; cin >> n >> c;
        vector<ll> a(n), b(n);
        for (auto &x : a) cin >> x;
        for (auto &x : b) cin >> x;

        ll ans = LLONG_MAX;
        bool ok1 = true; ll cost1 = 0;
        for (int i = 0; i < n; i++) {
            if (a[i] < b[i]) { ok1 = false; break; }
            cost1 += a[i] - b[i];
        }
        if (ok1) ans = min(ans, cost1);

        vector<ll> sa = a, sb = b;
        sort(sa.begin(), sa.end());
        sort(sb.begin(), sb.end());
        bool ok2 = true; ll cost2 = 0;
        for (int i = 0; i < n; i++) {
            if (sa[i] < sb[i]) { ok2 = false; break; }
            cost2 += sa[i] - sb[i];
        }
        if (ok2) ans = min(ans, cost2 + c);

        cout << (ans == LLONG_MAX ? -1 : ans) << "\n";
    }
    return 0;
}
