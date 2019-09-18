from datetime import datetime

import requests
from requests import ConnectTimeout, ReadTimeout

from BaseResponse import BaseResponse
from EncryptionUtil import EncryptionConfig
from EnvironmentConfig import EnvironmentConfig
from SdkResponseCode import SdkResponseCode
from Timestamp import Timestamp


class GetActiveBanks(object):

    def get_active_banks(self, get_active_banks_payload, credentials):

        try:
            get_response = EnvironmentConfig()
            if not get_response.credential_available(credentials):
                return get_response.throw_exception(status=get_response.empty_credential_code,
                                                    data=get_response.empty_credential_msg)
            else:
                rpg_environment = EnvironmentConfig.set_rpg_environment(credentials)
                headers = self.set_header(get_active_banks_payload, credentials)
                url = rpg_environment['GET_ACTIVE_BANKS_URL']
                if not credentials.connection_timeout:
                    credentials.connection_timeout = 30000
                config = EncryptionConfig()
                payload = {}

                try:
                    response = requests.post(url, headers=headers, json=payload, timeout=credentials.connection_timeout)
                    get_active_banks_response = BaseResponse(response.content)


                except ConnectTimeout:
                    return get_response.throw_exception(status=SdkResponseCode.CONNECTION_TIMEOUT_CODE,
                                                        data=SdkResponseCode.CONNECTION_TIMEOUT)
                except ValueError:
                    return get_response.throw_exception(status=SdkResponseCode.ERROR_IN_VALUE_CODE,
                                                        data=SdkResponseCode.ERROR_IN_VALUE)
                except ReadTimeout:
                    return get_response.throw_exception(status=SdkResponseCode.CONNECTION_TIMEOUT_CODE,
                                                        data=SdkResponseCode.CONNECTION_TIMEOUT)
                except ConnectionError as e:  # This is the correct syntax
                    return get_response.throw_exception(status=SdkResponseCode.ERROR_WHILE_CONNECTING_CODE,
                                                        data=SdkResponseCode.ERROR_WHILE_CONNECTING)

            return get_active_banks_response

        except Exception:
            return get_response.throw_exception(status=SdkResponseCode.ERROR_PROCESSING_REQUEST_CODE,
                                                data=SdkResponseCode.ERROR_PROCESSING_REQUEST)
    def set_header(self, get_active_banks_payload, credentials):

        hash_string = credentials.api_key + get_active_banks_payload.request_id + credentials.api_token

        txn_hash = EncryptionConfig.sha512(hash_string)
        time_stamp = Timestamp()

        headers = {'Content-Type': 'application/json', 'MERCHANT_ID':credentials.merchant_id, 'API_KEY':credentials.api_key,
                   'REQUEST_ID':get_active_banks_payload.request_id, 'REQUEST_TS':time_stamp.dateTimeObj(dateTimeObj=datetime.now()),
                   'API_DETAILS_HASH': txn_hash}
        return headers



