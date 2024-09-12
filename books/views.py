from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Book,Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class BooksListView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/book_list.html'

class BooksDetailView(DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'books/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()  # Get all reviews for this book
        if self.request.user.is_authenticated:
            context['form'] = ReviewForm()  # Only add the form if user is logged in
        return context

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        if request.method == 'POST' and request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.book = book
                review.author = request.user
                review.save()
                return redirect('book_detail', pk=book.pk)
        return render(request, self.template_name, self.get_context_data())
