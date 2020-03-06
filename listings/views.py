from django.shortcuts import render,get_object_or_404
from .models import Listing
from listings.choices import state_choices, bedroom_choices, price_choices
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.


def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 3)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context={
        'listings':paged_listings,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
    }
    return render(request,'listings/listings.html',context)

def listing(request,listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    other_images=[]
    for n in range(1, 7):
        try:
            other_images.append(getattr(listing, f'photo_{n}').url)
        except ValueError:
            continue
    
    context = {
        'listing': listing,
        'other_images': other_images
    }
    return render(request, 'listings/listing.html', context=context)

def search(request):
    queryset_list=Listing.objects.order_by('-list_date')
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    context={
        
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings':queryset_list,
        'values':request.GET,
    }
    return render(request,'listings/search.html',context)