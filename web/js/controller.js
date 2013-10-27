// declare a module
var myAppModule = angular.module('urlur', ['ngCookies']);

/*
	Setting up CORS
	Removing header X-Requested-With, Content-Type
	Adding useXDomain , withCredentials
*/
myAppModule.config(['$routeProvider','$httpProvider', function($routeProvider, $httpProvider){
	delete $httpProvider.defaults.headers.common["X-Requested-With"];
	delete $httpProvider.defaults.headers.common["content-type"];
	$httpProvider.defaults.useXDomain = true;
	$httpProvider.defaults.withCredentials = true;
	//$httpProvider.defaults.headers.common["Access-Control-Allow-Credentials"] = true;

	$routeProvider.when('/',{
			templateUrl : "login.html",
			controller : "loginCtr"
		}
	);

	$routeProvider.when('/home',{
			templateUrl : "home.html",
			controller : "postCtr"
		}
	);

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
		templateUrl : 'add-url-modal.html'
	};

});

/*
	Creating a directive to create a DOM element <addgroup>
*/
myAppModule.directive("addgroup", function(){
	return{
		restrict : 'E',
		templateUrl : 'add-group-modal.html'
	};

});

/*
	Creating a directive to create a DOM element <removemodal>
*/
myAppModule.directive("removemodal", function(){
	return{
		restrict : 'E',
		templateUrl : 'remove-modal.html'
	};

});

/*
	Creating a directive to create a DOM element <sharegroup>
*/
myAppModule.directive("sharegroup", function(){
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
		templateUrl : 'join-group-modal.html'
	};

});

