'use strict';

angular.module('App')

.controller('StartController', ['$scope', '$state', function ($scope, $state) {
    $state.go('app.home', {}, {reload: true});
}])


.controller('HomeController', ['$scope', '$window', 'model', function ($scope, $window, model) {
  	$scope.browseurl1 = function(){
		$window.open($scope.url1, '_blank');
  	}
  	$scope.browseurl2 = function(){
		$window.open($scope.url2, '_blank');
  	}
    $scope.clear = function(){
      $scope.resulttext=""
      $scope.url1=null
      $scope.url2=null
    };
    $scope.process = function(){
        var url1 = $scope.url1;
        var url2 = $scope.url2;
        var base = "http://stackoverflow.com/questions/";
        var id1 = $scope.url1.split("/")[4];
        var id2 = $scope.url2.split("/")[4];
        model.getResults(id1, id2, function(answer){
        	if(answer == "1")
	        	$scope.resulttext = "Result : Q1 > Q2 : (Q1 is more difficult than Q2)";
	        else if(answer == "2")
	        	$scope.resulttext = "Result : Q1 < Q2 : (Q2 is more difficult than Q1)";
	        else 
	        	alert('Result from server cannot be interpreted!');
        });
    };
}])

.controller('HeaderController', ['$scope', function ($scope) {
   
}])

;