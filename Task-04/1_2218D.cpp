#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int limit = 110000;
    vector<bool> isComposite(limit+1, false);
    vector<ll> primes;
    for (int i = 2; i <= limit; i++) {
        if (!isComposite[i]) {
            primes.push_back(i);
            for (ll j = (ll)i*i; j <= limit; j += i) isComposite[j] = true;
        }
    }

    int t; cin >> t;
    while (t--) {
        int n; cin >> n;
        vector<ll> a(n);
        a[0] = primes[0];
        for (int i = 1; i < n; i++) a[i] = primes[i-1] * primes[i];
        for (int i = 0; i < n; i++) cout << a[i] << " \n"[i==n-1];
    }
    return 0;
}