/*
	Post Controller
	Controller for home.html
*/
myAppModule.controller("postCtr", function ($scope, $http, $location, apiEndPoint){
	
	/*
		initializing models
	*/
	$scope.currentGroup;
  $scope.posts = [];
  $scope.flags = {};
  $scope.joinGroup = {};
  $scope.remove = {};

  /*
		Constants
	*/
  $scope.GROUP = "group";
  $scope.POST = "post";

  /*
		method to fire http request & GET posts for a group
		group is specified by $scope.currentGroup
	*/
	$scope.getData = function(){
		var me = this;
		
		// check if any group is selected
		if(typeof $scope.currentGroup !== "undefined"){
				var groupParam = "group_id="+$scope.currentGroup._id;

				// HTTP request to get posts
		    $http({method: 'GET', url : apiEndPoint+"/post?"+groupParam, withCredentials: true}).success(
                    function(data, status, headers, config){
                      
                      $scope.posts = data.data;
						        	
                    }).error(
	                    function(data, status, headers, config){
	                      console.log("posts call fail");
	                      $scope.checkForRedirect(status, 302);
                    }
      			);
		}
		    
	};

	/*
		set isAddUrlModal boolean to true.
		this will show the Add Post Modal
	*/
	$scope.showAddURLModal = function(){
		$('#addURLProgress').hide();
		$scope.flags.isAddURLModal = true;
	};

	/*
		set isAddGroupModal boolean to true.
		this will show the Add Group Modal
	*/
	$scope.showAddGroupModal = function(){
		$('#addGroupProgress').hide();
		$scope.flags.isAddGroupModal = true;
	};

	/*
		set isShareGroupModal boolean to true.
		this will show the Share Group Modal
	*/
	$scope.showShareGroupModal = function(){
		$scope.flags.isShareGroupModal = true;
	};

	/*
		set isJoinGroupModal boolean to true.
		this will show the Join Group Modal
	*/
	$scope.showJoinGroupModal = function(){
		$('#joinGroupProgress').hide();
		$scope.flags.isJoinGroupModal = true;
	};

	
	/*
		method called when user searches posts based on keywords
	*/
	$scope.search = function(){
	
		var me = this;
		var query = this.searchQuery;
		// encode the query with keywords, as this goes in the URL
		query = encodeURIComponent(query);
	
		// fire http reqest to search user query for posts
    $http({method: 'GET', url : apiEndPoint+"/search?q="+query, withCredentials: true}).success(
                    function(data, status, headers, config){
                      
                      $scope.posts = data.data;
						        	
                    }).error(
	                    function(data, status, headers, config){

	                      console.log("search call fail");

	                      // check for status code
	                      // if 302, redirect to login page
	                      $scope.checkForRedirect(status, 302);
                    }
      			);

	};


	/*
		handler for groupSelected event - triggers getData()
	*/
	$scope.$on('groupSelected', function(event) { 
		 $scope.getData();
	});


	/*
		handler for groupLoaded event - triggers lead selection
	*/
	$scope.$on('groupsLoaded', function(event) { 
		var groupsDOM = $('.group-item');
		var firstGroupDOM = $(groupsDOM[0]).children();
		$(firstGroupDOM).trigger('click');
	});


  /*
		method to get the url details from modal dialog & send it to the backend
	*/
  $scope.addUrl = function(evt){
  		// get the user inputs
  		// fire POST request

  		var buttonRef = $('#submitURL');
  		buttonRef.button('loading');
  		$('#addURLProgress').show();

  		if($scope.newPost == undefined){
  			// display error message for null value
  			alert("check input");
  			buttonRef.button('reset');
  			$('#addURLProgress').hide();
  			return ;
  		}

  		var newPostData = $scope.newPost;

  		// check for user input null values
  		if(newPostData.ipTitle && newPostData.ipURL && newPostData.ipGroup && newPostData.ipTags){

  			var result = $scope.checkBlanks(newPostData);

  			if(result == 111){
  				// no blank fields
  				var payloadObj = {};

		  		payloadObj.title = encodeURIComponent(newPostData.ipTitle);
		  		payloadObj.link = newPostData.ipURL;
		  		payloadObj.category = null;
		  		payloadObj.groups = newPostData.ipGroup._id;

		  		if(typeof newPostData.ipTags !== "undefinded"){
		  			var tagsArray = newPostData.ipTags.split(",");
			  		var correctedTags = [];
			  		
			  		// check for tags starting with space
			  		$.each(tagsArray, function(idx,tag){
			  			
			  			// trim tag to remove extra spaces
			  			tag = tag.trim();
			  			correctedTags.push(tag);

			  		});	
		  		}
		  		

		  		payloadObj.tags = correctedTags;

		  		$('#frmAddURL').hide();
		  		// fire http reqest to search user query for posts

			    $http({method: 'PUT', url: apiEndPoint+'/post', 
							withCredentials: true,
							headers: {'Content-Type': 'application/x-www-form-urlencoded'},
							data:"data="+JSON.stringify(payloadObj)
					}).success(function(data, status, headers, config){

								$('#addURLProgress').hide();
								var buttonRef = $('#submitURL');
								buttonRef.button('reset');

								$('#addURLModal').modal('hide');
		  					$('#frmAddURL').show(); 
		  					$scope.newPost = {};

		  					$scope.flags.isAddURLModal = false;
		  					$scope.getData();  

					}).error(function(data, status, headers, config){
								console.log("addurl fail");
								$scope.checkForRedirect(status, 302);
					});

  			} else{
  				// display error message
  				// ask user to input meaningful text rather than blank values
  				alert("check input -> blanks");
	  			buttonRef.button('reset');
	  			$('#addURLProgress').hide();
	  			return ;
  			}
  			
	  	} else{

	  		// display error message. Ask user to check for null values
	  		alert("check input");
  			buttonRef.button('reset');
  			$('#addURLProgress').hide();
  			return ;
	  	}


  		
  };


  /*
		method to get the add new group from modal dialog & send it to the backend
	*/
  $scope.addGroup = function(){
		
		var groupName = this.newGroupName;
		var payloadObj = {};
		payloadObj.group_name = groupName;
		var payload = "data="+JSON.stringify(payloadObj);
		console.log(payload);

		$('#addGroupProgress').show();
  	$('#frmAddGroup').hide();
  	$('#submitGroup').button('loading');

		$http({method: 'POST', url: apiEndPoint+'/group', 
					withCredentials: true,
					headers: {'Content-Type': 'application/x-www-form-urlencoded'},
					data:"data="+JSON.stringify(payloadObj)
			}).success(function(data, status, headers, config){
											
								$('#submitGroup').button('reset');
								$('#addGroupModal').modal('hide');
		  					$('#frmAddGroup').show();  

		  					$scope.newGroupName = "";
		  					$scope.flags.isAddGroupModal = false;
								$scope.getUserInfo();  

					}).error(function(data, status, headers, config){
											console.log("addgroup fail");
											$scope.checkForRedirect(status, 302);
									}
							);

	};


	/*
		method to join an existing group by entering the sharerID into modal dialog & send it to the backend
	*/
	$scope.joinGroup = function(){
		
		var groupSharer = this.joinGroupData.sharer;

		$('#joinGroupProgress').show();
  	$('#frmJoinGroup').hide();
  	$('#submitJoinGroup').button('loading');

			$http({method: 'POST', url: apiEndPoint+'/group/join/'+groupSharer, withCredentials: true}).success(
										function(data, status, headers, config){
											
											console.log("joingroup success");
											if(data.error){
												console.log(data.data[0]);
											}
												$('#submitJoinGroup').button('reset');
												$('#joinGroupModal').modal('hide');
						  					$('#frmJoinGroup').show();  

						  					$scope.flags.isJoinGroupModal = false;

						  					//reset data
						  					$scope.joinGroupData = {};

											$scope.getUserInfo();
										}
							).error(
									function(data, status, headers, config){
											console.log("joingroup fail");
											$scope.checkForRedirect(status, 302);
									}
							);

	};


  /*
		Method called when user selects any group from the sidebar
	*/
	$scope.selectGroup = function(evt, group){

		// save the selected group in the factory - shared data
		$scope.currentGroup = group;
		
		// change css class for selected group
		$('.group-item').removeClass('active');
		$(evt.currentTarget).parent().addClass('active');

		// fire groupSelected event, which triggers getData() in postCtr
 		$scope.$emit('groupSelected');
		
	};


	/*
		Method called when user clicks share icon for any group on the sidebar
		This will open the confirmation modal
	*/
	$scope.onShareGroup = function(evt, group){
		
		$scope.flags.isShareGroupModal = true;

		$scope.sharedGroup = {};
		$scope.sharedGroup.hash = group.hash;
		$scope.sharedGroup.name = group.name;

	};


	/*
		Method called when user clicks remove icon for any group on the sidebar
		This will open the confirmation modal
	*/
	$scope.onRemoveGroup = function(evt, group){
		$scope.flags.isRemoveModal = true;
		
		$scope.remove.type = $scope.GROUP;
		$scope.remove.data = group;
		$scope.remove.desc = group.name;
	};


	/*
		Method called when user clicks remove icon for any post
		This will open the confirmation modal
	*/
	$scope.onRemovePost = function(evt, post){
		$scope.flags.isRemoveModal = true;
		
		$scope.remove.type = $scope.POST;
		$scope.remove.data = post;
		$scope.remove.desc = post.title;
	};


	/*
		Method called when user clicks Logout
		TODO 
			* check why this goes into error callback
			* on success, redirect to signin page
	*/
	$scope.logout = function(){
						$http({method: 'POST', url: apiEndPoint+'/logout', withCredentials: true}).success(
										function(data, status, headers, config){
											console.log("logout success");
											
											// redirect to login screen
											$location.path("/");
										}
							).error(
									function(data, status, headers, config){
											console.log("logout fail");
									}
							);
	};


	/*
		Method called to get user info with username, his groups
		This is called on page load
	*/
	$scope.getUserInfo = function(){
					
						$http({method: 'GET', url : apiEndPoint+"/user/info", withCredentials: true}).success(
                    function(data, status, headers, config){
                      
                      $scope.groups = data.data[0].groups;
						        	$scope.uname = data.data[0].name;
						        	
						        	if($scope.groups.length > 0){
						        		// fire groupSelected event, which triggers getData() in postCtr
						        		setTimeout(function() {
						        			$scope.$emit('groupsLoaded');	
						        		}, 100);
 												
						        	} else{
						        		// No groups present => no posts
						        		// therefore, make posts model empty
						        		$scope.posts = [];
						        	}

                    }).error(
	                    function(data, status, headers, config){
	                      console.log("userinfo fail");
	                      $location.path("/");
                    }
      			);
	};


	/*
		Method called when user clicks remove icon on group or post
		This method checks for the type of object which triggered remove & calls corresponding object's remove method
	*/
	$scope.onRemoveItem = function(){

		$('#removeItem').button('loading');
		$('#removeItemProgress').show();
		
		if($scope.remove.type == $scope.GROUP){
			$scope.removeGroup();
		} else{
			$scope.removePost();
		}
	};


	/*
		Method called to remove a group
	*/
	$scope.removeGroup = function(){
			var groupId = $scope.remove.data._id;
				
			$http({method: 'delete', url: apiEndPoint+'/group/'+groupId, withCredentials: true}).success(
										function(data, status, headers, config){
											
											// on success remove modal
											console.log("group remove success");
											$('#removeItem').button('reset');
											$('#removeItemProgress').hide();
											$scope.flags.isRemoveModal = false;
											$('#removeModal').modal('hide');

											// get new data
											$scope.getUserInfo();
										}
			).error(
									function(data, status, headers, config){
										console.log("remove fail");
										$scope.checkForRedirect(status, 302);
									}
			);
	};


	/*
		Method called to remove a post
	*/
	$scope.removePost = function(){
			var postId = $scope.remove.data._id;
				
			$http({method: 'delete', url: apiEndPoint+'/post/'+postId, withCredentials: true}).success(
										function(data, status, headers, config){
											
											// remove modal
											console.log("post remove success");
											$('#removeItem').button('reset');
											$('#removeItemProgress').hide();
											$scope.flags.isRemoveModal = false;
											$('#removeModal').modal('hide');

											// get new data
											$scope.getData();
										}
			).error(
										function(data, status, headers, config){
											console.log("remove fail");
											$scope.checkForRedirect(status, 302);
										}
			);
	};

	$scope.checkBlanks = function(postObj){
		
		var bitResult = 0;
		
		if(postObj.ipTitle.trim().length > 0){
			bitResult = 100;
		}

		if(postObj.ipURL.trim().length > 0){
			bitResult = bitResult + 10;
		}

		if(postObj.ipTags.trim().length > 0){
			bitResult = bitResult + 1;	
		}		

		return bitResult;
	}
	/*
		util method to check if the response status is equal to @param2 status
		if true, redirect to index.html
	*/
	$scope.checkForRedirect = function(responseStatus, status){

			if(responseStatus == status){
				// display error : User not logged in
				alert("User not logged in");
				$location.path("/");
			}
	};

	// explicitly load group data on page load
	$scope.getUserInfo();

});

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
						        	
						        	if($scope.groups.length > 0){
						        		
						        		// this indicated user is already logged in
						        		// redirect him to the home page
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
	                    $scope.authError = data.data[0];
	            		$('#alert-container').show();
                    }
      );

    } else{
            // throw alert for wrong username password
            $scope.authError = "Check username / password";
            $('#alert-container').show();
    }
		
	};



	/*
		Method called to sigup the user with his details
	*/  
	$scope.register = function(){
		
		var me = this;
    if(this.rgName != undefined && this.rgEmail != undefined && this.rgPwd != undefined && this.rgRepeat != undefined){
      
      var xsrf = $.param({"email": this.rgEmail,"password":this.rgPwd,"verify":this.rgRepeat,"name":this.rgName});
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

	$scope.getUserInfo();
  	
});
