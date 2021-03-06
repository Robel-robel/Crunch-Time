from django.test import TestCase, Client
from django.urls import reverse

class TestMessageBoardViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.mainMessageBoard_url = reverse('mainMessageBoardView')
        self.messages_url = reverse('Messages')
        # self.manageusers_url = reverse('ManageUsers')
        # self.manageclubs_url = reverse('ManageClubs')
        # self.customiseusers_url = reverse('CustomiseUsers')
        self.sendmessage_url = reverse('SendMessage')
        # self.customiseclubs_url = reverse('CustomiseClub')

    # def test_messageBoard_GET(self):
    #    response = self.client.get(self.mainMessageBoard_url)
    #    # print(response)
    #    self.assertEquals(response.status_code, 200)
    #    #print(response.status_code)
    #    self.assertTemplateUsed(response, 'message_board/Main_Message_Board.html')

    def test_Messages_GET(self):
        response = self.client.get(self.messages_url)
        # print(response)
        self.assertEquals(response.status_code, 200)
        # print(response.status_code)
        self.assertTemplateUsed(response, 'Messages/messages.html')

    # def test_ManageUsers_GET(self):
    #     response = self.client.get(self.manageusers_url)
    #     # print(response)
    #     self.assertEquals(response.status_code, 200)
    #     # print(response.status_code)
    #     self.assertTemplateUsed(response, 'message_board/Create_Users.html')
    #
    # def test_ManageClubs_GET(self):
    #     response = self.client.get(self.manageclubs_url)
    #     # print(response)
    #     self.assertEquals(response.status_code, 200)
    #     # print(response.status_code)
    #     self.assertTemplateUsed(response, 'message_board/Customise_Clubs.html')
    #
    # def test_CustomiseUsers_GET(self):
    #     response = self.client.get(self.customiseusers_url)
    #     # print(response)
    #     self.assertEquals(response.status_code, 200)
    #     # print(response.status_code)
    #     self.assertTemplateUsed(response, 'message_board/Customise_Users.html')

    def test_SendMessage_GET(self):
        response = self.client.get(self.sendmessage_url)
        # print(response)
        self.assertEquals(response.status_code, 200)
        # print(response.status_code)
        self.assertTemplateUsed(response, 'message_board/Send_Message.html')

    # def test_CustomiseClubs_GET(self):
    #     response = self.client.get(self.customiseclubs_url)
    #     # print(response)
    #     self.assertEquals(response.status_code, 200)
    #     # print(response.status_code)
    #     self.assertTemplateUsed(response, 'message_board/Customise_Clubs.html')