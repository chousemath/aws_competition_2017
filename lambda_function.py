"""
This script contains the fundamental logic of a Doc&Me basic plan bot
"""

# import pyrebase
# from random import randint
#
# CONFIG = {
#     'apiKey': 'AIzaSyBryCO9fKB-lr5PWJljlmqzOIg_YZ--7bs',
#     'authDomain': 'kakao-32f6d.firebaseapp.com',
#     'databaseURL': 'https://kakao-32f6d.firebaseio.com',
#     'projectId': 'kakao-32f6d',
#     'storageBucket': 'kakao-32f6d.appspot.com',
#     'messagingSenderId': '1000763530924'
# }
# FIREBASE = pyrebase.initialize_app(CONFIG)
# DB = FIREBASE.database()

def lambda_handler(event, context):
    """
    Entry point for all AWS Lambda functions
    """
    if event.get('content') and event.get('type') == 'text':
        # user_key = event.get('user_key')
        # state_set(user_key, randint(0,9))
        return resp_dict(event.get('content'))
    return resp_type_2(phrase_dict('처음으로'), buttons_dict('처음으로'))

def resp_dict(phrase):
    """
    Returns appropriate Kakao-friendly JSON response according to input key
    JSON format is defined in https://github.com/plusfriend/auto_reply.
    """
    switcher = {
        '처음으로': resp_type_2(phrase_dict('처음으로'), buttons_dict('처음으로')),
        '병원 정보': resp_type_2(phrase_dict('병원 정보'), buttons_dict('병원 정보')),
        '병원 위치': resp_type_5(
            phrase_dict('병원 위치'),
            make_msg_btn('https://www.google.co.kr', '전화하기'),
            make_photo(photo_dict('병원 위치'))
        ),
        '병원 운영시간': resp_type_4(phrase_dict('병원 운영시간'), make_photo(photo_dict('병원 운영시간'), 792, 612)),
        '병원 프로모션': resp_type_2(phrase_dict('병원 프로모션'), buttons_dict('병원 프로모션')),
        '프로모션 A': resp_type_4(phrase_dict('프로모션 A'), make_photo(photo_dict('프로모션 A'), 600, 345)),
        '프로모션 B': resp_type_4(phrase_dict('프로모션 B'), make_photo(photo_dict('프로모션 B'), 600, 345)),
        '프로모션 C': resp_type_4(phrase_dict('프로모션 C'), make_photo(photo_dict('프로모션 C'), 600, 332)),
        '의료진': resp_type_6(phrase_dict('의료진'), buttons_dict('의료진'), make_photo(photo_dict('의료진'), 736, 769)),
        '병원 사진': resp_type_6(phrase_dict('병원 사진'), buttons_dict('병원 사진'), make_photo(photo_dict('병원 사진'), 800, 480)),
        '병원 진료과목': resp_type_4(phrase_dict('병원 진료과목'), make_photo(photo_dict('병원 진료과목'), 250, 250)),
        '병원 전화하기': resp_type_3(phrase_dict('병원 전화하기'), make_msg_btn('https://www.google.co.kr', '전화하기'))
    }
    return switcher.get(phrase, resp_type_2(phrase_dict('처음으로'), buttons_dict('처음으로')))

def resp_type_1(text):
    """
    Formats Kakao-friendly JSON with a text message
    JSON format is defined in https://github.com/plusfriend/auto_reply.
    """
    return {'message': {'text': text}}

def resp_type_2(text, buttons):
    """
    Formats Kakao-friendly JSON with a text message and selectable buttons
    JSON format is defined in https://github.com/plusfriend/auto_reply.
    """
    return {
        'message': {'text': text},
        'keyboard': {'type': 'buttons', 'buttons': buttons}
    }

def resp_type_3(text, message_button):
    """
    Formats Kakao-friendly JSON with a text message and message button
    JSON format is defined in https://github.com/plusfriend/auto_reply.
    """
    return {
        'message': {
            'text': text,
            'message_button': {
                'label': message_button['label'],
                'url': message_button['url']
            }
        }
    }

def resp_type_4(text, photo):
    """
    Formats Kakao-friendly JSON with a text message and photo
    JSON format is defined in https://github.com/plusfriend/auto_reply.
    """
    return {
        'message': {
            'text': text,
            'photo': {
                'url': photo['url'],
                'width': photo['width'],
                'height': photo['height']
            }
        }
    }

def resp_type_5(text, message_button, photo):
    """
    Formats Kakao-friendly JSON with text, photo, and message button
    JSON format is defined in https://github.com/plusfriend/auto_reply.
    """
    return {
        'message': {
            'text': text,
            'message_button': {
                'label': message_button['label'],
                'url': message_button['url']
            },
            'photo': {
                'url': photo['url'],
                'width': photo['width'],
                'height': photo['height']
            }
        }
    }

def resp_type_6(text, buttons, photo):
    """
    Formats Kakao-friendly JSON with a text message, photo, and buttons
    JSON format is defined in https://github.com/plusfriend/auto_reply.
    """
    return {
        'message': {
            'text': text,
            'photo': {
                'url': photo['url'],
                'width': photo['width'],
                'height': photo['height']
            }
        },
        'keyboard': {'type': 'buttons', 'buttons': buttons}
    }

