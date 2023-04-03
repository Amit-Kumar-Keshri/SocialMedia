import pytest
from app.calculations import add, BankAccount

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)




@pytest.mark.parametrize("x,y,z",[
    (1,2,3),
    (2,5,7),
    (56,52,108)
])
def test_add(x,y,z):
    print("testing the add function")
    
    assert add(x, y) == z
    
    
def test_bank_acc_balance(zero_bank_account):
    
    assert zero_bank_account.bal == 0 
    
    
def test_withdraw(bank_account):
    bank_account.withdraw(19)
    assert bank_account.bal == 31
    

def test_deposit(bank_account):
    bank_account.deposit(19)
    assert bank_account.bal == 69
    

def test_interest(bank_account):
    
    bank_account.interest()
    assert round(bank_account.bal,6) == 55
    

@pytest.mark.parametrize("x,y,z", [
    (20, 30, -10),
    (2, 5, -3),
    (500, 400, 100)
])
def test_bank_trans(zero_bank_account,x,y,z):
    zero_bank_account.deposit(x)
    zero_bank_account.withdraw(y)
    assert zero_bank_account.bal == z

    