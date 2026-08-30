#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int t; cin >> t;
    while (t--) {
        string x; cin >> x;
        int d = x.size();
        ll y = 1;
        for (int i = 0; i < d; i++) y *= 10;
        y += 1;
        cout << y << "\n";
    }
    return 0;
}