def phrase_dict(phrase):
    """
    Returns correct phase according to the input key
    The specific phrases are defined in James' bot architecture guidelines.
    """
    switcher = {
        '처음으로': '닥앤미 병원을 찾아주셔서 감사합니다. 직접문의원할시 오른쪽 아래 1:1 버튼을 눌러주시면 직접 상담 가능합니다. 1:1 상담 가능 시간은 09시 – 18시 입니다.',
        '병원 정보': '어떤 정보를 보시고 싶으신가요?',
        '병원 위치': '“닥앤미 병원 주소는 서울시 용산구 이촌동 세움상가 2층입니다.” 더 자세한 지도확인을 원하실 경우 아래 버튼을 눌러주세요',
        '병원 운영시간': '닥앤미 병원을 찾아주셔서 감사합니다. 병원 운영시간은 위의 내용과 같습니다',
        '병원 프로모션': '현재 진행되고 있는 병원 프로모션입니다. 자세히 보길 원하시면 아래의 프로모션을 선택해 주세요',
        '프로모션 A': '닥앤미에서 6월 30일까지 제공되는 프로모션 A 입니다.',
        '프로모션 B': '닥앤미에서 6월 30일까지 제공되는 프로모션 B 입니다.',
        '프로모션 C': '닥앤미에서 6월 30일까지 제공되는 프로모션 C 입니다.',
        '의료진': '안녕하세요, 닥앤미의 홍길동 전문의 입니다. 항상 최선을 다하겠습니다.',
        '병원 사진': '최고의 진료를 제공하는 닥앤미 병원입니다.',
        '병원 진료과목': '닥앤미 병원의 진료과목입니다.',
        '병원 전화하기': '닥앤미 병원 전화번호는 02 3522 XXXX 입니다. 지금 통화를 원하시면 아래 버튼을 눌러주세요'
    }
    default_text = 'Unable to find appropriate text response'
    return switcher.get(phrase, default_text)

def buttons_dict(phrase):
    """
    Returns correct button array according to the input key
    The specific phrases are defined in James' bot architecture guidelines.
    """
    switcher = {
        '처음으로': ['병원 정보', '병원 위치', '병원 운영시간', '병원 프로모션'],
        '병원 정보': ['의료진', '병원 사진', '병원 진료과목', '병원 전화하기'],
        '병원 프로모션': ['프로모션 A', '프로모션 B', '프로모션 C'],
        '의료진': ['홍길동 피부과 전문의', '김제인 마취과 전문의', '김존 피부과 전문의'],
        '병원 사진': ['내부', '건물', '진료실']
    }
    default_buttons = []
    return switcher.get(phrase, default_buttons) + ['처음으로']

def photo_dict(phrase):
    """
    Returns correct photo url according to the input key
    The specific phrases are defined in James' bot architecture guidelines.
    """
    switcher = {
        '병원 위치': 'https://maps.googleapis.com/maps/api/staticmap?center=37.507144,127.063737&zoom=16&size=640x480&markers=color:blue%7Clabel:S%7C37.507144,127.063737&key=AIzaSyCF-XXYf7IW1mkUZFeZF84BCcZdtC-z1M0',
        '병원 운영시간': 'http://gunn.pausd.org/sites/default/files/16-17-Bell-Schedule-Color---Compatible-Font.png',
        '프로모션 A': 'http://media.dontpayfull.com/media/deals/eurostar-promo-code.jpg',
        '프로모션 B': 'http://media.dontpayfull.com/media/deals/namebubbles-com-coupon-code.jpg',
        '프로모션 C': 'https://s-media-cache-ak0.pinimg.com/originals/79/79/31/79793174d230a27e9168bbccb33df62f.jpg',
        '의료진': 'https://s-media-cache-ak0.pinimg.com/736x/f4/89/ef/f489ef22363cf1e4c2a4fb5b1cd8aec5.jpg',
        '병원 사진': 'https://www.hpcimedia.com/images/website/ManChemNews/DIR_30/F_28071.jpg',
        '병원 진료과목': 'https://s-media-cache-ak0.pinimg.com/originals/d5/05/09/d505091a57d42d3ed1de8b6f9d906fdb.jpg'
    }
    default_url = 'http://autopartstoys.com/images/M127205243.jpg'
    return switcher.get(phrase, default_url)

def make_msg_btn(url, label):
    """
    Returns a dictionary with all the attributes for a Kakao message button
    JSON format is defined in https://github.com/plusfriend/auto_reply.
    """
    return {
        'url': url,
        'label': label
    }

def make_photo(url, width=640, height=480):
    """
    Returns a dictionary with all the attributes for a Kakao photo
    JSON format is defined in https://github.com/plusfriend/auto_reply.
    """
    return {
        'url': url,
        'width': width,
        'height': height
    }

# def state_set(user_key, state):
#     """
#     Makes or overrides a user state entry in Firebase
#     All Python commands are defined here: https://github.com/thisbejim/Pyrebase
#     """
#     data = {'state': state}
#     DB.child('user_states').child('sample-bot-basic-' + user_key).set(data)
#
# def state_get(user_key):
#     """
#     Gets a user state entry from Firebase, creates a new one if none is present
#     All Python commands are defined here: https://github.com/thisbejim/Pyrebase
#     """
#     user_state = DB.child('user_states').get().val().get('sample-bot-basic-' + user_key)
#     if user_state:
#         return user_state.get('state')
#     state_set(user_key, 'base')
#     return 'base'
