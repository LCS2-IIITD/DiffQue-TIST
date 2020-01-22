'use strict';

angular.module('App')
.constant("baseURL","http://192.168.16.208:3000/api/")
.factory('$localStorage', ['$window', function ($window) {
    return {
        store: function (key, value) {
            $window.localStorage[key] = value;
        },
        get: function (key, defaultValue) {
            return $window.localStorage[key] || defaultValue;
        },
        remove: function (key) {
            $window.localStorage.removeItem(key);
        },
        storeObject: function (key, value) {
            $window.localStorage[key] = JSON.stringify(value);
        },
        getObject: function (key, defaultValue) {
            return JSON.parse($window.localStorage[key] || defaultValue);
        }
    };
}])
.service('model', ['$localStorage','baseURL', '$http', function ($localStorage, baseURL, $http) { 
this.getResults = function(id1, id2, next){
        $http({
            method: 'POST',
            url: baseURL+'questions/',
            data: {id1: id1, id2: id2}
          }).then(function successCallback(response) {
                if(response.status==200){
                   next(response.data);
                }
                else
                 {
                    alert('server failed to serve');
                 }
            }, function errorCallback(response) {
                  {
                    alert('failed to contact server');
                 }
            });
    };
}])

;
