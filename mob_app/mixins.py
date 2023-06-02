from twilio.rest import Client 

def send_otp_on_phone(phone,otp):
    client = Client('ACf14eb9b19ddc296b2bf57b975eaaab71','68587452f999d3b22eec4f6edcd99c90')
    message = client.messages \
                    .create(
                        body=f'Your otp is {otp}',
                        
                        from_='+13156311410',
                        to= phone
                        
                    )
    print('otp send to')

