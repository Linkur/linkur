// declare a module
var myAppModule = angular.module('urlur', ['ngCookies']);

myAppModule.config(['$routeProvider','$httpProvider', function($routeProvider, $httpProvider){
	delete $httpProvider.defaults.headers.common["X-Requested-With"];
	delete $httpProvider.defaults.headers.common["content-type"];
	$httpProvider.defaults.useXDomain = true;
	$httpProvider.defaults.withCredentials = true;
	//$httpProvider.defaults.headers.common["Access-Control-Allow-Credentials"] = true;

}]);

myAppModule.value('apiEndPoint', 'http://localhost:5000');

myAppModule.directive("addurl", function(){
	return{
		restrict : 'E',
		templateUrl : 'add-url-modal.html'
	};

});

myAppModule.directive("addgroup", function(){
	return{
		restrict : 'E',
		templateUrl : 'add-group-modal.html'
	};

});

myAppModule.directive("removemodal", function(){
	return{
		restrict : 'E',
		templateUrl : 'remove-modal.html'
	};

});

myAppModule.directive("sharegroup", function(){
	return{
		restrict : 'E',
		templateUrl : 'share-group-modal.html'
	};

});

myAppModule.directive("joingroup", function(){
	return{
		restrict : 'E',
		templateUrl : 'join-group-modal.html'
	};

});

