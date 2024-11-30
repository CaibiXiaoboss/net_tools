import requests
import time
from util import yaml_io


def upload_image(access_token, image_path: str):
    """
    上传图片素材并获取media_id
    :param access_token: 微信公众号的access_token
    :param image_path: 图片文件的本地路径
    :return: 返回包含media_id的响应数据
    """
    url = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token={}&type=image".format(access_token)
    files = {'media': open(image_path, 'rb')}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        result = response.json()
        if 'media_id' in result:
            return result['media_id']
        else:
            raise Exception("上传图片素材失败，错误信息：{}".format(result['errmsg']))
    else:
        raise Exception("上传图片请求失败，状态码：{}".format(response.status_code))


class WechatAccessTokenManager:
    def __init__(self, config_file='config.yaml'):
        self.config = yaml_io.read_yaml(config_file)
        self.expires_at = 0

    def get_access_token(self):
        """
        获取一个访问的token
        :return:
        access_token:str
        live_time:int
        """
        appid = self.config['AppID']
        app_secret = self.config['AppSecret']
        url = "https://api.weixin.qq.com/cgi-bin/token?" \
              "grant_type=client_credential&appid={}&secret={}".format(appid, app_secret)
        response = requests.get(url)

        if response.status_code == 200:
            result = response.json()
            try:
                access_token = result['access_token']
                expires_in = result['expires_in']
                return access_token, expires_in
            except KeyError:
                print("Response JSON does not contain expected keys.")
                return None, None
        else:
            print("Failed to retrieve access token, HTTP status code:", response.status_code)
            return None, None

    def _is_valid(self, access_token):
        return self.expires_at > time.time()


class WechatMaterialManager:
    def __init__(self, access_token):
        self.access_token = access_token
        self.offset = 0
        self.count = 20

    def add_permanent_article(self, articles):
        """
        新增永久图文素材
        :param articles: 图文素材列表，每个元素是一个包含图文信息的字典
        :return: 返回微信服务器响应的JSON数据
        """
        url = "https://api.weixin.qq.com/cgi-bin/material/add_news?access_token={}".format(self.access_token)
        data = {
            "articles": articles
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            return result
        else:
            raise Exception("新增永久图文素材请求失败，状态码：{}，内容：{}".format(response.status_code, response.text))

    def get_permanent_material(self, media_id):
        """
        获取永久素材
        :param media_id: 永久素材的media_id
        :return: 返回素材内容，如果是图文素材则为包含图文信息的字典列表
        """
        url = "https://api.weixin.qq.com/cgi-bin/material/get_material?access_token={}".format(self.access_token)

        # 对于非文件类型素材（如图文），应使用data而非files
        data = {"media_id": media_id}

        headers = {
            'Content-Type': 'application/json'  # 实际上获取永久素材不需要Content-Type为json，但对于GET请求通常无需设置此头
        }

        # 使用requests.get()来获取非文件类型的素材（如图文）
        # 注意：对于获取永久素材接口，实际上应当使用requests.get()而非requests.post()
        response = requests.get(url, params=data)

        if response.status_code == 200:
            # 处理响应体，如果是图文素材，返回其内容
            if 'news_item' in response.json().keys():
                return response.json()['news_item']
            else:
                # 针对非图文素材，这里可能是错误处理或者进一步解析不同素材类型
                raise Exception("素材类型不是图文消息")
        else:
            raise Exception("获取永久素材请求失败，状态码：{}，内容：{}".format(response.status_code, response.text))

    def get_material_list(self, the_type='news'):
        """
        分页获取永久素材列表，目前仅支持图文素材类型（'news'）
        :param the_type: 素材类型，默认为图文素材
        :return: 返回包含多个素材信息的列表
        """
        all_materials = []
        while True:
            url = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={}".format(
                self.access_token)
            payload = {
                "type": the_type,
                "offset": self.offset,
                "count": self.count
            }
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                result = response.json()
                materials = result.get('item', [])
                all_materials.extend(materials)

                # 判断是否还有更多素材
                total_count = result.get('total_count', 0)
                if len(all_materials) >= total_count:
                    break
                else:
                    self.offset += self.count
            else:
                raise Exception("获取素材列表失败，状态码：{}，内容：{}".format(response.status_code, response.text))

        return all_materials
