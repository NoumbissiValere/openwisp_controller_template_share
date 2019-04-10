import uuid
import collections

from jsonfield import JSONField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_netjsonconfig import settings as app_settings
from django_netjsonconfig.base.config import AbstractConfig, TemplatesThrough
from django_netjsonconfig.base.config import TemplatesVpnMixin as BaseMixin
from django_netjsonconfig.base.device import AbstractDevice
from django_netjsonconfig.base.tag import AbstractTaggedTemplate, AbstractTemplateTag
from django_netjsonconfig.base.template import AbstractTemplate
from django_netjsonconfig.base.vpn import AbstractVpn, AbstractVpnClient
from django_netjsonconfig.utils import get_random_key
from django_netjsonconfig.validators import key_validator, mac_address_validator
from sortedm2m.fields import SortedManyToManyField
from taggit.managers import TaggableManager

from openwisp_users.mixins import OrgMixin, ShareableOrgMixin

from .utils import get_default_templates_queryset


class TemplatesVpnMixin(BaseMixin):
    class Meta:
        abstract = True

    def get_default_templates(self):
        """ see ``openwisp_controller.config.utils.get_default_templates_queryset`` """
        queryset = super(TemplatesVpnMixin, self).get_default_templates()
        assert self.device
        return get_default_templates_queryset(self.device.organization_id,
                                              queryset=queryset)

    @classmethod
    def clean_templates_org(cls, action, instance, pk_set, **kwargs):
        templates = cls.get_templates_from_pk_set(action, pk_set)
        if not templates:
            return templates
        # when using the admin, templates will be a list
        # we need to get the queryset from this list in order to proceed
        if not isinstance(templates, models.QuerySet):
            template_model = cls.templates.rel.model
            pk_list = [template.pk for template in templates]
            templates = template_model.objects.filter(pk__in=pk_list)
        # lookg for invalid templates
        invalids = templates.exclude(organization=instance.device.organization) \
                            .exclude(organization=None) \
                            .values('name')

        if templates and invalids:
            names = ''
            for invalid in invalids:
                names = '{0}, {1}'.format(names, invalid['name'])
            names = names[2:]
            message = _('The following templates are owned by organizations '
                        'which do not match the organization of this '
                        'configuration: {0}').format(names)
            raise ValidationError(message)
        # return valid templates in order to save computation
        # in the following operations
        return templates

    @classmethod
    def clean_templates(cls, action, instance, pk_set, **kwargs):
        """
        adds organization validation
        """
        templates = cls.clean_templates_org(action, instance, pk_set, **kwargs)
        # perform validation of configuration (local config + templates)
        super(TemplatesVpnMixin, cls).clean_templates(action, instance, templates, **kwargs)


# if unique attribute for NETJSONCONFIG_HARDWARE_ID_OPTIONS is not explicitely mentioned,
# consider it to be False
if not getattr(settings, 'NETJSONCONFIG_HARDWARE_ID_OPTIONS', {}).get('unique'):
    app_settings.HARDWARE_ID_OPTIONS.update({'unique': False})


class Device(OrgMixin, AbstractDevice):
    """
    Concrete Device model
    """
    name = models.CharField(max_length=64, unique=False, db_index=True)
    mac_address = models.CharField(
        max_length=17,
        db_index=True,
        unique=False,
        validators=[mac_address_validator],
        help_text=_('primary mac address')
    )

    class Meta(AbstractDevice.Meta):
        unique_together = (
            ('name', 'organization'),
            ('mac_address', 'organization'),
            ('hardware_id', 'organization'),
        )
        abstract = False

    def get_temp_config_instance(self, **options):
        c = super(Device, self).get_temp_config_instance(**options)
        c.device = self
        return c


class Config(TemplatesVpnMixin, AbstractConfig):
    """
    Concrete Config model
    """
    device = models.OneToOneField('config.Device', on_delete=models.CASCADE)
    templates = SortedManyToManyField('config.Template',
                                      related_name='config_relations',
                                      verbose_name=_('templates'),
                                      base_class=TemplatesThrough,
                                      blank=True,
                                      help_text=_('configuration templates, applied from '
                                                  'first to last'))
    vpn = models.ManyToManyField('config.Vpn',
                                 through='config.VpnClient',
                                 related_name='vpn_relations',
                                 blank=True)

    class Meta(AbstractConfig.Meta):
        abstract = False


class TemplateTag(AbstractTemplateTag):
    """
    openwisp-controller TemplateTag model
    """
    class Meta(AbstractTemplateTag.Meta):
        abstract = False


