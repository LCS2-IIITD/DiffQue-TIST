var fs = require('fs');
var contents = fs.readFileSync('init_edges_weight.txt', 'utf8');
var t = contents.split('\n');
weight_dict = {}
for(var i=0;i<t.length;i++)
{
  var val = t[i].split(" ");
  weight_dict[val[0]] = parseFloat(val[1])
}
console.log(weight_dict)
