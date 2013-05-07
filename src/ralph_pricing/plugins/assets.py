# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ralph.util import plugin
from ralph_assets.api_pricing import get_assets
from ralph_pricing.models import Device


def update_assets(data, date):
    device, created = Device.objects.get(
        device_id=data['device_id'],
    )
    device.asset_id = data['asset_id']
    device.slots = data['slots']
    device.save()
    daily, daily_created = DailyDevice.objects.get_or_create(
        date=date,
        pricing_device=device,
    )
    daily.price
    daily.save()
    return created


@plugin.register(chain='pricing', requires=['sync_devices'])
def sync_assets(**kwargs):
    """Updates the devices from Ralph Assets."""

    date = kwargs['today']
    count = sum(update_assets(data, date) for data in get_assets())
    return True, '%d new devices' % count, kwargs

