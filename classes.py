from datetime import date, time
import itertools
import random
class Bank():
    """Class created for bank entities
    
    Attributes
    ---------
    interest_rate: float
        current interest rate for all banks to use
    used_credit_card_num_lst: list
        all existing credit card numbers 
    """
    interest_rate = 0.0225
    used_credit_card_num_lst = []
    
    def __init__(self, name, location, opening_hours, closing_hours):
        """Initialize a bank instance

        Parameters
        ----------
        name: string
            name of bank instance
        location: string
            location of bank instance
        opening_hours/closing_hours: string (in military hours:minutes format)
            operating times of bank instance

        Attributes
        ---------
        accounts: dict
            {str: object} pairs with {account_id: Account object} information
        all_detail_accounts: list
            list of all type of accounts (checking, savings, credit) created in the bank
        processed_transaction_id: list
            list of all transactions under this bank instance
        """
        if "Bank" not in name:
            self.name = name + " Bank"
        else:
            self.name = name

        self.location = location
        self.opening_hours = time(int(opening_hours.split(":")[0]), int(opening_hours.split(":")[1]))
        self.closing_hours = time(int(closing_hours.split(":")[0]), int(closing_hours.split(":")[1]))
      
        self.accounts = {} #Changed to dictionary
        self.all_detail_accounts = []
        self.processed_transaction_id = []
    
    def summarize_account_balance(account):
        """Pretty print out balances in accounts
        
        Parameters
        ----------
        account: type(Account), type(CheckingAccount), type(SavingsAccount), type(CreditAccount)
            accounts that require printing out balances
            
        Returns
        -------
        If given detail accounts, will only print out single detail account. 
        Otherwise, will print out all balances associated with account.
        """
        account.summarize_account_balance()

    def open_accounts(self, owner, type_accounts = None, starting_amounts = None):
        """Open new customer account with random assigned account id. 
        If given (type_accounts, starting_amounts), create detail account as well.
        
        Parameters
        ----------
        owner: string
            name of the account owner
        type_accounts: list of str or str, optional
            list of types of account, or single type of account to be created. 
            must contain character variants of ("checking", "savings", "credit")
        starting_amounts: list of int or float or (int or float), optional
            list of starting amounts, or single starting amount associated with account
          
        Return
        ------
        new_account: type(Account)
            Account object containing various information such as owner, account_id, associated detail accounts
            
        Note
        ----
        len(type_accounts) must be at least len(starting_amounts) 
        (best to be equal but allow for error/missing values).
        starting_amounts will be defaulted as 0 if not positive values. 
        """
        account_id = random.randint(10 ** 5, (10 ** 6) - 1)
        while account_id in self.accounts.keys():
            account_id = random.randint(10 ** 5, (10 ** 6) - 1)
            
        new_account = Account(owner, account_id, self)
        self.accounts[str(account_id)] = new_account
        
        # Generate associated accounts if optional parameters given right type
        if type_accounts != None and starting_amounts != None:
            
            if isinstance(type_accounts, list) and isinstance(starting_amounts, list):
                self.add_accounts(new_account, type_accounts, starting_amounts)
                
            elif isinstance(type_accounts, str) and isinstance(starting_amounts, (int, float)):
                
                if type_accounts.lower() == "checking":
                    self.add_checking_account(account, starting_amounts)
                elif type_accounts.lower() == "savings":
                    self.add_savings_account(account, starting_amounts)
                elif type_accounts.lower() == "credit":
                    self.add_credit_account(account, starting_amounts)
                    
        return new_account
    
    def add_accounts(self, account, type_accounts, starting_amounts):
        """Wrapper to Open multiple accounts with different types
        
        Parameters
        ----------
        account: type(Account)
            account that detail account will associate with
        type_accounts: list of str
            list of types of account, must contain character variants of ("checking", "savings", "credit")
        starting_amounts: list of int or float
            list of starting amounts, must be >=0 or will default 0.
        """
        # Loop through individual (type_account, starting_amount) pair 
        # None value terms filled for starting_amount if len(type_accounts) > len(starting_amounts)
        for type_account, starting_amount in itertools.zip_longest(type_accounts, starting_amounts):
            
            if not isinstance(starting_amount, (int, float)):
                starting_amount = 0 # replace None value with 0
                
            if type_account.lower() == "checking":
                self.add_checking_account(account, starting_amount)
            elif type_account.lower() == "savings":
                self.add_savings_account(account, starting_amount)
            elif type_account.lower() == "credit":
                self.add_credit_account(account, starting_amount)
                    
    def add_checking_account(self, account, starting_amount):
        """Open one checking account
        
        Parameters
        ----------
        account: type(Account)
            customer account that this checking account will associate with
        starting_amount: int or float
            must be >=0 or will default 0.
        """   
        if (not account.has_checking):
            account.has_checking = True
            
            if starting_amount < 0:
                print("WARNING: You are adding negative balance to the account. Defaulting to 0 balance.")
                starting_amount = 0
                
            new_checking_account = CheckingAccount(account, starting_amount, self)
            account.detail_accounts.append(new_checking_account)
            self.all_detail_accounts.append(new_checking_account)
            
        elif account.has_checking:
            print("ERROR: Checking Account exists. Unable to create another")
                
    def add_savings_account(self, account, starting_amount):
        """Open one savings account
        
        Parameters
        ----------
        account: type(Account)
            customer account that this savings account will associate with
        starting_amount: int or float
            must be >=0 or will default 0.
        """
        if (not account.has_savings):
            account.has_savings = True
            
            if starting_amount < 0:
                print("WARNING: You are adding negative balance to the account. Defaulting to 0 balance.")
                starting_amount = 0
                
            new_savings_account = SavingsAccount(account, starting_amount, self)
            account.detail_accounts.append(new_savings_account)
            self.all_detail_accounts.append(new_savings_account)
        
        elif account.has_savings:
            print("ERROR: Savings Account exists. Unable to create another")
    
    def add_credit_account(self, account, credit_limit):
        """Open one credit account
        
        Parameters
        ----------
        account: type(Account)
            customer account that this credit account will associate with
        credit_limit: int or float
            limit of balances, must be >=0 or will default 100.
        """  
        new_credit_card_num = random.randint(10 ** 16, 10 ** 17 -1)
        while new_credit_card_num in Bank.used_credit_card_num_lst:
            new_credit_card_num = random.randint()
        Bank.used_credit_card_num_lst.append(new_credit_card_num)
        
        if credit_limit <= 0:
            print("WARNING: You are requesting 0 or less credit limit to the account. Defaulting 100.")
            credit_limit = 100
        
        new_credit_account = CreditAccount(account, new_credit_card_num, credit_limit, self)
        account.detail_accounts.append(new_credit_account)
        account.num_credit_account += 1
        self.all_detail_accounts.append(new_credit_account)

    def add_transaction_to_account(self, account, date, description, amount, is_debit,
                                   type_account = None, credit_card_num = None):
        """Add one transaction to certain account
        
        Parameters
        ----------
        account: type(Account), type(CheckingAccount), type(SavingsAccount), type(CreditAccount)
            account that this transaction would add onto
        date: type(datetime.date) or str
            transaction date
        description: str
        amount: int or float
        is_debit: bool
            in terms of accounting, indicating a subtraction (debit) or addition (credit) to balances. 
            CreditAccount will always be addition to balance
        type_account: str, optional
            if the given account is type(Account), used to get the DetailAccount of certain type
        credit_card_num: int, optional
            if the given account is type(Account), used to get unique CreditAccount
        """
        if not is_real_account_in_bank(account):
            return None
        
        if isinstance(account, Account):
            detail_account = get_detail_account_of_type(type_account, account, credit_card_num)
            
        if account is None:
            return None
        
        account.add_transaction(detail_account, date, description, amount, is_debit)
        
    def transfer_to_account(self, from_account, to_account, date, description, amount, bank = None):
        """Transfer money within same bank
        
        Parameters
        ----------
        from_account: type(CheckingAccount), type(SavingsAccount)
            where to take money from
        to_account: type(CheckingAccount), type(SavingsAccount), type(CreditAccount)
            where to add money/pay balances(for CreditAccount)
        date: type(datetime.date) or str
            transaction date
        description: str
        amount: int or float
        """        
        if not isinstance(from_account, (CheckingAccount, SavingsAccount)):
            return None
        
        if to_account not in self.all_detail_accounts:
            return None
        
        amount = -amount
        transfer_transaction = Transaction(date, description, amount)
        from_account.transfer_to_account(to_account, transfer_transaction)
    
    def bank_transfer_to_account(self, from_account, to_bank, to_account, date, description, amount):
        """Interbank transfer
        
        Parameters
        ----------
        from_account: type(CheckingAccount), type(SavingsAccount)
            where to take money from
        to_bank: type(Bank)
            where to send the money to
        to_account: type(CheckingAccount), type(SavingsAccount), type(CreditAccount)
            where to add money/pay balances(for CreditAccount)
        date: type(datetime.date) or str
            transaction date
        description: str
        amount: int or float
        """
        if amount <= 0:
            return None
        
        if not isinstance(from_account, (CheckingAccount, SavingsAccount)):
            return None
        
        if to_account not in to_bank.all_detail_accounts:
            return None
        
        amount = -amount
        transfer_transaction = Transaction(date, description, amount)
        from_account.transfer_to_account(to_account, transfer_transaction)
    
    def print_bank_info(self):
        """Print out details of the bank
        
        Return
        ------
        Details of the bank including name, location, operating hours
        """
        print("{} at {} opens from {} to {}".format(
            self.name, self.location, self.opening_hours, self.closing_hours))
    
    def get_detail_account_of_type(self, type_account, account, credit_card_num = None):
        """Get the detail account with certain type under a customer account
        
        Parameters
        ----------
        type_account: str
            must contain character variants of ("checking", "savings", "credit")
        account: type(Account)
            customer account that contains the detail account with certain type
        credit_card_num: int, optional
            16 digit credit_card_num if requesting credit account
            
        Return
        ------
        detail_account: type(CheckingAccount), type(SavingsAccount), type(CreditAccount), None
            the detail account object that can easily operate
        """
        detail_account = account.get_detail_account_of_type(type_account, credit_card_num)
        return detail_account
    
    
