# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making BK-LOG 蓝鲸日志平台 available.
Copyright (C) 2021 THL A29 Limited, a Tencent company.  All rights reserved.
BK-LOG 蓝鲸日志平台 is licensed under the MIT License.
License for BK-LOG 蓝鲸日志平台:
--------------------------------------------------------------------
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
We undertake not to change the open source license (MIT license) applicable to the current version of
the project delivered to anyone in the future.
"""

import pytz
from django.utils import timezone
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from apps.api import BKLoginApi
from apps.exceptions import ApiRequestError, ApiResultError
from apps.utils.cache import cache_half_minute
from apps.utils.local import activate_request, set_local_param


class UserLocalMiddleware(MiddlewareMixin):
    """
    国际化中间件，从BK_LOGIN获取个人配置的时区
    """

    def process_view(self, request, view, args, kwargs):
        activate_request(request)

        login_exempt = getattr(view, "login_exempt", False)
        if login_exempt:
            return None

        # 后台API不处理用户时区
        if settings.BKAPP_IS_BKLOG_API:
            set_local_param("time_zone", settings.TIME_ZONE)
            timezone.activate(pytz.timezone(settings.TIME_ZONE))
            request.session["bluking_timezone"] = settings.TIME_ZONE
            return None

        user_info = self._get_user_info(user=request.user.username)
        tzname = user_info.get("time_zone", settings.TIME_ZONE)
        set_local_param("time_zone", tzname)
        timezone.activate(pytz.timezone(tzname))
        request.session["bluking_timezone"] = tzname

    @staticmethod
    @cache_half_minute("{user}_user_info")
    def _get_user_info(*, user):
        try:
            return BKLoginApi.get_user({"username": user})
        except (ApiRequestError, ApiResultError):
            return {}