function postCtr($scope, $http, $location, apiEndPoint){
	
	//  initialize models
	$scope.currentGroup;
  $scope.posts = [];
  $scope.flags = {};
  $scope.joinGroup = {};
  $scope.remove = {};

  //Constants
  $scope.GROUP = "group";
  $scope.POST = "post";

  // method to fire http request & GET posts
	$scope.getData = function(){
		var me = this;
		//$scope.cookieValue = $cookieStore.get('session');
		
		// check if any group is selected
		if(typeof $scope.currentGroup !== "undefined"){
				var groupParam = "group_id="+$scope.currentGroup._id;
				console.log(groupParam);

				// // HTTP request to get posts

		    $http({method: 'GET', url : apiEndPoint+"/post?"+groupParam, withCredentials: true}).success(
                    function(data, status, headers, config){
                      
                      $scope.posts = data.data;
						        	
                    }).error(
	                    function(data, status, headers, config){
	                      alert("posts call fail");
                    }
      			);
		}
		    
	};

	$scope.showAddURLModal = function(){
		$('#addURLProgress').hide();
		$scope.flags.isAddUrlModal = true;
	};

	$scope.showAddGroupModal = function(){
		$('#addGroupProgress').hide();
		$scope.flags.isAddGroupModal = true;
	};

	$scope.showShareGroupModal = function(){
		$scope.flags.isShareGroupModal = true;
	};

	$scope.showJoinGroupModal = function(){
		$('#joinGroupProgress').hide();
		$scope.flags.isJoinGroupModal = true;
	};

	// method called when user searches for a post
	$scope.search = function(){
	
		var me = this;
		var query = this.searchQuery;
		query = encodeURIComponent(query);
	
		// fire http reqest to search user query for posts

    $http({method: 'GET', url : apiEndPoint+"/search?q="+query, withCredentials: true}).success(
                    function(data, status, headers, config){
                      
                      $scope.posts = data.data;
						        	
                    }).error(
	                    function(data, status, headers, config){
	                      alert("search call fail");
	                      if(status == "302"){
	                      	$.location.path('/index.html');
	                      }
                    }
      			);

	};

	// handler for groupSelected event - triggers getData()
	$scope.$on('groupSelected', function(event) { 
		 $scope.getData();
	});

	// handler for groupLoaded event - triggers lead selection
	$scope.$on('groupsLoaded', function(event) { 
		var groupsDOM = $('.group-item');
		var firstGroupDOM = $(groupsDOM[0]).children();
		$(firstGroupDOM).trigger('click');
	});

  // method to get the url details from modal dialog & send it to the backend
  $scope.addUrl = function(evt){
  		// get the user inputs
  		// fire POST request

  		var buttonRef = $('#submitURL');
  		buttonRef.button('loading');
  		$('#addURLProgress').show();

  		var newPostData = $scope.newPost;
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
	  			while($scope.doesStartWithSpace(tag)){
	  					tag = tag.slice(1,tag.length);
	  			}
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

  					$scope.flags.isAddUrlModal = false;
  					$scope.getData();  

					}).error(function(data, status, headers, config){
											alert("addurl fail");
									}
							);

  };

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

		  					$scope.flags.isAddGroupModal = false;
								$scope.getUserInfo();  

					}).error(function(data, status, headers, config){
											alert("addgroup fail");
									}
							);

	};

	$scope.joinGroup = function(){
		
		var groupSharer = this.joinGroup.sharer;

		$('#joinGroupProgress').show();
  	$('#frmJoinGroup').hide();
  	$('#submitJoinGroup').button('loading');

			$http({method: 'POST', url: apiEndPoint+'/group/join/'+groupSharer, withCredentials: true}).success(
										function(data, status, headers, config){
											
											console.log("joingroup success");
											if(json.error){
												alert(json.data[0]);
											}
												$('#submitJoinGroup').button('reset');
												$('#joinGroupModal').modal('hide');
						  					$('#frmJoinGroup').show();  

						  					$scope.flags.isJoinGroupModal = false;
												$scope.getUserInfo();
										}
							).error(
									function(data, status, headers, config){
											alert("joingroup fail");
									}
							);

	};

  /*
	*	Methods to handle events & data related to groups
	*/

	$scope.selectGroup = function(evt, group){

		// save the selected group in the factory - shared data
		$scope.currentGroup = group;
		// console.log('selected - '+group._id);

		// change css class for selected group
		$('.group-item').removeClass('active');
		$(evt.currentTarget).parent().addClass('active');

		// fire groupSelected event, which triggers getData() in postCtr
 		$scope.$emit('groupSelected');
		
	};

	$scope.onShareGroup = function(evt, group){
		
		$scope.flags.isShareGroupModal = true;

		$scope.sharedGroup = {};
		$scope.sharedGroup.hash = group.hash;
		$scope.sharedGroup.name = group.name;

	}

	$scope.onRemoveGroup = function(evt, group){
		$scope.flags.isRemoveModal = true;
		
		$scope.remove.type = $scope.GROUP;
		$scope.remove.data = group;
		$scope.remove.desc = group.name;
	};

	$scope.onRemovePost = function(evt, post){
		$scope.flags.isRemoveModal = true;
		
		$scope.remove.type = $scope.POST;
		$scope.remove.data = post;
		$scope.remove.desc = post.title;
	};

	$scope.logout = function(){
						$http({method: 'POST', url: apiEndPoint+'/logout', withCredentials: true}).success(
										function(data, status, headers, config){
											console.log("logout success");
										}
							).error(
									function(data, status, headers, config){
											alert("logout fail");
									}
							);
	};

	$scope.getUserInfo = function(){
					
						$http({method: 'GET', url : apiEndPoint+"/user/info", withCredentials: true}).success(
                    function(data, status, headers, config){
                      
                      $scope.groups = data.data[0].groups;
						        	$scope.uname = data.data[0].name;
						        	
						        	if($scope.groups.length > 0){
						        		// fire groupSelected event, which triggers getData() in postCtr
						        		setTimeout(function() {
						        			$scope.$emit('groupsLoaded');	
						        		}, 50);
 												
						        	}

                    }).error(
	                    function(data, status, headers, config){
	                      alert("userinfo fail");
                    }
      			);
	};

	$scope.onRemoveItem = function(){

		$('#removeItem').button('loading');
		$('#removeItemProgress').show();
		
		if($scope.remove.type == $scope.GROUP){
			$scope.removeGroup();
		} else{
			$scope.removePost();
		}
	};

	$scope.removeGroup = function(){
			var groupId = $scope.remove.data._id;
				
			$http({method: 'delete', url: apiEndPoint+'/group/'+groupId, withCredentials: true}).success(
										function(data, status, headers, config){
											
											console.log("group remove success");
											$('#removeItem').button('reset');
											$('#removeItemProgress').hide();
											$scope.flags.isRemoveModal = false;
											$('#removeModal').modal('hide');

											$scope.getUserInfo();
										}
			).error(
										function(data, status, headers, config){
											alert("remove fail");
										}
			);
	};

	$scope.removePost = function(){
			var postId = $scope.remove.data._id;
				
			$http({method: 'delete', url: apiEndPoint+'/post/'+postId, withCredentials: true}).success(
										function(data, status, headers, config){
											
											console.log("post remove success");
											$('#removeItem').button('reset');
											$('#removeItemProgress').hide();
											$scope.flags.isRemoveModal = false;
											$('#removeModal').modal('hide');

											$scope.getData();
										}
			).error(
										function(data, status, headers, config){
											alert("remove fail");
										}
			);
	};	


	// util method to check if a tag (string starts with a blank space)
	$scope.doesStartWithSpace = function(tag){
		if(tag[0] === " "){
			return true;
		} else{
			return false;
		}
	};

	// explicitly load group data on page load
	$scope.getUserInfo();

}
