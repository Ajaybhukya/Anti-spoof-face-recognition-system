import smtplib
from datetime import date
def send_email(id,name,to_mail):
    mymail = ''
    password = ''  # Replace with your app password
    subject="Avanthi Attendance Management System"
    content=f"Hello ID: {id} Name: {name.title()} ! \n Today({date.today()}) Attendance Marked Sucessful"
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(mymail, password)
        mail_content = f"Subject: {subject}\n\n {content}"
        s.sendmail(mymail, to_mail, mail_content)
        s.quit()
    except Exception as e:
        print(f"Error sending email: {e}")
# send_email("1234","sai","projectface1213@gmail.com")
# print("Email sent successfully!")