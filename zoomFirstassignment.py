
class MiniBank:

    main_userInfo:dict={}
    transfer_log: dict = {}

    def firstOption(self):
        try:
            option:int = int(input("Press 1 to Login\nPress 2 to Register: "))

            if option == 1:
                self.login()
            elif option==2:
                self.register()
            else:
                print('This option has not this project')

        except Exception as error:
            print(error)

    def returnId(self,transfer_username):
        userInfo_length:int =len(self.main_userInfo)
        for i in range(1,userInfo_length+1):
            if self.main_userInfo[i]['r_username']==transfer_username:
                return i
        return None

    def menu(self,loginId):
        menu_input=int(input('press1 to Transfer:\npress2 to Withdraw:\npress3 to user data:'))

        if menu_input==1:
                if len(self.main_userInfo) < 2:
                    print(" Transfer not possible. Only one user exists.")
                    return

                transfer_username:str=input('Please enter username to transfer:')
                transfer_id:int = self.returnId(transfer_username)
                print("We get to transfer id",transfer_id)
                # print('MyId',loginId)
                if transfer_id==loginId:
                    print('You cannot transfer to yourself')
                    return

                try:
                    amount = int(input(f'Enter amount to transfer to {self.main_userInfo[transfer_id]["r_username"]}: '))
                    if self.main_userInfo[loginId]['r_amount']>=amount:
                        self.main_userInfo[loginId]['r_amount']-=amount
                        self.main_userInfo[transfer_id]['r_amount']+=amount
                        self.main_userInfo[loginId]['last_transfer'] = amount

                        print('Transfer Successful')
                        print(f"Amount Transferred: {amount}")

                    else:
                        print('Insufficient balance')

                except Exception as error:
                    print(error)



        elif menu_input==2:
                try:
                    if 'last_transfer' in self.main_userInfo[loginId]:

                        print("\n------ Withdraw (Transfer) Summary ------")
                        print(f"Username: {self.main_userInfo[loginId]['r_username']}")
                        print(f"Remaining Balance: {self.main_userInfo[loginId]['r_amount']}")
                    else:
                        print('Withdraw Failed')

                except Exception as error:
                    print(error)

        elif menu_input==3:
                update_input=int(input('Press1 to name change :\nPress2 to amount change:\n Press3 to password change:'))
                if update_input==1:
                    n_name=input('Please enter new name:')
                    self.main_userInfo[loginId]['r_username']=n_name
                    print('new username ',n_name)

                elif update_input==2:
                    n_amount=int(input('Please enter new amount:'))
                    self.main_userInfo[loginId]['r_amount']=n_amount
                    print('new amount',n_amount)

                elif update_input==3:
                    n_password=int(input('Please enter new password:'))
                    self.main_userInfo[loginId]['r_password2']=n_password
                    print('new password',n_password)
                else:
                    print('Invalid Input')
        else:
            print('Invalid option')

    def log_transfer(self, user_id, message):
        if user_id not in self.transfer_log:
            self.transfer_log[user_id] = []
        self.transfer_log[user_id].append(message)


    def login(self):
        print("------------This is from login page-------------")
        l_username:str=input('Please enter your username:')
        l_password:int=int(input('Please enter your password:'))

        exitUsername=self.exitUsername(l_username,l_password)
        if(exitUsername):
            print('-------Login successful-------')
            loginId:int=self.returnId(l_username)
            self.menu(loginId)
        else:
            print('you cannot login')


    def exitUsername(self,l_username,l_password):
        user_count=len(self.main_userInfo)
        for i in range(1,user_count+1):
            if self.main_userInfo[i]['r_username']==l_username and self.main_userInfo[i]['r_password2']==l_password:
                return True
            else:
                return False


    def register(self):
        print("-------------This is from register page----------")
        r_username:str=input('Please enter username to register:')

        for user in self.main_userInfo.values():
            if user['r_username'] == r_username:
                print(" Username already exists. Try a different one.")
                return

        r_amount:int=int(input('please enter your amount:'))
        r_password1:int=int(input('Please enter password to register:'))
        r_password2:int=int(input('Please enter your confirm password:'))

        if r_password1==r_password2:
            id:int=self.checkingUserCount()
            userInfoForm:dict={id:{'r_username':r_username,'r_password2':r_password2,'r_amount':r_amount}}
            self.main_userInfo.update(userInfoForm)
            print('\n---------register successful--------\n')
            print(self.main_userInfo)


    def checkingUserCount(self):
        count=len(self.main_userInfo)
        return count+1


if __name__=="__main__":
    miniBank :MiniBank =MiniBank()
    while True:
        miniBank.firstOption()