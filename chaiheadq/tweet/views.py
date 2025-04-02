from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.

# def index(request):
#     return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    print("tweeijt ",tweets)
    return render(request, 'tweet_list.html', {'tweets': tweets})

@login_required
def tweet_create(request):
    if request.method == "POST":  # If the request method is POST (form submission)
        form = TweetForm(request.POST, request.FILES)  
        if form.is_valid():  # Validate the form
            tweet = form.save(commit=False)  # Create a Tweet instance but don't save it yet
            tweet.user = request.user  # Assign the logged-in user to the tweet
            tweet.save()  # Now save the tweet in the database
            return redirect('tweet_list')  # Redirect to the tweet list page
    else:
        form = TweetForm()  # If not a POST request, initialize an empty form
        
    return render(request, 'tweet_form.html', {'form': form})  #  Render the tweet form page

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)  #  Ensures the tweet exists and belongs to the logged-in user

    if request.method == 'POST':  # If form is submitted
        form = TweetForm(request.POST, request.FILES, instance=tweet)  
        if form.is_valid():  #  Validate the form
            tweet = form.save(commit=False)  #  Update the existing tweet
            tweet.user = request.user  # (This may not be necessary since the user is unchanged)
            tweet.save()  #  Save the updated tweet
            return redirect('tweet_list')  #  Redirect to the tweet list after saving
    else:
        form = TweetForm(instance=tweet)  #  Pre-fill the form with existing tweet data

    return render(request, 'tweet_form.html', {'form': form})  # Render the form with existing data for editing

@login_required   
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == 'POST':  
        tweet.delete()  
        return redirect('tweet_list')  #  Redirects and exits the function

    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})  #  This only runs if the method is NOT POST (i.e., when confirming deletion)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})
