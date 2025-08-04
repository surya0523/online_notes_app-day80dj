# notes/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Note
from django.contrib import messages

# Ensure you have Django 3.x+ for generic views, or import FormMixin
# from django.views.generic.edit import FormMixin # If needed for older Django versions

class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        # Only show notes belonging to the logged-in user
        return Note.objects.filter(user=self.request.user).order_by('-updated_at')

class NoteDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Note
    template_name = 'notes/note_detail.html'
    context_object_name = 'note'

    def test_func(self):
        # Only allow access to notes owned by the current user
        note = self.get_object()
        return note.user == self.request.user

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    template_name = 'notes/note_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('notes:note_list')

    def form_valid(self, form):
        # Automatically set the note's user to the logged-in user
        form.instance.user = self.request.user
        messages.success(self.request, "Note created successfully!")
        return super().form_valid(form)

class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    template_name = 'notes/note_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('notes:note_list')

    def test_func(self):
        # Only allow user to update their own notes
        note = self.get_object()
        return note.user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Note updated successfully!")
        return super().form_valid(form)

class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('notes:note_list')
    context_object_name = 'note'

    def test_func(self):
        # Only allow user to delete their own notes
        note = self.get_object()
        return note.user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Note deleted successfully!")
        return super().form_valid(form)