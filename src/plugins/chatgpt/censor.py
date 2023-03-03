import json
import sys

from typing import List

from alibabacloud_imageaudit20191230.client import Client as imageaudit20191230Client
from alibabacloud_imageaudit20191230.models import ScanTextResponse
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_imageaudit20191230 import models as imageaudit_20191230_models
from alibabacloud_tea_util import models as util_models
from nonebot import logger


class AliyunCensor:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> imageaudit20191230Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = f'imageaudit.cn-shanghai.aliyuncs.com'
        return imageaudit20191230Client(config)

    @staticmethod
    def main(
        content: str,
    ) -> ScanTextResponse:
        # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS
        # 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = AliyunCensor.create_client('***', '***')
        labels_0 = imageaudit_20191230_models.ScanTextRequestLabels(
            label='politics'
        )
        tasks_0 = imageaudit_20191230_models.ScanTextRequestTasks(
            content=content
        )
        scan_text_request = imageaudit_20191230_models.ScanTextRequest(
            tasks=[
                tasks_0
            ],
            labels=[
                labels_0
            ]
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            return client.scan_text_with_options(scan_text_request, runtime)
        except Exception as error:
            # 如有需要，请打印 error
            logger.error(str(error))

    @staticmethod
    def is_block(content):
        results = AliyunCensor.main(content=content)
        elements = results.body.data.elements
        for element in elements:
            for result in element.results:
                if result.suggestion == 'block':
                    return True
        return False
