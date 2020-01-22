#include <bits/stdc++.h>
using namespace std;

#define display(arr,s,e) for(i=s; i<=e; i++) cout<<arr[i]<<" ";
#define mset(arr,x) memset(arr,x,sizeof(arr))

#define MOD 1000000007
#define epsilon 0.000000000001
#define I_MAX 9223372036854775807

#define rep(i,s,e) for(i=s;i<=e;i++)
#define rrep(i,s,e) for(i=s;i>=e;i--)
#define endl "\n"

#define ll long long
#define mid(a,b) ((a)+((b-a)/2))
#define min(a,b) ((a)<(b)?(a):(b))
#define max(a,b) ((a)>(b)?(a):(b))

// Useful STL commands:
#define pb push_back
#define mp make_pair
#define f first
#define s second
#define si set<int>
#define vi vector<int>
#define ii pair<int,int>
#define sii set<ii>
#define vii vector<ii>
#define all(c) c.begin(),c.end()
#define tr(c,it) for(auto it=c.begin();it!=c.end();++it)

#define DEBUG
// debugging
#ifdef DEBUG
#define trace1(x)                    cerr << #x << ": " << x << endl;
#define trace2(x, y)                 cerr << #x << ": " << x << " | " << #y << ": " << y << endl;
#define trace3(x, y, z)              cerr << #x << ": " << x << " | " << #y << ": " << y << " | " << #z << ": " << z << endl;
#define trace4(a, b, c, d)           cerr << #a << ": " << a << " | " << #b << ": " << b << " | " << #c << ": " << c << " | " << #d << ": " << d << endl;
#define trace5(a, b, c, d, e)        cerr << #a << ": " << a << " | " << #b << ": " << b << " | " << #c << ": " << c << " | " << #d << ": " << d << " | " << #e << ": " << e << endl;
#define trace6(a, b, c, d, e, f)     cerr << #a << ": " << a << " | " << #b << ": " << b << " | " << #c << ": " << c << " | " << #d << ": " << d << " | " << #e << ": " << e << " | " << #f << ": " << f << endl;
#else
#define trace1(x)
#define trace2(x, y)
#define trace3(x, y, z)
#define trace4(a, b, c, d)
#define trace5(a, b, c, d, e)
#define trace6(a, b, c, d, e, f)
#endif

ll gcd(ll a, ll b)
{
    if( (a == 0) || (b == 0) )
        return a + b;
    return gcd(b, a % b);
}

ll pow_mod(ll a, ll b)
{
    ll res = 1;
    while(b)
    {
        if(b & 1)
            res = (res * a)%MOD;
        a = (a * a)%MOD;
        b >>= 1;
    }
    return res;
}

bool isPrime(ll a)
{
	for(int i=3; (i*i)<=a; i+=2)
    {
		if( (a%i)==0 )
		{
			return false;
		}
	}
	return true;
}

bool visited[500010];
vector< pair<ll, ll> > vc;
vector< ll > adj[500010];
map<ll, ll> ma;
void dfs( ll so )
{
    visited[so] = 1;
    ll i, kk = adj[so].size(), opop;

    rep(i, 0, kk-1)
    {
        opop = adj[so][i];
        if( visited[opop] )
        {
            continue;
        }
        dfs( opop );
    }
}
int main()
{
    freopen("mse.txt","r",stdin);

    ll i, j, N, A, B, pp = 1, ans = 0;

    cin >> N;
    rep(i, 1, N)
    {
       cin >> A >> B;
       if( !ma[A] )
       {
           ma[A] = pp++;
       }
       if( !ma[B] )
       {
           ma[B] = pp++;
       }
       vc.pb( mp(A, B) );
    }
    //trace1(pp)
    rep(i, 1, N)
    {
       A = vc[i-1].f;
       B = vc[i-1].s;
       A = ma[A];
       B = ma[B];
       adj[A].pb(B);
       adj[B].pb(A);
    }

    rep(i, 1, pp-1)
    {
        if( !visited[i] )
        {
            dfs(i);
            ans++;
        }
    }
    cout << ans;

    return 0;
}
