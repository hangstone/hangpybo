from django.apps import AppConfig


# PyboConfig 클래스는 config/base.py 파일의 INSTALLED_APPS 항목에 추가되어야 한다.
# 그렇지 않으면, 장고는 pybo 앱을 인식하지 못하고, DB 관련 작업도 할 수 없다.
# 자세힐 설명하면, 장고는 모델을 이용하여 DB의 실체가 될 테이블을 만드는데, 모델은 앱에 종속되어
# 있으므로 반드시 장고에 앱을 등록해야 테이블 작업을 진행할 수 있다.
class PyboConfig(AppConfig):
    name = 'pybo'
