from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_name>", views.entry, name="title"),
    path("searchresults", views.searchresults, name="search_results"),
    path("newpage", views.newpage, name="create_new_page"),
    path("editpage/<str:entry_name>", views.editpage, name="edit_existing_page")
]
