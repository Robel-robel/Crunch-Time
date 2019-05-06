from django.test import TestCase, Client
from django.urls import reverse

class TestViews(TestCase):

    def setUp(self):
        self.cleint = Client()
        self.messageBoard_url = reverse('messageBoardView')
        self.messages_url = reverse('Messages')
        self.mainmessages_url = reverse('MainMessageBoard')
        self.manageusers_url = reverse('ManageUsers')

    #def test_AdminMessageBoard_GET(self):
    #    response = self.client.get(self.messageBoard_url)
    #    #print(response)
    #    self.assertEquals(response.status_code, 200)
    #    #print(response.status_code)
    #    self.assertTemplateUsed(response, 'message_board/Admin_message_board.html')

    def test_Messages_GET(self):
        response = self.client.get(self.messages_url)
        # print(response)
        self.assertEquals(response.status_code, 200)
        # print(response.status_code)
        self.assertTemplateUsed(response, 'Messages/messages.html')

    def test_MainMessages_GET(self):
        response = self.client.get(self.mainmessages_url)
        # print(response)
        self.assertEquals(response.status_code, 200)
        # print(response.status_code)
        self.assertTemplateUsed(response, 'message_board/Main_Message_Board.html')

    def test_ManageUsers_GET(self):
        response = self.client.get(self.manageusers_url)
        # print(response)
        self.assertEquals(response.status_code, 200)
        # print(response.status_code)
        self.assertTemplateUsed(response, 'message_board/Manage_Users.html')
