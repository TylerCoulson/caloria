from app.auth.email.email import fm, send_email, EmailSchema
from email.parser import BytesParser
import base64

async def test_send_msg(client):
    fm.config.SUPPRESS_SEND = 1
    fm.config.MAIL_FROM = "your@email.com"
    with fm.record_messages() as outbox:
        payload = {"email": "user@example.com"}
        response = await send_email(email=EmailSchema(**payload), request=None, )
        # print(outbox[0])
        # test = BytesParser().parsebytes(outbox[0].get_payload().as_bytes())
        # b = test.get_payload()
        # by = base64.b64decode(b)
        # print(by.decode("utf-8"))
        
        assert response.body == b'{"message":"email has been sent"}'
        assert len(outbox) == 1
        assert outbox[0]['from'] == "your@email.com"
        assert outbox[0]['To'] == "user@example.com"
        

async def test_verification(client, user):
    fm.config.SUPPRESS_SEND = 1
    fm.config.MAIL_FROM = "your@email.com"

    with fm.record_messages() as outbox:
        
        response = await client.post(f"/api/v1/auth/request-verify-token", json={"email":user.email})
        
        body = base64.b64decode(
                BytesParser().parsebytes(
                    outbox[0].get_payload()[0].as_bytes()
                ).get_payload()
            ).decode("utf-8") 
        print("email", body)

        assert response.status_code == 202
        assert len(outbox) == 1
        assert outbox[0]['from'] == "your@email.com"
        assert outbox[0]['To'] == user.email
        assert outbox[0]['subject'] == "Verify Account"
        assert body.find("http://test/verify?token=") != -1
        


async def test_forgotten_password(client, user):
    fm.config.SUPPRESS_SEND = 1
    fm.config.MAIL_FROM = "your@email.com"
    with fm.record_messages() as outbox:
        response = await client.post(f"/api/v1/auth/forgot-password", json={"email":user.email})
        
        body = base64.b64decode(
                BytesParser().parsebytes(
                    outbox[0].get_payload()[0].as_bytes()
                ).get_payload()
            ).decode("utf-8") 
        print('email', body)
        assert response.status_code == 202
        assert len(outbox) == 1
        assert outbox[0]['from'] == "your@email.com"
        assert outbox[0]['To'] == user.email
        assert outbox[0]['subject'] == "Forgot Password"
        assert body.find("http://test/reset-password?token=") != -1