class Account():
    """Class for each customer account entities"""
    
    def __init__(self, owner, account_id, bank = None):
        """Initialize a customer account
        
        Parameters
        ----------
        owner: str
            name of the account owner
        account_id: int
            unique identifer of the account
        bank: type(Bank)
            associate with Bank object

        Attributes
        ----------
        detail_accounts: list
            contain all the associated detail accounts (can only have 1 checking and 1 savings)
        has_checking/has_savings: bool
            check whether such detail accounts are created
        num_credit_account: int
        _bank: type(Bank)
            avoid direct operation on the bank instance
        """     
        self.owner = owner
        self.account_id = account_id
        self._bank = bank
        
        self.detail_accounts = []
        self.has_checking = False
        self.has_savings = False
        self.num_credit_account = 0

    def print_account_info(self):
        """Print out account information"""    
        print("The account with id {} is owned by {}.".format(self.account_id, self.owner))
        
    def summarize_account_balance(self):
        """Prnt out all account balances"""
        lst_accounts = self.detail_accounts #Get all associated accounts
        print("This account contain(s) {} account(s):".format(len(lst_accounts)))
            
        for account_index in range(0,len(lst_accounts)): #Print each of associated accounts with format
            detail_account = lst_accounts[account_index]
            print("\t" + detail_account.summarize_account_balance())
        
    def get_detail_account_of_type(self, type_account, credit_card_num = None):
        """Get the detail account with certain type under a customer account
        
        Parameters
        ----------
        type_account: str
            must contain character variants of ("checking", "savings", "credit")
        credit_card_num: int, optional
            16 digit credit_card_num if requesting credit account
            
        Return
        ------
        self.detail_accounts[index]: type(CheckingAccount), type(SavingsAccount), type(CreditAccount), None
            the detail account object that can easily operate
        """
        for index in range(0, len(self.detail_accounts)):
            
            if credit_card_num is None:
                if self.detail_accounts[index].type_account == type_account.lower():
                    return self.detail_accounts[index]  
                
            elif credit_card_num is not None:
                if ((self.detail_accounts[index].type_account == type_account.lower()) and 
                    (self.detail_accounts[index].credit_card_num == credit_card_num)):
                    return self.detail_accounts[index]
                
        return None
    
    def add_transaction(detail_account, date, description, amount, is_debit):
        """Create new transaction in a associated account
        
        Parameters
        ----------
        detail_account: type(CheckingAccount), type(SavingsAccount), type(CreditAccount)
            the associated account that will post the transaction
        date: type(datetime.date) or str
            transaction date
        description: str
        amount: int or float
        is_debit: bool
            in terms of accounting, indicating a subtraction (debit) or addition (credit) to balances. 
            CreditAccount will always be addition to balance
        """
        if amount <= 0:
            return None
        
        if isinstance(detail_account, (CheckingAccount, SavingsAccount)):
            if is_debit:
                amount = -amount
                
        elif isinstance(detail_account, CreditAccount):
            amount = abs(amount)
        
        new_transaction = Transaction(date, description, amount)
        detail_account.add_transaction(transaction)
        
        if is_real_account_in_bank(detail_account):
            detail_account._bank.processed_transaction_id.append(new_transaction.transaction_id)
   
    
