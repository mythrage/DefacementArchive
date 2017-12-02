from django.db import models
from django.contrib.flatpages.models import FlatPage

class Defacer(models.Model):
   defacer_name = models.CharField(maxlength=50, unique=True)
   defacer_text = models.TextField()
   class Admin:
      list_display = ("defacer_name", "defacer_text")
      search_fields = ['defacer_name']
   class Meta:
      ordering = ('defacer_name',)
   def __str__(self):
      return self.defacer_name

class System(models.Model):
   system_name = models.CharField(maxlength=20)
   class Admin:
      list_display = ("system_name",)
   def __str__(self):
      return self.system_name

class Webserver(models.Model):
   webserver_name = models.CharField(maxlength=20)
   class Admin:
      list_display = ("webserver_name",)
   def __str__(self):
      return self.webserver_name

class IpAddress(models.Model):
   ip_number = models.IPAddressField(unique=True)
   whois_as = models.CharField(maxlength=50)
   whois_as_name = models.CharField(maxlength=150)
   whois_date = models.DateField(auto_now=True)
   class Admin:
      list_display = ("ip_number", "whois_as", "whois_as_name", "whois_date")
      search_fields = ['ip_number']
   class Meta:
      ordering = ('ip_number',)
   def __str__(self):
      return self.ip_number

class Mirror(models.Model):
   mirror_date = models.DateField()
   mirror_link = models.CharField(maxlength=200, unique=True)
   mirror_page = models.ForeignKey(FlatPage)
   class Admin:
      list_display = ("mirror_date", "mirror_link", "mirror_page")
      search_fields = ['mirror_link']
   class Meta:
      ordering = ('mirror_link',)
   def __str__(self):
      return self.mirror_link

class Website(models.Model):
   date_defaced = models.DateField()
   ticket = models.CharField(maxlength=50)
   system_type = models.ForeignKey(System)
   defacer_name = models.ForeignKey(Defacer)
   ip_address = models.ForeignKey(IpAddress)
   web_server = models.ForeignKey(Webserver)
   mirror = models.ForeignKey(Mirror)
   class Admin:
      list_display = ("date_defaced", "ticket", "mirror", "defacer_name", "system_type","ip_address", "web_server")
      search_fields = ['mirror__mirror_link']
   def __str__(self):
      return str(self.ip_address)  

class Domain(models.Model):
   domain_name = models.CharField(maxlength=50, core=True)
   link_address = models.CharField(maxlength=100, core=True)
   domain = models.ForeignKey(Website, edit_inline=models.TABULAR, num_in_admin=3,num_extra_on_change=5)
   class Admin:
      list_display = ("domain_name", "link_address", "domain")
      search_fields = ['domain_name']
   def __str__(self):
      return self.domain_name