class TaggedTemplate(AbstractTaggedTemplate):
    """
    openwisp-controller TaggedTemplate model
    """
    tag = models.ForeignKey('config.TemplateTag',
                            related_name='%(app_label)s_%(class)s_items',
                            on_delete=models.CASCADE)

    class Meta(AbstractTaggedTemplate.Meta):
        abstract = False


class Template(ShareableOrgMixin, AbstractTemplate):
    """
    openwisp-controller Template model
    """
    tags = TaggableManager(through='config.TaggedTemplate', blank=True,
                           help_text=_('A comma-separated list of template tags, may be used '
                                       'to ease auto configuration with specific settings (eg: '
                                       '4G, mesh, WDS, VPN, ecc.)'))
    vpn = models.ForeignKey('config.Vpn',
                            verbose_name=_('VPN'),
                            blank=True,
                            null=True,
                            on_delete=models.CASCADE)
    url = models.URLField(_('URL'),
                          blank=True,
                          null=True,
                          help_text=_('Enter URL to import template from'))
    description = models.TextField(_('Description'),
                                   blank=True,
                                   null=True,
                                   help_text=_('Enter public description of this template'))
    notes = models.TextField(_('Notes'),
                             blank=True,
                             null=True,
                             help_text=_('Enter internal notes for the administrators'))
    variable = JSONField(_('Variable'),
                         default=dict,
                         blank=True,
                         help_text=_('Enter Values for the variables used by this template'),
                         load_kwargs = {'object_pairs_hook': collections.OrderedDict},
                         dump_kwargs = {'indent': 4})

    class Meta(AbstractTemplate.Meta):
        abstract = False
        unique_together = (('organization', 'name'), )

    def clean(self):
        self._validate_org_relation('vpn')
        if self.flag == 'public' or self.flag == 'shared_secret':
            if self.description is None:
                raise ValidationError(('description'), _('Please enter public description of '
                                                         'shared template'))
            if self.notes is None:
                raise ValidationError('notes', _('Please enter notes used by administrations of '
                                                 'shared template'))
            if self.variable is {}:
                raise ValidationError('variable', _('Please enter sample values for variables '))
            if self.flag == 'public':
                self.url = 'http://{0}/api/templates/{1}'.format(self.url, self.id)
            if self.flag == 'shared_secret':
                self.url = 'http://{0}/api/templates/{1}/?key={2}'.format(self.url, self.id, self.key)

        if self.flag == 'import':
            if self.url is None:
                raise ValidationError('url', _('Please enter the Url to import template from'))
            if self.variable is {}:
                raise ValidationError('variable', _('Please enter the values of the variables '
                                                    'shown at the library'))
        super(Template, self).clean()


class Vpn(ShareableOrgMixin, AbstractVpn):
    """
    openwisp-controller VPN model
    """
    ca = models.ForeignKey('pki.Ca',
                           verbose_name=_('Certification Authority'),
                           on_delete=models.CASCADE)
    cert = models.ForeignKey('pki.Cert',
                             verbose_name=_('x509 Certificate'),
                             help_text=_('leave blank to create automatically'),
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)

    class Meta(AbstractVpn.Meta):
        abstract = False

    def clean(self):
        self._validate_org_relation('ca')
        self._validate_org_relation('cert')

    def _auto_create_cert_extra(self, cert):
        """
        sets the organization on the server certificate
        """
        cert.organization = self.organization
        return cert


class VpnClient(AbstractVpnClient):
    """
    m2m through model
    """
    config = models.ForeignKey('config.Config',
                               on_delete=models.CASCADE)
    vpn = models.ForeignKey('config.Vpn',
                            on_delete=models.CASCADE)
    cert = models.OneToOneField('pki.Cert',
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True)

    class Meta(AbstractVpnClient.Meta):
        abstract = False

    def _auto_create_cert_extra(self, cert):
        """
        sets the organization on the created client certificate
        """
        cert.organization = self.config.device.organization
        return cert


@python_2_unicode_compatible
class OrganizationConfigSettings(models.Model):
    """
    Configuration management settings
    specific to each organization
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.OneToOneField('openwisp_users.Organization',
                                        verbose_name=_('organization'),
                                        related_name='config_settings',
                                        on_delete=models.CASCADE)
    registration_enabled = models.BooleanField(_('auto-registration enabled'),
                                               default=True,
                                               help_text=_('Whether automatic registration of '
                                                           'devices is enabled or not'))
    shared_secret = models.CharField(_('shared secret'),
                                     max_length=32,
                                     unique=True,
                                     db_index=True,
                                     default=get_random_key,
                                     validators=[key_validator],
                                     help_text=_('used for automatic registration of devices'))

    class Meta:
        verbose_name = _('Configuration management settings')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.organization.name