class DetailAccount():
    """Base class for each associated accounts"""
    
    def __init__(self, account, bank = None):
        """Initialize a detail account
        
        Parameters
        ----------
        account: type(Account)
            associated customer account
        bank: type(Bank)
            associate with Bank object

        Attributes
        ----------
        balance: int or float
            remaining balance in the account. Starting with 0.
        statement: list
            list of transactions
        _bank: type(Bank)
            avoid direct operation on the bank instance
        """     
        self.account = account
        self.balance = 0
        self.statement = []
        self._bank = bank
        
    def add_transaction(self, transaction):
        """Add transaction to this account
        
        Parameters
        ----------
        transaction: type(transaction)
            object containing date, transaction_id, description, and amount
        """
        if is_real_account_in_bank(self.account):
            self._bank.processed_transaction_id.append(transaction.transaction_id)
        else:
            Transaction.used_transaction_id.remove(transaction.transaction_id)
            del transaction
            return None
            
        if self.balance + transaction.amount >= 0:
            self.statement.append(transaction)
            self.balance = self.balance + transaction.amount
            
        else:
            print("ERROR: Insufficient fund in account.")
            self._bank.processed_transaction_id.remove(transaction.transaction_id)
            Transaction.used_transaction_id.remove(transaction.transaction_id)
            del transaction   
            
    def transfer_to_account(self, account, transaction):
        """
        Reduce money from this account instance and add money in another account 
        (or pay off balance in CreditAccount)
        
        Parameters
        ----------
        account: type(CheckingAccount), type(SavingsAccount), type(CreditAccount)
            the account that will receive money (or reduce balance in CreditAccount)
        transaction: type(transaction)
            transaction of reducing money
        """
        if transaction.amount >= 0:
            return None
        
        if not isinstance(account, DetailAccount):
            return None
        
        self.add_transaction(transaction)
        if isinstance(account, (CheckingAccount, SavingsAccount)):
            receiving_transaction = Transaction(transaction.date, transaction.description, -transaction.amount)
            Transaction.used_transaction_id.remove(receiving_transaction.transaction_id)
            receiving_transaction.transaction_id = transaction.transaction_id
            account.add_transaction(receiving_transaction)
            
        elif isinstance(account, CreditAccount):
            account.add_transaction(transaction)
            
    def summarize_account_balance(self):
        """Print out account balance"""
        return "This {} account has available balance:\t{}".format(self.type_account, self.balance)
    
    def print_statement(self):
        """Pretty print out statement"""
        for item in self.statement:
            print("{}:\n{}\t{}\t${:,.2f}".format(
                str(item.date), item.transaction_id, item.description, item.amount))
    
    
