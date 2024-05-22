# pip install pytest
# test directory 지정
# test_ ~ .py 이름
# test_ 함수이름 

def test_equal_or_not_equal():
    assert 3 == 3
    # assert 3 == 2

def test_check():
    assert 3 != 2
    # assert 3 == 2

def test_is_instance():
    # assert isinstance('this is string',int)
    assert isinstance('this is string',str)

def test_boolean():
    validated = True
    assert validated is True

def test_type():
    # assert type('Hello') is str
    assert type('Hello' is str)

def test_list():
    num = [1,2,3,4]
    any = [False, False]
    
    assert all(num)
    assert not all(any)


# 인스턴스 고정해서 테스트 하기
import pytest

class Student:
    def __init__(self,
                 first_name : str,
                 last_name : str,
                 major : str,
                 years : str):
        
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

# 이렇게 해도 되지만 p 객체를 매번 생성하지 않고 고정시킬 수 있음
# def test_person_initialization():
#     p = Student('Jungmin','Lim','Coding',3)
#     assert p.first_name == 'Jungmin', 'First name should be Jungmin'
#     assert p.last_name == 'Lim', 'Last name should be Lim'
#     assert p.major == 'Coding'
#     assert p.years == 3
    # assert p.years == 4

# 인스턴스 고정
@pytest.fixture
def default_employee():
    return Student('Jungmin','Lim','Coding',3)

def test_person_initialization2(default_employee):
    assert default_employee.first_name == 'Jungmin', 'First name should be Jungmin'
    assert default_employee.last_name == 'Lim', 'Last name should be Lim'
    assert default_employee.major == 'Coding' # AssertionError 메모는 선택 사항
    assert default_employee.years == 3
