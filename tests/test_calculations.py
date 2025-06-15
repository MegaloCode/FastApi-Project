import pytest
from app.calculations import add , subtract , multiply , divide , BankAccount , InsufficientFunds

@pytest.fixture # function that run before a specfic test case 
def zero_bank_account():
    print("creating my bank account")
    return BankAccount() # bank_account with initial value of zero 0



@pytest.fixture
def bank_account():
    return BankAccount(50) # here we set the initial to 50



@pytest.mark.parametrize("num1 , num2 , expected", [(3 , 4 , 7),(1 , 5 , 6),(12 , 4 , 16)])
def test_add(num1 , num2 , expected): # the --name-- of the test should begin with ==> test_
    print("==>testing add function<==") # to print this statement in the pytest ==> pytest -v -s
    assert add(num1 , num2) == expected



# def test_add(): # the --name-- of the test should begin with ==> test_

#     print("==>testing add function<==") # to print this statement in the pytest ==> pytest -v -s

#     assert add(3 , 5) == 8



def test_subtract():
    assert subtract(9 , 5) == 4



def test_multiply():
    assert multiply(3 , 5) == 15



def test_divide():
    assert divide(10 , 2) == 5



##############################################################################



def test_bank_set_initial_amount(bank_account): # here bank_account is fixture variable not instance of the class
    assert bank_account.balance == 50



def test_bank_default_amount(zero_bank_account):
    print("testin my bank account")
    assert zero_bank_account.balance == 0



def test_withdraw():
    bank_account = BankAccount(50)
    bank_account.withdraw(20)
    assert bank_account.balance == 30



def test_deposit():
    bank_account = BankAccount(50)
    bank_account.deposit(20)
    assert bank_account.balance == 70



def test_collecting_interest():
    bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance , 6) == 55 # use round function to nearest integer number



@pytest.mark.parametrize("deposited , withdrew , expected", [(200 , 100 , 100),(50 , 10 , 40),(1200 , 200 , 1000)])
def test_bank_transaction(zero_bank_account , deposited , withdrew , expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected



def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
