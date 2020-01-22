var express = require('express');
var router = express.Router();
var fs = require('fs');
var graph = require('pagerank.js');

var contents = fs.readFileSync('pagerank_with_weight.txt', 'utf8');
var t = contents.split('\n');

for(var i=0;i<t.length;i++)
{
  var val = t[i].split(" ");
  graph.link(val[0].replace(/(\r\n|\n|\r)/gm,""), val[1].replace(/(\r\n|\n|\r)/gm,""), val[1].replace(/(\r\n|\n|\r)/gm,""));
}

var file = fs.createWriteStream('rank_nodes_pagerank_with_weight.txt');
file.on('error', function(err) { /* error handling */ });

graph.rank(0.85, 0.000001, function (node, rank) 
{
  // console.log("Node " + node + " has a rank of " + rank);
  file.write(node+" "+rank+"\n");
});

console.log('Done!');

module.exports = router;