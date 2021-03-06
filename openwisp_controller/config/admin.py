import json

from django import forms
from django.contrib import admin
from django.urls import reverse
from django_netjsonconfig import settings as django_netjsonconfig_settings
from django_netjsonconfig.base.admin import (AbstractConfigForm, AbstractConfigInline, AbstractDeviceAdmin,
                                             AbstractTemplateAdmin, AbstractVpnAdmin, AbstractVpnForm,
                                             BaseForm)

from openwisp_users.models import Organization
from openwisp_users.multitenancy import MultitenantOrgFilter, MultitenantRelatedOrgFilter
from openwisp_utils.admin import AlwaysHasChangedMixin
from django.utils.translation import gettext_lazy as _

from ..admin import MultitenantAdminMixin
from .models import Config, Device, OrganizationConfigSettings, Template, Vpn, Subscribe, Unsubscribe


class ConfigForm(AlwaysHasChangedMixin, AbstractConfigForm):
    class Meta(AbstractConfigForm.Meta):
        model = Config

    def get_temp_model_instance(self, **options):
        config_model = self.Meta.model
        instance = config_model(**options)
        device_model = config_model.device.field.related_model
        org = Organization.objects.get(pk=self.data['organization'])
        instance.device = device_model(
            name=self.data['name'],
            mac_address=self.data['mac_address'],
            organization=org
        )
        return instance


class ConfigInline(MultitenantAdminMixin, AbstractConfigInline):
    model = Config
    form = ConfigForm
    extra = 0
    multitenant_shared_relations = ('templates',)


class DeviceAdmin(MultitenantAdminMixin, AbstractDeviceAdmin):
    inlines = [ConfigInline]
    list_filter = [('organization', MultitenantOrgFilter),
                   ('config__templates', MultitenantRelatedOrgFilter),
                   'config__status',
                   'created']
    if django_netjsonconfig_settings.BACKEND_DEVICE_LIST:
        list_filter.insert(1, 'config__backend')
    list_select_related = ('config', 'organization')

    def _get_default_template_urls(self):
        """
        returns URLs to get default templates
        used in change_form.html template
        """
        organizations = Organization.active.all()
        urls = {}
        for org in organizations:
            urls[str(org.pk)] = reverse('config:get_default_templates', args=[org.pk])
        return json.dumps(urls)

    def get_extra_context(self, pk=None):
        ctx = super(DeviceAdmin, self).get_extra_context(pk)
        ctx.update({'default_template_urls': self._get_default_template_urls()})
        return ctx

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = self.get_extra_context()
        return super(DeviceAdmin, self).add_view(request, form_url, extra_context)


DeviceAdmin.list_display.insert(1, 'organization')
DeviceAdmin.fields.insert(1, 'organization')


class TemplateForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = Template


class TemplateAdmin(MultitenantAdminMixin, AbstractTemplateAdmin):
    form = TemplateForm
    multitenant_shared_relations = ('vpn',)

    def subscribe(self, obj):
        if obj:
            count = Subscribe.objects.filter(template=obj.pk).count()
            return count
    subscribe.short_description = _('Subscribed')

    def unsubscribe(self, obj):
        if obj:
            count = Unsubscribe.objects.filter(template=obj.pk).count()
            return count
    unsubscribe.short_description = _('Unsubscribed')

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(TemplateAdmin, self).get_readonly_fields(request, obj)
        return readonly_fields + ('subscribe', 'unsubscribe')

    def get_fields(self, request, obj=None):
        fields = super(TemplateAdmin, self).get_fields(request, obj)
        if obj and obj.flag=='import':
            fields = tuple(fields)
            return fields + ('subscribe', 'unsubscribe')
        return fields

    def add_view(self, request, form_url='', extra_context=None):
        if request.POST:
            if request.POST.get('flag') == 'public' or \
                    request.POST.get('flag') == 'shared_secret':
                domain = request.META['HTTP_HOST']
                request.POST = request.POST.copy()
                request.POST['url'] = domain
        return super(TemplateAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.POST:
            if request.POST.get('flag') == 'public' or \
                    request.POST.get('flag') == 'shared_secret':
                domain = request.META['HTTP_HOST']
                request.POST = request.POST.copy()
                request.POST['url'] = domain
        return super(TemplateAdmin, self).change_view(request, object_id, form_url, extra_context)


TemplateAdmin.list_display.insert(1, 'organization')
TemplateAdmin.list_display.insert(5, 'url')
TemplateAdmin.list_filter.insert(0, ('organization', MultitenantOrgFilter))
# TemplateAdmin.fields.insert(0, 'subscribe')
# TemplateAdmin.fields.insert(1, 'unsubscribe')
TemplateAdmin.fields.insert(1, 'organization')
TemplateAdmin.fields.insert(3, 'url')


class VpnForm(AbstractVpnForm):
    class Meta(AbstractVpnForm.Meta):
        model = Vpn


class VpnAdmin(MultitenantAdminMixin, AbstractVpnAdmin):
    form = VpnForm
    multitenant_shared_relations = ('ca', 'cert')


VpnAdmin.list_display.insert(1, 'organization')
VpnAdmin.list_filter.insert(0, ('organization', MultitenantOrgFilter))
VpnAdmin.list_filter.remove('ca')
VpnAdmin.fields.insert(2, 'organization')

admin.site.register(Device, DeviceAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(Vpn, VpnAdmin)


if getattr(django_netjsonconfig_settings, 'REGISTRATION_ENABLED', True):
    from openwisp_users.admin import OrganizationAdmin

    class ConfigSettingsForm(AlwaysHasChangedMixin, forms.ModelForm):
        pass

    class ConfigSettingsInline(admin.StackedInline):
        model = OrganizationConfigSettings
        form = ConfigSettingsForm

    OrganizationAdmin.save_on_top = True
    OrganizationAdmin.inlines.insert(0, ConfigSettingsInline)
