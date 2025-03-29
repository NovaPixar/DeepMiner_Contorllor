# coding: utf-8


class LicenseService:
    """ License service """

    def validate(self, license: str, email: str):
        """ Verify if the activation code is legal """
        if license == "123456":

            return True
        return False

