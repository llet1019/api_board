## Community Board API
- 카테고리가 있는 게시판 만들기

## 기본 기능
#### user 관련 기능 
- user 관련 api 는 jwt 토큰을 이용한다.
#### board 관련 기능
- board 는 작성자만 수정, 삭제가 가능하다. 
- 생성, 조회는 모두가 가능하다.

## API 명세서
| API 기능 | API URL | METHOD |
|-----|---------|-----|
| 회원가입 | /accounts/user/signup/ | POST |
| 로그인 | /accounts/user/login/ | POST |
| 로그아웃 | /accounts/user/logout | DELETE |
| 개인정보 조회 | /accounts/user/info/ | GET |
| 게시물 생성 | /board/ | POST |
| 게시물 조회 | /board/{board_id}/ | GET |
| 게시물 수정 | /board/{board_id}/ | PATCH |
| 게시물 삭제 | /board/{board_id}/ | DELETE |
| 게시물 목록 조회 | /category/{category_id}/board/ | GET |
