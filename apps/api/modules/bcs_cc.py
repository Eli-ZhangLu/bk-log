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
"""
import json

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from apps.api import BkSSMApi
from apps.api.modules.utils import add_esb_info_before_request
from config.domains import BCS_CC_APIGATEWAY_ROOT
from apps.api.base import DataAPI


def bcs_cc_before_request(params):
    params = add_esb_info_before_request(params)
    if settings.BCS_CC_SSM_SWITCH:
        bkssm_access_token = BkSSMApi.get_access_token({"grant_type": "client_credentials", "id_provider": "client"})
        access_token = bkssm_access_token["access_token"]
        params["X-BKAPI-AUTHORIZATION"] = json.dumps({"access_token": access_token})
    return params


def bcs_get_cluster_config_after(response):
    response["data"] = json.loads(response["data"]["configure"])
    return response


class _BcsCcApi(object):
    MODULE = _(u"Bcs cc 配置中心")

    def __init__(self):
        self.get_cluster_config_by_cluster_id = DataAPI(
            method="GET",
            url=BCS_CC_APIGATEWAY_ROOT + "v1/clusters/{cluster_id}/cluster_config/",
            module=self.MODULE,
            url_keys=["cluster_id"],
            description=u"根据集群id获取集群信息",
            header_keys=["X-BKAPI-AUTHORIZATION"],
            before_request=bcs_cc_before_request,
            after_request=bcs_get_cluster_config_after,
        )
        self.get_cluster_by_cluster_id = DataAPI(
            method="GET",
            url=BCS_CC_APIGATEWAY_ROOT + "clusters/{cluster_id}/",
            module=self.MODULE,
            url_keys=["cluster_id"],
            description=u"根据集群id获取集群信息",
            header_keys=["X-BKAPI-AUTHORIZATION"],
            before_request=bcs_cc_before_request,
        )
        self.list_cluster = DataAPI(
            method="GET",
            url=BCS_CC_APIGATEWAY_ROOT + "cluster_list/",
            module=self.MODULE,
            before_request=bcs_cc_before_request,
            header_keys=["X-BKAPI-AUTHORIZATION"],
        )
        self.list_area = DataAPI(
            method="GET",
            url=BCS_CC_APIGATEWAY_ROOT + "areas/",
            module=self.MODULE,
            before_request=bcs_cc_before_request,
            header_keys=["X-BKAPI-AUTHORIZATION"],
        )
        self.list_project = DataAPI(
            method="GET",
            url=BCS_CC_APIGATEWAY_ROOT + "projects/",
            module=self.MODULE,
            before_request=bcs_cc_before_request,
            header_keys=["X-BKAPI-AUTHORIZATION"],
        )
