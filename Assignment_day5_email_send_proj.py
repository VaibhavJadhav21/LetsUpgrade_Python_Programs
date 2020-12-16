def sendMail(email, name):
    
    html_text = '''<p><span style="font-family: Courier New, courier;"><span style="background-color: rgb(247, 218, 100);">HEY Rowdy,'''+ name+'''</span>&nbsp;</span></p>
                <p><span style="font-family: Courier New, courier;"><br></span></p>
                <p><span style="font-family: Courier New, courier;">How are you this is SAIKIRAN FROM LEtsUpgrade,&nbsp;</span></p>
                <p><span style="font-family: Courier New, courier;">Cheif Rowdy at LU !!</span></p>
                <p><span style="font-family: Courier New, courier;">Love teaching you all, hope you like this project&nbsp;</span></p>
                <p><span style="font-family: Courier New, courier;"><br></span></p>
                <p><span style="font-family: Courier New, courier;">Regards,&nbsp;</span></p>
                <p><strong><span style="font-family: Courier New, courier;">Cheif Rowdy,</span></strong></p>
                <p><span style="font-family: Courier New, courier;"><strong>Saikiran Sondarkar</strong></span></p>'''

    subject = "Hey Rowdy "+ name + ", you have EMAIL FROM LetsUpgrade"
    message = emails.html(html=html_text,
                          subject=subject,
                          mail_from=('Rowdy LetsUpgrade', 'sai@xyz.com'))

    
    mail_via_python = message.send(to=email, 
                               smtp={'host': 'smtp.gmail.com', 
                                     'timeout': 5,
                                    'port':587,
                                    'user':'YOUREMAIL@REQUIRED>COM',
                                    'password':'YourPassWordREquired',
                                    'tls':True})
    return mail_via_python.status_code
sendMail("abc@gmail.com","SaiKiran")
