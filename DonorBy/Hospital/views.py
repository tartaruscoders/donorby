from django.shortcuts import render, redirect, get_object_or_404
from .models import Measurement
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import get_geo
from django.contrib.auth.models import User
from django.contrib import auth
import folium
from .utils import get_center_coordinates, get_zoom
from ipware import get_client_ip


def HospitalLogin(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            print('login sucessfully')
            return redirect('MapDistanceCalculate')
        else: 
            print('invalid credentials')
            return redirect('HospitalLogin')
    else: 
        return render(request, 'Hospital/login.html')

def HospitalRegister(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                print('username exist')
                return redirect('HospitalRegister')
            else:
                if User.objects.filter(email=email).exists():
                    print('email exist')
                    return redirect('HospitalRegister')


                else:
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.save()
                    return redirect('HospitalLogin') 
        else:
            print('Password didnt match')
            return redirect('HospitalRegister')

    else:
        return render(request, 'Hospital/Registration.html')


def MapDistanceCalculate(request):
    
    ip, is_routable = get_client_ip(request)

    if ip is None:
        ip = "0.0.0.0"
    else:
        if is_routable:
            ipv = "Public"
        else:
            ipv = "Private"


    # initial values
    distance = None
    donorLocation = None
    
    # obj = get_object_or_404(Measurement, id=3)
    # obj = Measurement.objects.get(id = 3)
    # print(obj)

    form = MeasurementModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='measurements')

    country, city, lat, lon = get_geo(ip)

    location = geolocator.geocode(city)

    # location coordinates
    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)


    # initial folium map
    m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon), zoom_start=8)


    # location marker
    folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'],
    icon=folium.Icon(color='purple')).add_to(m)

    if form.is_valid():
        instance = form.save(commit=False)
        donorLocation_ = form.cleaned_data.get('donorLocation')
        
        donor = geolocator.geocode(donorLocation_)

        # donor coordinates
        d_lat = donor.latitude
        d_lon = donor.longitude
        pointB = (d_lat, d_lon)

        # distance calculation
        # answer will be in km and round to 2 decimal places
        distance = round(geodesic(pointA, pointB).km, 2)

        
        # folium map modification
        m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon, d_lat, d_lon), zoom_start=get_zoom(distance))
        # location marker
        folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'],
                    icon=folium.Icon(color='purple')).add_to(m)
        # donorLocation marker
        folium.Marker([d_lat, d_lon], tooltip='click here for more', popup=donorLocation,
                    icon=folium.Icon(color='red', icon='cloud')).add_to(m)
        
        # draw the line between location and donorLocation
        line = folium.PolyLine(locations=[pointA, pointB], weight=5, color='blue')
        m.add_child(line)

        instance.location = location
        instance.distance = distance
        instance.save()
    
    # object is returning 
    #  <folium.folium.Map object at 0x000001393AD2CE20>
    #therefore changing it to html representation
    m = m._repr_html_()
        
    context = {
        'distance' : distance,
        'donorLocation': donorLocation,
        'form': form,
        'map': m,
    }

    return render(request,'Hospital/Map.html',context)


def HospitalMain(request):
    return render(request,'Hospital/HospitalMain.html')