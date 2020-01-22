var express = require('express');
var router = express.Router();
var fs = require('fs');
var graph = require('ngraph.graph')();
var pagerank = require('ngraph.pagerank');

infilename = 'edges.txt';
outfilename = 'rank_nodes_pagerank_without_weight.txt';

if(process.argv[2]!=null && process.argv[3]!=null){
	infilename = process.argv[2];
	outfilename = process.argv[3];
}

console.log(infilename + " -> " + outfilename);

var contents = fs.readFileSync(infilename, 'utf8');
var t = contents.split('\n');

for(var i=0;i<t.length;i++)
{
  var val = t[i].split(" ");
  graph.addLink(val[0].replace(/(\r\n|\n|\r)/gm,""), val[1].replace(/(\r\n|\n|\r)/gm,""));
}

var contents = fs.readFileSync('init_edges_weight.txt', 'utf8');
var t = contents.split('\n');
weight_dict = {}
for(var i=0;i<t.length;i++)
{
  var val = t[i].split(" ");
  weight_dict[val[0]] = parseFloat(val[1])
}
// console.log(weight_dict)


var rank = pagerank(graph,weight_dict);

var file = fs.createWriteStream(outfilename);
file.on('error', function(err) { /* error handling */ });
var flush;

for(x in rank)
{
  flush = file.write(x+" "+rank[x] +"\n");
}

file.end();

console.log('Done!');

if (!flush) {
  file.once('finish', () => {
  	console.log('The data has been flushed');
	process.exit(0);
  });
}

module.exports = router;

