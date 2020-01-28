from django.shortcuts import render
from django.http import JsonResponse
from .forms import ContactForm
from django.views.generic import TemplateView, FormView
import os
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from backends.table.search import TableSearch


# Create your views here.
class MainPage(TemplateView):

    template_name = 'main/home/home.html'


# view for the research page
class ResearchPage(TemplateView):

    template_name = 'main/research/research.html'


# view for the research page
class IndustryPage(TemplateView):

    template_name = 'main/industry/industry.html'


# view for the research page
class DisplayPage(TemplateView):

    template_name = 'main/projects/projects.html'


# view for the research page
class PublicationsPage(TemplateView):

    template_name = 'main/publications/pub.html'

    def get_context_data(self, **kwargs):
        # get the context data
        context = super(PublicationsPage, self).get_context_data(*kwargs)

        # create a TableSearch and get the table context data
        table = TableSearch(name='talks', csv_path='publications/ConnorPublications-talks.csv', bold=['C. McClellan', 'C.J. McClellan'])
        table_2 = TableSearch(name='journals', csv_path='publications/ConnorPublications-journals.csv', bold=['C. McClellan', 'C.J. McClellan'])
        # add the table context
        context = table.add_context_data(context=context)
        context = table_2.add_context_data(context=context)
        return context


# view for the research page
class HobbiesPage(TemplateView):

    template_name = 'main/hobbies/hobbies.html'


# view for contacting me
class ContactMe(FormView):

    template_name = 'main/contact_me/contact_me.html'
    form_class = ContactForm

    def get_context_data(self, **kwargs):
        context = super(ContactMe, self).get_context_data(**kwargs)
        try:
            context['contact_success'] = self.kwargs['contact_success']
        except:
            context['contact_success'] = False
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        # make sure the form is valid.  Otherwise, send back to user
        if form.is_valid():
            try:
                subject = form.cleaned_data['subject'] + ' from ' + form.cleaned_data['email'] + ' to Fiona'
                send_mail(subject, form.cleaned_data['message'],
                          settings.EMAIL_HOST_USER,
                          [settings.EMAIL_CONTACT], fail_silently=False)

            except BadHeaderError:
                pass

            self.kwargs['contact_success'] = True
            return self.get(request=request)

        else:
            return render(request, template_name=self.template_name, context={'form': form})


# prepare variables for the image carousel using ajax
def ajax_carousel_images(request):
    path = request.GET['path']

    assert path[0] == '/', '{0} is not an absolute path'.format(path)
    a = path[1:7]
    assert path[1:7] == 'static', '{0} does not point to static directory'.format(path)

    # Get the images.  Don't include the leading '/'
    images = os.listdir(os.path.join(settings.BASE_DIR, path[1:]))

    data = {'paths': [], 'names': []}

    # now get the names and paths of the images
    for image in images:
        data['paths'].append(os.path.join(path, image))
        data['names'].append(image.split('.')[0])

    return JsonResponse(data=data)
