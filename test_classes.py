"""Test for classes created

"""
from classes import *

ABCBank = Bank("ABC", "9450 Nobel Dr", "08:00", "20:00")
new_account = ABCBank.open_accounts("Test")

def test_open_accounts():
    
    assert new_account in ABCBank.accounts.values()
    assert isinstance(new_account, Account)
    assert new_account.owner == "Test"
    
def test_add_accounts():
    
    ABCBank.add_accounts(new_account, ['CHECKING', 'sAvIngs', 'Credit'], [191.1, 1175])
    assert len(ABCBank.all_detail_accounts) == 3
    assert len(Bank.used_credit_card_num_lst) == 1
    assert ABCBank.all_detail_accounts[2].credit_limit == 100
    