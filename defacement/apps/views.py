
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context
from defacement.apps import models
import commands, string

def index(request):
   return HttpResponseRedirect("/1/")

def website(request,page):
   page = int(page)
   if page < 1:
      page = 1
   domain_list = models.Domain.objects.select_related().order_by('-apps_website.date_defaced')[(page* 15)-15:page * 15]
   number = models.Domain.objects.count()
   number = (number / 15) + 2
   t = get_template('website.html')
   if page > 1:
      previous = page - 1
   else:
      previous = page
   if page < number - 1:
      next = page + 1
   else:
      next = page
   output = []
   for i in range(1,number):
      if i==page:
         output.append("<b><a href=\"../../%s\">%s</a></b>" %(i, i))
      else:
         output.append("<a href=\"../../%s\">%s</a>" %(i, i))
   c = Context({'domain_list': domain_list, 'previous': previous, 'next': next, 'output': output})
   return HttpResponse(t.render(c))

def defacer(request):
   object_list = models.Defacer.objects.all()
   for i in object_list:
      i.count = models.Website.objects.filter(defacer_name=i.id).count()
   t = get_template('defacer.html')
   c = Context({'object_list': object_list})
   return HttpResponse(t.render(c))

def defacer_filter(request, offset):
   domain_list = models.Domain.objects.select_related().filter(domain__defacer_name=offset)
   domain_count = domain_list.count()
   name = models.Defacer.objects.filter(id=offset)
   website_list = models.Website.objects.select_related().filter(defacer_name=offset)
   website_count = website_list.count()
   t = get_template('defacer_filter.html')
   c = Context({'domain_list': domain_list, 'website_list': website_list, 'domain_count': domain_count, 'website_count': website_count, 'name':name})
   return HttpResponse(t.render(c))  

def whois(request,ip):
   command = 'whois -h whois.cymru.com " -f %s"|awk -F"|" \'{print "<p>AS: " $1 "</p><p>IP Address: " $2 "</p><p>AS Name: " $3"</p>"}\'' %(ip)
   output = commands.getoutput(command)
   t = get_template('whois.html')
   available = models.IpAddress.objects.filter(ip_number = ip)
   c = Context({'output': output, 'available' : available})
   return HttpResponse(t.render(c))

def whois_all(request):
   object_list = models.IpAddress.objects.order_by('ip_number')
   t = get_template('whois_all.html')
   c = Context({'object_list': object_list}) 
   return HttpResponse(t.render(c))

def filter(request,type,offset):
   if type == "whois_filter":
      domain_list = models.Domain.objects.select_related().filter(domain__ip_address__whois_as=offset)
      whois = offset
      provider = domain_list[0].domain.ip_address.whois_as_name
      domain_number = domain_list.count()
      website_number = models.Website.objects.select_related().filter(ip_address__whois_as=offset).count()
      t = get_template('whois_filter.html')
      c = Context({'domain_list': domain_list, 'whois': whois, 'provider': provider, 'domain_number': domain_number, 'website_number': website_number})
      return HttpResponse(t.render(c))
   if type == "system":
      domain_list = models.Domain.objects.select_related().filter(domain__system_type__id=offset)
      system_name = domain_list[0].domain.system_type
      domain_number = domain_list.count()
      website_number = models.Website.objects.select_related().filter(system_type__id=offset).count()
      t = get_template('system_filter.html')
      c = Context({'domain_list': domain_list, 'system_name': system_name, 'domain_number': domain_number, 'website_number': website_number})
      return HttpResponse(t.render(c))
   if type == "webserver":
      domain_list = models.Domain.objects.select_related().filter(domain__web_server__id=offset)
      webserver_name = domain_list[0].domain.web_server
      domain_number = domain_list.count()
      website_number = models.Website.objects.select_related().filter(web_server__id=offset).count()
      t = get_template('webserver_filter.html')
      c = Context({'domain_list': domain_list, 'webserver_name': webserver_name, 'domain_number': domain_number, 'website_number': website_number})
      return HttpResponse(t.render(c))
   else:
      return HttpResponse("created by mythrage")

def search(request):
   search = ""
   prompt = ""
   output_list = []
   if request.method == 'POST':
      prompt = "Please enter query text and select category"
      search = request.POST.copy()
      if search:
         if search['text']:
            prompt = "Please select category"
         if search['category']=='defacer':
            if search['text']!= "":
               output_list = models.Domain.objects.filter(domain__defacer_name__defacer_name__icontains=search['text'])
               prompt = ""
               if output_list.count() == 0:
                  prompt = "Information not found"
         if search['category']=='domain':
            if search['text']!= "":
               output_list = models.Domain.objects.filter(domain_name__icontains=search['text'])
               prompt = ""
               if output_list.count() == 0:
                  prompt = "Information not found"
         if search['category']=='ipaddress':
            if search['text']!= "":
               output_list = models.Domain.objects.filter(domain__ip_address__ip_number__contains=search['text'])
               prompt = ""
               if output_list.count() == 0:
                  prompt = "No Information found"
   t = get_template('search.html')
   c = Context({'output_list': output_list, 'prompt': prompt, 'search': search})
   return HttpResponse(t.render(c))

def date_detail(request,offset):
   object_list = models.Domain.objects.filter(domain__date_defaced=offset)
   ip_list = models.Website.objects.filter(date_defaced=offset)
   unique = ip_list.count()
   domain = object_list.count()
   case = ip_list.count()
   t = get_template('date.html')
   c = Context({'object_list': object_list, 'case': case, 'offset': offset, 'ip_list': ip_list , 'unique': unique, 'domain': domain})
   return HttpResponse(t.render(c))

def detail(request):
   system_type = models.System.objects.all()
   for i in system_type:
      i.count = models.Website.objects.select_related().filter(system_type=i).count()
   webserver_type = models.Webserver.objects.all()
   for i in webserver_type:
      i.count = models.Website.objects.select_related().filter(web_server=i).count()
   provider = models.IpAddress.objects.order_by('whois_as')
   for i in provider:
      i.count = models.Website.objects.select_related().filter(ip_address__whois_as=i.whois_as).count()
   t = get_template('detail.html')
   c = Context({'system_type':system_type, 'webserver_type': webserver_type, 'provider': provider})
   return HttpResponse(t.render(c))
