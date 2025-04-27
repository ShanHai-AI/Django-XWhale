from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from .models import Agent
# Create your views here.


def status(request):
    agents = Agent.objects.all().order_by('agentID')
    status_list = {
        "1":'standby',
        "2":'working',
        "3": 'completed',
        "4": 'charging',
    }
    data = [
        {'id': agent.id, 'name':agent.name,'state': status_list[str(agent.status)]}
        for agent in agents
    ]
    return JsonResponse(data, safe=False)
    # return HttpResponse("Agent is running")
