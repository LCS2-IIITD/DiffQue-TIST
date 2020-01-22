#include <bits/stdc++.h>
#define maxn 10000000
using namespace std;
vector <int> adj_list[maxn];
bool present[maxn];
bool visited[maxn];
int component[maxn];
int component_counter = 0;
int component_node_count = 0;
void dfs(int v){
	assert(visited[v] == false);
	component[v] = component_counter;
	component_node_count++;
	visited[v] = true;
	for (int i = 0; i < adj_list[v].size(); ++i)
	{
		if (visited[adj_list[v][i]] == false)
			dfs(adj_list[v][i]);
	}
}
int main(int argc, char const *argv[])
{
	memset(present, false, sizeof(present));
	memset(visited, false, sizeof(visited));
	memset(component, 0, sizeof(component));
	int m; cin>>m;
	for (int i = 0; i < m; ++i)
	{
		int a,b; cin>>a>>b;
		adj_list[a].push_back(b);
		adj_list[b].push_back(a);
		present[a] = present[b] = true;
	}
	int max_component_size = 0;
	map <int, int> freq_count;
	for (int i = 0; i < maxn; ++i)
	{
		if(present[i] && visited[i] == false){
			component_counter++;
			component_node_count = 0;
			dfs(i);
			max_component_size = max(max_component_size, component_node_count);
			if(freq_count.count(component_node_count))
				freq_count[component_node_count]++;
			else
				freq_count[component_node_count] = 1;
		}
	}
	cout<<"component_counter "<<component_counter<<endl;
	cout<<"max_component_size "<<max_component_size<<endl;
	for(map<int, int >::const_iterator it = freq_count.begin();it != freq_count.end(); ++it)
	{
	    std::cout << it->first << " " << it->second << "\n";
	}
	return 0;
}