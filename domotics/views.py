from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views import generic
# Create your views here.

from django.http import HttpResponse
from django.template import loader
from .models import Switch, Sensor, Clock, Rule
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

def index(request):
    template = loader.get_template('domotics/index.html')
    context = {
        'switches': Switch.objects.all(),
        'sensors': Sensor.objects.all(),
        'clocks': Clock.objects.all(),
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def switch(request, switch_id):
    if request.method == 'POST':
        switch = Switch.objects.get(pk=switch_id)
        if switch.state:
            switch.state = False
        else:
            switch.state = True
        switch.save()
        return HttpResponse("OK")
    else:
        switch = Switch.objects.get(pk=switch_id)
        return HttpResponse(switch.state)

@csrf_exempt
def sensor(request, sensor_id):
    if request.method == 'POST':
        sensor = Sensor.objects.get(pk=sensor_id)
        sensor.value = request.POST['value']
        sensor.save()
        return HttpResponse("OK")
    else:
        sensor = Sensor.objects.get(pk=sensor_id)
        return HttpResponse(sensor.value)

@csrf_exempt
def clock(request, clock_id):
    if request.method == 'POST':
        clock = Clock.objects.get(pk=clock_id)
        clock.time = request.POST['time']
        clock.save()
        return HttpResponse("OK")
    else:
        clock = Clock.objects.get(pk=clock_id)
        return HttpResponse(clock.time)

class RulesView(TemplateView):
    template_name = 'rules.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rules'] = Rule.objects.all()
        return context

class RuleListView(TemplateView):
    template_name = 'rule-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rules'] = Rule.objects.all()
        return context

class CreateRuleView(CreateView):
    model = Rule
    template_name = 'rule-form.html'
    success_url = reverse_lazy('rules')
    fields = '__all__'

class DeleteRuleView(generic.DeleteView):
    model = Rule
    template_name = 'rule-remove.html'
    success_url = reverse_lazy('rules')

class UpdateRuleView(generic.UpdateView):
    model = Rule
    template_name = 'rule-form.html'
    success_url = reverse_lazy('rules')
    fields = '__all__'