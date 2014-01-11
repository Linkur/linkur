
// LOGIN CONTROLLER 

myAppModule.controller("loginCtr", function($scope,$http, $location, apiEndPoint){
	
	$http.defaults.useXDomain = true;


	/*
		Method called to get user info with username, his groups
		This is called on page load
	*/
	$scope.getUserInfo = function(){
					
						$http({method: 'GET', url : apiEndPoint+"/user/info", withCredentials: true}).success(
                    function(data, status, headers, config){
                      
                      $scope.groups = data.data[0].groups;
						        	$scope.uname = data.data[0].name;	
						        		// this indicated user is already logged in
						        		// redirect him to the home page
						        		if($location.path() != "/settings"){
						        			$location.path("/home");	
						        		}

                    }).error(
	                    function(data, status, headers, config){
	                      console.log("userinfo fail");
                    }
      			);
	};


	/*
		Method called to sigin the user with his credentials
	*/
	$scope.login = function(){
		
		var me = this;
    if(this.emailVal != undefined && this.pwdVal != undefined){
      
      var xsrf = $.param({"email": this.emailVal,"password":this.pwdVal});

      $http({method: 'POST', url : apiEndPoint+"/signin", withCredentials: true, headers: {'Content-Type': 'application/x-www-form-urlencoded'}, data: xsrf})
      .success(
                    function(data, status, headers, config){

                      // If no error in response & http status code = 200
                      // redirect to home page
                      if(data.error == false && status == "200"){
                        // redirect to /home
                        console.log("signin success");
                        $location.path("/home");
                      }
                    })
      .error(
                    function(data, status, headers, config){
                    // error logging in the user
                    // display the error message on screen	
                     	alert("signin fail");
	                    $scope.authResult = data.data[0];
                      $('#alert-container').show();
                      $scope.$apply();
                    }
  );

    } else{
            // throw alert for wrong username password
            $scope.authResult = "Check username / password";
            $('#alert-container').show();
            $scope.$apply();
    }
		
	};



	/*
		Method called to sigup the user with his details
	*/  
	$scope.register = function(){
		
		var me = this;
    if(this.rgName != undefined && this.rgEmail != undefined && this.rgPwd != undefined && this.rgRepeat != undefined){
      this.rgEmail = this.rgEmail.toLowerCase();
      var xsrf = $.param({"email": this.rgEmail,"password":this.rgPwd,"verify":this.rgRepeat,"name":this.rgName});

      // TODO: check for blank values

      $.ajax({
        crossDomain:true,
        url : apiEndPoint+"/signup",
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

              // clear input form
              delete $scope.rgName;
              delete $scope.rgEmail;
              delete $scope.rgPwd;
              delete $scope.rgRepeat;

              $scope.$apply();
            } else{
              // throw error
              $scope.authResult = "Error registering user";
              $('#alert-container').show();
              $scope.$apply();
            }
      }).error(function(data, status, header){
          response = JSON.parse(data.responseText);
          $scope.authResult = response.data[0];
          $('#alert-container').show();
          $scope.$apply();
      });
    } else{
            // throw alert for wrong username password
            $scope.authResult = "Check user info for registration";
            $('#alert-container').show();
            $scope.$apply();
    }
		
	};

	// fire get info to check user login & redirect
	$scope.getUserInfo();
  	
});

