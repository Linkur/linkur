
// SETTINGS CONTROLLER 

myAppModule.controller("settingsCtr", function($scope,$http, $location, apiEndPoint){
	
	$http.defaults.useXDomain = true;

	/*
		Method called when change password is click from settings screen
	*/
	$scope.onChangePassword = function(){

		var me = this;

		// check for null inputs
		if(this.changePwd != undefined && 
			this.changePwd.oldPwd != undefined && 
			this.changePwd.newPwd != undefined && 
			this.changePwd.repeat != undefined){
			
				// check for blank inputs && equality
				if(this.changePwd.oldPwd.trim().length > 0 &&
					this.changePwd.newPwd.trim().length > 0 &&
					this.changePwd.repeat.trim().length > 0 && 
					this.changePwd.newPwd === this.changePwd.repeat){

						// prepare the payload
						var xsrf = $.param({"old_password": this.changePwd.oldPwd,"new_password":this.changePwd.newPwd});

						$http({method: 'POST', 
							url : apiEndPoint+"/user/password",
							withCredentials: true, 
							headers: {'Content-Type': 'application/x-www-form-urlencoded'}, 
							data: xsrf})
						      .success(
					                    function(data, status, headers, config){

					                      // If no error in response & http status code = 200
					                      // redirect to home page
					                      if(data.error == false && status == "200"){
					                        // redirect to /home
					                        alert("change password success");
					                        console.log("change password success");
					                        $location.path("/home");
					                      } else{
					                      	// error logging in the user
					                    	// display the error message on screen	
					                      	
					                      	alert("Error changing password");
					                      	$scope.authError = data.data[0];
						            		$('#alert-container').show();
					                      }
						                })
						      .error(
					                    function(data, status, headers, config){
					                    // error logging in the user
					                    // display the error message on screen	
					                     	alert("change password fail");
						                    $scope.authError = data.data[0];
						            		$('#alert-container').show();
					                    });
				}
		}
	};

});

