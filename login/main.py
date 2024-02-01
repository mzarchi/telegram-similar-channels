import sys
import getpass
import telethon
from telethon.sync import TelegramClient
import re


sys.path.append('./')
import config as ac


class ClientManager:
    """Base Class For login"""
    __phoneNumber = None
    __TwoFactor = None
    __LoginCode = None
    __Client = None

    def ValidatePhone(self, phone: str) -> bool:
        """Validate user input is a valid phone number
        ~~~~~~~~~~~~~~~~~~~~~
        Args:
            :param `phone`: (str) telegram phone number

        Returns:
            :return: (bool)
        """
        reg = r"^\+[0-9]{12,12}$"
        # example: +981234567891
        return True if re.search(reg, phone) else False

    def GetPhoneNumber(self):
        """Get User Phone Number"""
        while True:
            x = input(
                "Enter you're phone number is form of +<country code><phone number>: ")
            if not self.ValidatePhone(x):
                print("Invalid Phone number :(")
                continue
            else:
                self.__phoneNumber = x
                break

    def GetLoginCode(self):
        """Get Telegram Code in Hidden Mode"""
        self.__LoginCode = getpass.getpass("LoginCode: ")

    def GetTwoStepCode(self):
        """Get 2-Step code in hidden mode"""
        self.__TwoFactor = getpass.getpass("2-Step Code: ")

    def LoginClient(self):
        """Login Method"""
        self.GetPhoneNumber()
        client = TelegramClient(
            ac.SESSION_FILE_NAME, ac.API_ID, ac.API_HASH)
        client.connect()
        client.send_code_request(self.__phoneNumber, force_sms=False)
        self.GetLoginCode()
        try:
            client.sign_in(self.__phoneNumber, code=self.__LoginCode)
        except telethon.errors.SessionPasswordNeededError:
            self.GetTwoStepCode()
            client.sign_in(password=self.__TwoFactor)
        print("Successfully Connect!\nSession created at sessions dir")
        self.__Client = client

    def GetClient(self):
        """Use This Method For Getting <TelegramClient> client"""
        return self.__Client


client = ClientManager()
client.LoginClient()
