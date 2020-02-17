from django.shortcuts import render

from django.http import HttpResponse

from rango.models import Category

from rango.models import Page

from rango.forms import CategoryForm

from rango.forms import PageForm

from django.shortcuts import redirect

from django.urls import reverse

from rango.forms import UserForm, UserProfileForm

def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    response = render(request, 'rango/index.html', context=context_dict)
    
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return render(request,'rango/about.html')

def show_category(request, category_name_slug):

    context_dict = {}
    try:

        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages

        context_dict['category'] = category
        
    except Category.DoesNotExist:


        context_dict['category'] = None
        context_dict['pages'] = None
        
    return render(request, 'rango/category.html', context=context_dict)

def add_category(request):
    form = CategoryForm()
# A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
# Have we been provided with a valid form?
        if form.is_valid():
# Save the new category to the database.
            cat = form.save(commit=True)
# Now that the category is saved, we could confirm this.
# For now, just redirect the user back to the index view.
            print(cat, cat.slug)
            return redirect('/rango/')
        else:
# The supplied form contained errors -
# just print them to the terminal.
            print(form.errors)
# Will handle the bad form, new form, or no form supplied cases.
# Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
# You cannot add a page to a Category that does not exist...
    if category is None:
        return redirect('/rango/')
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category',kwargs={'category_name_slug':category_name_slug}))
    else:
        print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):

    registered = False

    if request.method == 'POST':

        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user= user_form.save()

            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

 # Did the user provide a profile picture?
 # If so, we need to get it from the input form and
 #put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

 # Now we save the UserProfile model instance.
            profile.save()

 # Update our variable to indicate that the template
 # registration was successful.
            registered = True
        else:
# Invalid form or forms - mistakes or something else?
# Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
# Not a HTTP POST, so we render our form using two ModelForm instances.
# These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

# Render the template depending on the context.
    return render(request,'rango/register.html',context = {'user_form': user_form,'profile_form': profile_form,'registered': registered})
            
            