class CheckingAccount(DetailAccount):
    """Class for each checking account entities"""
    
    def __init__(self, account, starting_amount, bank = None):
        """Initialize a checking account inherited from DetailAccount
        
        Parameters
        ----------
        account: type(Account)
            associated customer account
        starting_amount: int or float
            initial deposit amount
        bank: type(Bank)
            associate with Bank object
            
        Attributes
        ----------
        inherit from DetailAccount
            balance: int or float
                remaining balance in the account. Starting with 0.
            statement: list
                list of transactions
            _bank: type(Bank)
                avoid direct operation on the bank instance
        """ 
        super().__init__(account, bank)
            
        if starting_amount > 0:
            new_transaction = Transaction(date.today(), "Initial Deposit", starting_amount)
            self.add_transaction(new_transaction)
        
        self.type_account = "checking"
        self.is_checking_account = True
        
        
class SavingsAccount(DetailAccount):
    """Class for each savings account entities"""
    
    def __init__(self, account, starting_amount, bank = None):
        """Initialize a checking account inherited from DetailAccount
        
        Parameters
        ----------
        account: type(Account)
            associated customer account
        starting_amount: int or float
            initial deposit amount
        bank: type(Bank)
            associate with Bank object
        
        Attributes
        ----------
        inherit from DetailAccount
            balance: int or float
                remaining balance in the account. Starting with 0.
            statement: list
                list of transactions
            _bank: type(Bank)
                avoid direct operation on the bank instance
        """
        super().__init__(account, bank)
        
        if starting_amount > 0:
            new_transaction = Transaction(date.today(), "Initial Deposit", starting_amount)
            self.add_transaction(new_transaction)
            
        self.type_account = "savings"
        self.is_savings_account = True
    
    
