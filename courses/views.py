from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import SomeModel
from .services import process_new_object


@login_required
def create_somemodel(request):
    if request.method == "POST":
        obj = SomeModel.objects.create(
            user=request.user,
            condition_field=True  # можно заменить на значение из формы
        )
        process_new_object(obj)
        return redirect("home")

    return render(request, "create.html")
