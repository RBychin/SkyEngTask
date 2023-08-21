from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

from core.helpers import create_log_file, delete_file
from core.models import File
from web.forms import FileUploadForm

User = get_user_model()


class FileUpload(LoginRequiredMixin, CreateView):
    """Upload file view."""

    model = File
    form_class = FileUploadForm
    template_name = 'web/upload_file.html'
    success_url = reverse_lazy('web:main')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.name = obj.file.name
        obj.save()
        create_log_file(obj, f'file {obj.name} uploaded')
        return super().form_valid(form)


class FileUpdate(LoginRequiredMixin, UpdateView):
    """..."""

    model = File
    form_class = FileUploadForm
    template_name = 'web/upload_file.html'
    success_url = reverse_lazy('web:main')

    def form_valid(self, form):
        file = self.get_object()
        if self.request.user == file.user:
            delete_file(file)
            obj = form.save(commit=False)
            obj.name = obj.file.name
            obj.check_status = 'Waiting'
            obj.pep = None
            obj.is_new = True
            obj.email_notification = False
            obj.save()
            create_log_file(file, f'file {obj.name} updated')
        return super().form_valid(form)


class FilesIndex(LoginRequiredMixin, ListView):
    """The Main page view with all files."""

    template_name = 'web/main.html'
    queryset = File.objects.all()


class ProfileIndex(LoginRequiredMixin, ListView):
    """Profile page view with only user files."""

    template_name = 'web/profile.html'

    def get_queryset(self):
        return self.request.user.files.all()


class PyFileDetailView(DetailView):
    """Detail view file page with errors and logs."""

    model = File
    template_name = 'web/view_py_file.html'
    context_object_name = 'file'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        file = get_object_or_404(
            File, pk=kwargs.get('object').pk
        )
        context['form'] = FileUploadForm(
            self.request.POST or None,
            files=self.request.FILES or None,
            instance=file
        )
        with open(self.object.file.path, 'r') as py_file:
            file_content = py_file.read()
            lexer = PythonLexer()
            formatter = HtmlFormatter(style='vs', noclasses=True)
            highlighted_code = highlight(file_content, lexer, formatter)
            context['highlighted_code'] = highlighted_code
        return context




class FileDelete(View):
    """Delete file foo."""

    def get(self, request, pk):
        file = get_object_or_404(File, id=pk)
        if file.user == request.user:
            file.delete()
            delete_file(file)
        return redirect('web:main')

