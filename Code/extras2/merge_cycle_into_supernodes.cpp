#include <bits/stdc++.h>
#define maxn 50000000
#define minimum 31756883
#define maximum 45901563
using namespace std;
vector <int> adj_list[maxn];
vector <int> inverse_adj_list[maxn];
bool visited[maxn];
int start[maxn], end[maxn];
int parent[maxn];
int timer = 0;
bool active[maxn];
int active_counter = maximum - minimum;
bool find_in_vector(vector<int> &a , int e)
{
	return find(a.begin(), a.end(), e) != a.end();
}
void add_to_vector(vector<int> &a, int e){
	if(find_in_vector(a, e) == false)
		a.push_back(e);
}
void compress(int ansector, int child){
	int v = child;
	int length = 0;
	while(v != ansector){
		assert(active[v]);
		assert(v != -1);
		active[v] = false;
		active_counter--;
		length++;
		// cout<<v<<" ";
		v = parent[v];
	}
	// cout<<v<<" ";
	length++;
	// cout<<"Compressing length of "<<length<<" from"<<ansector<<" to "<<child<<" ";
	v = child;
	while(v != ansector){
		for (int i = 0; i < inverse_adj_list[v].size(); ++i)
		{
			int next = inverse_adj_list[v][i];
			if(next == parent[v])
				continue;
			adj_list[next].erase(remove(adj_list[next].begin(), adj_list[next].end(), v), adj_list[next].end());
			add_to_vector(adj_list[next], ansector);
			add_to_vector(inverse_adj_list[ansector], next);
		}
		for (int i = 0; i < adj_list[v].size(); ++i)
		{
			int next = adj_list[v][i];
			add_to_vector(inverse_adj_list[next], ansector);
			add_to_vector(adj_list[ansector], next);
		}
		v = parent[v];
	}
	v = child;
	while(v != ansector){
		adj_list[ansector].erase(remove(adj_list[ansector].begin(), adj_list[ansector].end(), v), adj_list[ansector].end());
		v = parent[v];
	}
	adj_list[ansector].erase(remove(adj_list[ansector].begin(), adj_list[ansector].end(), ansector), adj_list[ansector].end());
	// cout<<"adj_list "<<ansector<<": ";
	// for (int i = 0; i < adj_list[ansector].size(); ++i)
	// 	cout<<adj_list[ansector][i]<<" ";
	// cout<<endl;
}
bool dfs(int v){
	assert(active[v]);
	if (visited[v])
		return false;
	visited[v] = true;
	start[v] = ++timer;
	for (int i = 0; i < adj_list[v].size(); ++i)
	{
		int next = adj_list[v][i];
		if(visited[next] == false){
			parent[next] = v;
			bool found = dfs(next);
			if(found)
				return true;
		}
		else{
			if(start[next] < start[v] && end[next] == -1){
			// if(start[next] < start[v] && end[next] == -1 && parent[v] != next){
				compress(next, v);
				return true;
			}
		}
	}
	end[v] = ++timer;
	return false;
}
void reset(){
	for(int i = minimum; i <= maximum; i++){
		visited[i] = false;
		start[i] = -1;
		end[i] = -1;
		parent[i] = -1;
	}
}
void verify(){
	for (int i = minimum; i <= maximum; ++i)
	{
		if(active[i]){
			for(int j = 0; j < adj_list[i].size(); j++){
				assert(active[adj_list[i][j]]);
			}
		}
	}
}
void print(){
	ofstream myfile ("new_so_no_cycle_edges_2_cycle_too.txt");
	for (int i = minimum; i <= maximum; ++i)
	{
		if(active[i]){
			for(int j = 0; j < adj_list[i].size(); j++){
				myfile<<i<<" "<<adj_list[i][j]<<"\n";
			}
		}
	}
	myfile.close();
}
int main(int argc, char const *argv[])
{
	int m; cin>>m;
	for (int i = 0; i < maxn; ++i){
		if(i >= minimum && i <= maximum)
			active[i] = true;
		else
			active[i] = false;
	}

	for (int i = 0; i < m; ++i)
	{
		int a,b; cin>>a>>b;
		adj_list[a].push_back(b);
		inverse_adj_list[b].push_back(a);
	}
	bool found = true;
	while(found){
		cout<<"Restarted "<<active_counter<<endl;
		// verify();
		found = false;
		reset();
		for (int i = minimum; i <= maximum; ++i)
		{
			if(visited[i] == false && active[i]){
				found = dfs(i);
				if (found)
					break;
			}
		}
	}
	print();
	return 0;
}