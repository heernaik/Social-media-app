from django.shortcuts import redirect

def check_user(function):
	def wrapper(request, *args, **kwargs):
		user = request.user 
		if not user.is_authenticated:
			return redirect('login')
		elif user.is_authenticated:
			return function(request, *args, **kwargs)

		return function(request, *args, **kwargs)
	return wrapper		

def login_user(function):
	def wrapper(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('showlist')
		else:
			return function(request, *args, **kwargs)
	return wrapper