class CreditAccount(DetailAccount):
    """Class for each credit account entities"""
    
    def __init__(self, account, credit_card_num, credit_limit, bank = None):
        """Initialize a checking account inherited from DetailAccount
        
        Parameters
        ----------
        account: type(Account)
            associated customer account
        credit_card_num: str
            associated credit card
        credit_limit: int or float
            initial maximum balance allowed
        bank: type(Bank)
            associate with Bank object
        
        Attributes
        ----------
        inherit from DetailAccount
            balance: int or float
                remaining outstanding balance in the account. Starting with 0.
            statement: list
                list of transactions
            _bank: type(Bank)
                avoid direct operation on the bank instance
        """
        super().__init__(account, bank)
        
        self.credit_card_num = credit_card_num
        self.credit_limit = credit_limit
        
        self.type_account = "credit"
        self.is_credit_account = True
        
    def summarize_account_balance(self):
        """Overwrite base summarize_account_balance method since CreditAccount needs more info"""
        return "This credit account({}) has outstanding balance with limit:\t{}/{}".format(
            self.credit_card_num, self.balance, self.credit_limit)
    
    def add_transaction(self, transaction):
        """Overwrite base add_transaction to add transaction to this account
        
        Parameters
        ----------
        transaction: type(transaction)
            object containing date, transaction_id, description, and amount
        """
        if is_real_account_in_bank(self):
            self._bank.processed_transaction_id.append(transaction.transaction_id)
        else:
            Transaction.used_transaction_id.remove(transaction.transaction_id)
            del transaction 
            return None
            
        if self.balance + transaction.amount <= self.credit_limit:
            self.statement.append(transaction)
            self.balance = self.balance + transaction.amount
            
        else:
            print("ERROR: Insufficient credit in account.")
            self._bank.processed_transaction_id.remove(transaction.transaction_id)
            Transaction.used_transaction_id.remove(transaction.transaction_id)
            del transaction
                
    def transfer_to_account(self, account, transaction):
        """Overwrite base transfer_to_account to not allow behavior"""
        raise NotImplementedError("You cannot transfer debt from credit account!")
    
class Transaction():
    """Class for all transactions performed
    
    Attribute
    ---------
    used_transaction_id: list
        list of all transactions performed (valid or invalid)
    """
    used_transaction_id = []
    def __init__(self, date, description, amount):
        """ Initialize a transaction
        
        Parameters
        ----------
        date: type(datetime.date) or str
            transaction date
        description: str
        amount: int or float
        
        Attribute
        ---------
        transaction_id: int
            random id generated at creation
        """
        self.date = date
        self.transaction_id = Transaction.generate_id()
        self.description = description
        self.amount = amount
     
    @classmethod
    def generate_id(cls):
        """Generate random transaction id and add to used id
        
        Return
        ------
        new_transaction_id: int
            random generated transaction id
        """
        new_transaction_id = random.randint(10 ** 10, 10 ** 11 - 1)
        while new_transaction_id in Transaction.used_transaction_id:
            new_transaction_id = random.randint(10 ** 10, 10 ** 11 -1)
            
        Transaction.used_transaction_id.append(new_transaction_id)
        
        return new_transaction_id

    
def is_real_account_in_bank(account):
    """Check if such account is real
    
    Parameter
    ---------
    account: type(Account), type(CheckingAccount), type(SavingsAccount), type(CreditAccount):
        account to check if it exists in the associated bank
    
    Return
    ------
    True/False
    """
    if account._bank is None or not isinstance(account._bank, Bank):
        return False
        
    if isinstance(account, Account):
        
        if account in account._bank.accounts.values():
            return True
        else:
            return False
        
    elif isinstance(account, DetailAccount):
        
        if account in account._bank.all_detail_accounts:
            return True
        else:
            return False