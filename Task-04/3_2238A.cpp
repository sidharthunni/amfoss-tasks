#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int t; cin >> t;
    while (t--) {
        string s; cin >> s;
        int n = s.size();
        vector<int> suf13(n+1, 0);
        for (int i = n-1; i >= 0; i--)
            suf13[i] = suf13[i+1] + (s[i]=='1' || s[i]=='3');
        int p2 = 0, best = 0;
        for (int p = 0; p <= n; p++) {
            best = max(best, p2 + suf13[p]);
            if (p < n && s[p] == '2') p2++;
        }
        cout << (n - best) << "\n";
    }
    return 0;
}
