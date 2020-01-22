'use strict';
angular.module('App', ['ui.router','ngResource','ngDialog','ui.bootstrap','ngMaterial', 'ngMessages','ngCookies'])
.config(function($stateProvider, $urlRouterProvider) {
    $stateProvider
            .state('app', {
                url:'/',
                views: {
                    'header': {
                        templateUrl : 'views/header.html'
                    },
                    'content': {
                        controller  : 'StartController'
                    },
                    'footer': {
                        templateUrl : 'views/footer.html'
                    }
                }

            })
			.state('app.home', {
                url:'home',
                views: {
                    'content@': {
                        templateUrl : 'views/home.html',
                        controller: 'HomeController'
                    }
                }
            })
            ;
            $urlRouterProvider.otherwise('/');
        })
;
