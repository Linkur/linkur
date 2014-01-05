
/*
	Post Controller
	Controller for home.html
*/
myAppModule.controller("postCtr", function ($scope, $http, $location, apiEndPoint){
	
  $http.defaults.useXDomain = true;
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

    var operation = {};
    operation.id = 0;
    operation.desc = "Add";
    
    $scope.post = {};
    $scope.post.operation = operation;
		$('#addURLProgress').hide();
		$scope.flags.isAddURLModal = true;
    $scope.setFocus($('#urlmodal-title'));
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
  $scope.addPost = function(payloadObj){
  		// get the user inputs
  		// fire PUT request

      $http({method: 'PUT', url: apiEndPoint+'/post', 
          withCredentials: true,
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          data:"data="+JSON.stringify(payloadObj)
      }).success(function(data, status, headers, config){
            // reset the buttons
            // hide the modal
            $('#addURLProgress').hide();
            var buttonRef = $('#submitURL');
            buttonRef.button('reset');
            $('#addURLModal').modal('hide');
              $('#frmAddURL').show(); 

              // reset the inout model
              $scope.newPost = {};
              $scope.flags.isAddURLModal = false;
              
              // refresh data
              $scope.getData();  

      }).error(function(data, status, headers, config){
            console.log("addurl fail");
            $scope.checkForRedirect(status, 302);
      });
/*
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

*/
  		
  };


  /*
		method to get the add new group from modal dialog & send it to the backend
	*/
  $scope.addGroup = function(){
		
		var groupName = this.newGroupName;
		var payloadObj = {};
		payloadObj.group_name = encodeURIComponent(groupName);
		var payload = "data="+JSON.stringify(payloadObj);
		console.log(payload);

		$('#addGroupProgress').show();
	  	$('#frmAddGroup').hide();
	  	$('#submitGroup').button('loading');

		$http({method: 'PUT', url: apiEndPoint+'/group', 
					withCredentials: true,
					headers: {'Content-Type': 'application/x-www-form-urlencoded'},
					data:"data="+JSON.stringify(payloadObj)
			}).success(function(data, status, headers, config){
								
								// reset buttons
								// hide modal
								$('#submitGroup').button('reset');
								$('#addGroupModal').modal('hide');
		  						$('#frmAddGroup').show();
		  						$scope.flags.isAddGroupModal = false;

		  						// reset input model
		  						$scope.newGroupName = "";

		  						// refresh data
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

											// reset buttons
											// hide modal
											$('#submitJoinGroup').button('reset');
											$('#joinGroupModal').modal('hide');
						  					$('#frmJoinGroup').show();  
											$scope.flags.isJoinGroupModal = false;

						  					//reset input model
						  					$scope.joinGroupData = {};

						  					// refresh data
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

		Input model $scope.remove is used as a generic model for remove group & remove post
		The property "type" signifies what object is being removed by user
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

		Input model $scope.remove is used as a generic model for remove group & remove post
		The property "type" signifies what object is being removed by user
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
											$location.path("/login");
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
	                      $location.path("/login");
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
		
		// determine the type of object beeing removed & calls the respective remove method
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
				
			$http({method: 'DELETE', url: apiEndPoint+'/group/'+groupId, withCredentials: true}).success(
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
				
			$http({method: 'DELETE', url: apiEndPoint+'/post/'+postId, withCredentials: true}).success(
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

	/*
		Event handler for Edit post, which opens the Modal with data binding
	*/
	$scope.onEditPost = function(evt, post){
			console.log(post);	
			console.log(evt);	
     
      var operation = {};
      operation.id = 1;
      operation.desc = "Edit";

      $scope.post = {};
      $scope.post.operation = operation;
      $scope.post.data = {};
      // bind data to the modal
      $scope.post.data._id = post._id;
      $scope.post.data.ipTitle = post.title;
      $scope.post.data.ipURL = post.link;
      var visibleTags = post.tags[0];
      for(var i=1; i<post.tags.length; i++ ){
       visibleTags +=", "+post.tags[i];
      }
      $scope.post.data.ipTags = visibleTags;
      
      // bind the current model data to ipModel
      $.each($scope.groups, function(idx, value){
        if(value._id == post.group){
          $scope.post.data.ipGroup = value;
        }
      });

      $('#addURLProgress').hide();
      $scope.flags.isAddURLModal = true;
      $scope.setFocus($('#urlmodal-title'));

	};

  $scope.editPost = function(payloadObj){
  		// get the user inputs
  		// fire POST request

      $http({method: 'POST', url: apiEndPoint+'/post', 
          withCredentials: true,
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          data:"data="+JSON.stringify(payloadObj)
      }).success(function(data, status, headers, config){
            // reset the buttons
            // hide the modal
            $('#addURLProgress').hide();
            var buttonRef = $('#submitURL');
            buttonRef.button('reset');
            $('#addURLModal').modal('hide');
              $('#frmAddURL').show(); 

              // reset the inout model
              $scope.newPost = {};
              $scope.flags.isAddURLModal = false;
              
              // refresh data
              $scope.getData();  

      }).error(function(data, status, headers, config){
            console.log("addurl fail");
            $scope.checkForRedirect(status, 302);
      });
  }

  $scope.onSubmitPost = function(evt, post){
    // Do basic user input check
    // call respective HTTP handler to perform operation based on the operation type
   		// get the user inputs
  		// fire POST request

  		var buttonRef = $('#submitURL');
  		buttonRef.button('loading');
  		$('#addURLProgress').show();

  		if(post.data == undefined){
  			// display error message for null value
  			alert("check input");
  			buttonRef.button('reset');
  			$('#addURLProgress').hide();
  			return ;
  		}

  		var newPostData = post.data;

  		// check for user input null values
  		if(newPostData.ipTitle && newPostData.ipURL && newPostData.ipGroup){

  			var result = $scope.checkBlanks(newPostData);

  			// if bitResult is 111, user input is valid
			// else, one of the mandatory fields are empty
  			if(result == 111 || result == 110){
  				// no blank fields
  				var payloadObj = {};
          
		  		payloadObj.title = encodeURIComponent(newPostData.ipTitle);
		  		payloadObj.link = encodeURIComponent(newPostData.ipURL);
		  		payloadObj.category = null;
		  		payloadObj.groups = newPostData.ipGroup._id;

          var correctedTags = [];
		  		if(typeof newPostData.ipTags !== "undefined" && newPostData.ipTags.length > 0){
		  			var tagsArray = newPostData.ipTags.split(",");
			  		
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
          if(post.operation.id == 00){
            $scope.addPost(payloadObj);
          } else{
            payloadObj._id = newPostData._id;
            $scope.editPost(payloadObj);
          }
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
  }

	$scope.checkBlanks = function(postObj){
		
		var bitResult = 0;
		
		if(postObj.ipTitle.trim().length > 0){
			bitResult = 100;
		}

		if(postObj.ipURL.trim().length > 0){
			bitResult = bitResult + 10;
		}

		if(postObj.ipTags && postObj.ipTags.trim().length > 0){
			bitResult = bitResult + 1;	
		}		

		// if bitResult is 111, user input is valid
		// else, one of the mandatory fields are empty
		return bitResult;
	}

	/*
		event handler
		called when user clicks on "Change Password" link in home page
	*/
	$scope.navigateToSettings = function(evt){
		$location.path("/#/settings");
	}

	/*
		util method to check if the response status is equal to @param2 status
		if true, redirect to index.html
	*/
	$scope.checkForRedirect = function(responseStatus, status){

			if(responseStatus == status){
				// display error : User not logged in
				alert("User not logged in");
				$location.path("/login");
			}
	};

  /*
   util method to explicitly set focus for an element
  */
  $scope.setFocus = function(elem){
    setTimeout(function(){
      $(elem).focus();
    }, 200);
  };

	// explicitly load group data on page load
	$scope.getUserInfo();

});
