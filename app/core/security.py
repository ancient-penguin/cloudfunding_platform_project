from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 1. 비밀번호 검증 함수 (로그인 할 때 사용)
# plain_password: 사용자가 입력한 비번
# hashed_password: DB에 저장된 괴문자
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 2. 비밀번호 암호화 함수 (회원가입 할 때 사용)
def get_password_hash(password):
    return pwd_context.hash(password)