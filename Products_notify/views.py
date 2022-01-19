from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Products, User
import datetime
from django.core.mail import send_mail
# Create your views here.


def mail_send(request):
    prod_lst = []
    x = datetime.datetime.now()
    day = x.strftime("%d")
    month = x.strftime("%m")
    year = x.strftime("%Y")
    cur_date = datetime.date(int(year), int(month), int(day))
    get_data = Products.objects.all()
    if get_data:
        for i in get_data:
            difference = (i.edate-cur_date).days
            if difference <= 30 and difference > 0:
                prod_lst.append(f"{i.name} : {difference} days")
        if prod_lst:
            htmlgen = f"<b> Your purchased products will expire as : </b> <br>"
            for i in prod_lst:
                htmlgen += f"<list> {i}</list> <br>"
            send_mail('Products Expiry Alert', "", 'ajaynotify@gmail.com',
                      ["sandeepbisht045@gmail.com.com"], fail_silently=False, html_message=htmlgen)

            # # print(i.sdate-timedelta(days=30))
            return HttpResponse("success")
        else:
            return HttpResponse("")
    else:
        return HttpResponse("Products are not available")


def index(request):
    return render(request, "index.html", {"get_data": Products.objects.all()})


def login(request):
    if not request.session.get("id"):
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")

            filter_data = User.objects.filter(email=email, password=password)
            if filter_data.exists():
                for i in filter_data:
                    request.session["id"] = i.id

                return redirect("/")
            else:
                return render(request, "login.html", {"alert": "Invalid email or password"})

    return render(request, "login.html")


def logout(request):
    if request.session.get("id"):
        request.session.clear()
        return redirect("/")


def add_products(request):
    if request.method == "POST":
        if request.session.get("id"):
            product = request.POST.get("product")
            vendor_name = request.POST.get("vendor_name")
            vendor_email = request.POST.get("vendor_email")
            license_date = request.POST.get("license_date")
            expiry_date = request.POST.get("expiry_date")
            license_lst = license_date.split("-")
            expiry_lst = expiry_date.split("-")
            sdate = datetime.date(int(license_lst[0]), int(
                license_lst[1]), int(license_lst[2]))
            edate = datetime.date(int(expiry_lst[0]), int(
                expiry_lst[1]), int(expiry_lst[2]))
            if (edate-sdate).days >= 0:
                Products.objects.create(name=product, sdate=sdate, edate=edate,
                                        vendor_name=vendor_name, vendor_email=vendor_email).save()
                return render(request, "index.html", {"msg": "Product has been added successfully", "get_data": Products.objects.all()})
            else:
                return render(request, "add_products.html", {"alert": "Product purchased date cannot be greater than expiry date", "product": product, "vendor_name": vendor_name, "vendor_email": vendor_email})
        else:
            return render(request, "login.html", {"alert": "Login first to add products"})
    return render(request, "add_products.html")


def delete(request, id):
    if request.session.get("id"):
        if request.method == "POST":
            data = Products.objects.get(id=id)
            if data:
                data.delete()
            return redirect("/")
        else:
            return redirect("/")

    else:
        return render(request, "login.html", {"alert": "Login first to delete"})
