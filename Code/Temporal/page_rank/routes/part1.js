var express = require('express');
var router = express.Router();
var fs = require('fs');
var graph = require('ngraph.graph')();
var pagerank = require('ngraph.pagerank');

var contents = fs.readFileSync('pagerank_without_weight.txt', 'utf8');
var t = contents.split('\n');

for(var i=0;i<t.length;i++)
{
  var val = t[i].split(" ");
  graph.addLink(val[0].replace(/(\r\n|\n|\r)/gm,""), val[1].replace(/(\r\n|\n|\r)/gm,""));
}

var rank = pagerank(graph);

var file = fs.createWriteStream('rank_nodes_pagerank_without_weight.txt');
file.on('error', function(err) { /* error handling */ });

for(x in rank)
{
  file.write(x+" "+rank[x] +"\n");
}

file.end();

console.log('Done!');

module.exports = router;