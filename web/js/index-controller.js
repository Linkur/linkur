// declare a module
var myAppModule = angular.module('myApp', []);

myAppModule.config(['$httpProvider', function($httpProvider){
  delete $httpProvider.defaults.headers.common['X-Requested-With'];
	delete $httpProvider.defaults.headers.common["Content-Type"];

  console.log($httpProvider.defaults.headers.common);
	$httpProvider.defaults.useXDomain = true;
  console.log($httpProvider.defaults);
}]);

function loginCtr($scope,$http){
	$http.defaults.useXDomain = true;

	$scope.login = function(){
		
		var me = this;
    if(this.emailVal != undefined && this.pwdVal != undefined){
      
      var xsrf = $.param({"email": this.emailVal,"password":this.pwdVal});

      $http({method: 'POST', url : "http://192.168.1.11:5000/signin", withCredentials: true, headers: {'Content-Type': 'application/x-www-form-urlencoded'}, data: xsrf}).success(
                    function(data, status, headers, config){
                      alert("signin success");
                    }
      ).error(
                    function(data, status, headers, config){
                      alert("signin fail");
                    }
      );

    } else{
            // throw alert for wrong username password
            $scope.authError = "Check username / password";
            $('#alert-container').show();
    }
		
	};

  
   		
	$scope.register = function(){
		
		var me = this;
    if(this.rgName != undefined && this.rgEmail != undefined && this.rgPwd != undefined && this.rgRepeat != undefined){
      
      var xsrf = $.param({"email": this.rgEmail,"password":this.rgPwd,"verify":this.rgRepeat,"name":this.rgName});
      $.ajax({
        crossDomain:true,
        url : "http://localhost:5000/signup",
              type : "POST",
              data: xsrf,
               xhrFields: {
        withCredentials: true
        }
      }).success(function(data, status, header) {
            console.log(data);
            // check for statusCode. if success, redirect to home.html
            if(data.error == false){
              $scope.authResult = "Hurray! Registration successful";
              $('#alert-container').show();
            } else{
              // throw error
              $scope.authResult = "Error registering user";
              $('#alert-container').show();
            }
      });
    } else{
            // throw alert for wrong username password
            $scope.authError = "Check user info for registration";
            $('#alert-container').show();
    }
		
	};


  	
};



