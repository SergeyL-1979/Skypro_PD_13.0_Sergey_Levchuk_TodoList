# import json
# import pytest
# from django.urls import reverse
# from rest_framework import status
# from tests import factories
#
#
# @pytest.mark.django_db
# def test_bot_verify(auth_client, user):
#     factories.TuserFactory.create(
#         chat_id=124315315,
#         user_id=12431,
#         user_ud=124315315,
#         username='test_user',
#         user=user,
#         verification_code='correct'
#     )
#     url: str = reverse('bot:verify')
#     payload1 = {
#         'verification_code': 'correct'
#     }
#     payload2 = {
#         'verification_code': 'incorrect'
#     }
#
#     response1 = auth_client.patch(
#         path=url,
#         data=json.dump(payload1),
#         content_type='application/json',
#     )
#     response2 = auth_client.patch(
#         path=url,
#         data=json.dumps(payload2),
#         content_type='application/json',
#     )
#
#     assert response1.status_code == status.HTTP_201_CREATED
#     assert response2.status_code == status.HTTP_400_BAD_REQUEST
