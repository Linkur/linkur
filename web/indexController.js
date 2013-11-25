// declare a module
var myAppModule = angular.module('urlur', ['ngCookies']);

/*
	Setting up CORS
	Removing header X-Requested-With, Content-Type
	Adding useXDomain , withCredentials
*/
myAppModule.config(['$routeProvider','$httpProvider', '$locationProvider', function($routeProvider, $httpProvider, $locationProvider){
	delete $httpProvider.defaults.headers.common["X-Requested-With"];
	delete $httpProvider.defaults.headers.common["content-type"];
	$httpProvider.defaults.useXDomain = true;
	$httpProvider.defaults.withCredentials = true;
	//$httpProvider.defaults.headers.common["Access-Control-Allow-Credentials"] = true;

	$routeProvider.when('/login',{
			templateUrl : "login/index.html",
			controller : "loginCtr"
		}
	);

	$routeProvider.when('/home',{
			templateUrl : "home/index.html",
			controller : "postCtr"
		}
	);

	$routeProvider.when('/settings',{
			templateUrl : "settings/index.html",
			controller : "settingsCtr"
		}
	);

	$routeProvider.otherwise({
		redirectTo: "/login"
	});

	//$locationProvider.html5Mode(true).hashPrefix('!');
	//$locationProvider.html5Mode(true);

}]);

/*
	Global variable across the module to store the API endpoint
	All ajax calls use this as base url 
*/
myAppModule.value('apiEndPoint', 'http://localhost:5000');

/*
	Creating a directive to create a DOM element <addurl>
*/
myAppModule.directive("addurl", function(){
	return{
		restrict : 'E',
		templateUrl : 'modals/add-url-modal.html'
	};

});

/*
	Creating a directive to create a DOM element <addgroup>
*/
myAppModule.directive("modals/addgroup", function(){
	return{
		restrict : 'E',
		templateUrl : 'add-group-modal.html'
	};

});

/*
	Creating a directive to create a DOM element <removemodal>
*/
myAppModule.directive("modals/removemodal", function(){
	return{
		restrict : 'E',
		templateUrl : 'remove-modal.html'
	};

});

/*
	Creating a directive to create a DOM element <sharegroup>
*/
myAppModule.directive("modals/sharegroup", function(){
	return{
		restrict : 'E',
		templateUrl : 'share-group-modal.html'
	};

});

/*
	Creating a directive to create a DOM element <joingroup>
*/
myAppModule.directive("joingroup", function(){
	return{
		restrict : 'E',
		templateUrl : 'modals/join-group-modal.html'
	};

});

