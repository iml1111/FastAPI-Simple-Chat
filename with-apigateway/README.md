# FastAPI-Simple-Chat
본 예제는 Webscoket API Gateway와 연동하여 Chat App을 구현한 예제입니다.

# Get started
```shell
// 환경 변수 설정 필요
export AWS_ACCESS_KEY_ID=XXX...
export AWS_SECRET_ACCESS_KEY=XXX...
export API_GATEWAY_ENDPOINT=https://{API-ID}.execute-api.{REGION}.amazonaws.com/{STAGE}

pip install -r requirements.txt
uvicorn main:app --reload
```
샘플 코드에 대한 자세한 설명은 [여기](https://blog.naver.com/shino1025/222898722779)에서 확인하실 수 있습니다.
