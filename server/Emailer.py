import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Emailing:
   def __init__(self, sending_email, email_password):
      self.sending_email = sending_email
      self.password = email_password
      self.smtp_host = 'smtp.gmail.com'
      self.smtp_port = 587

   def _create_html_content(self, subject, content):
      """
      Creates a MIMEText object with the HTML content for the email.
      """
      msg = MIMEMultipart()
      msg['From'] = self.sending_email
      msg['Subject'] = subject
      msg.attach(MIMEText(content, 'html'))
      return msg

   def _send_email(self, msg, recipient_email):
      """
      Sends the email message to the specified recipient.
      """
      try:
         with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
               server.starttls()  # Secure connection
               server.login(self.sending_email, self.password)
               server.sendmail(self.sending_email, recipient_email, msg.as_string())
               print(f"Email sent to {recipient_email}")
      except Exception as e:
         print(f"Error sending email: {e}")

   def send_alert_email(self, name, gpa, program, student_email):
      """
      Sends an alert email to the student whose GPA falls below the threshold.
      """
      subject = f"Alert: GPA Below Expected Threshold for {name}"
      content = f"""
      <html>
      <body>
         <p>Dear {name},</p>
         <p>We regret to inform you that your current GPA of {gpa} is below the expected standard for your program. We recommend that you take the following actions:</p>
         <ul>
               <li>Review your academic performance.</li>
               <li>Reach out to your academic advisor at <a href="mailto:{self.sending_email}">{self.sending_email}</a> for guidance.</li>
         </ul>
         <p>Program: {program}</p>
         <p>If you have any concerns, feel free to contact your advisor.</p>
         <br>
         <p>Best regards,</p>
         <p>Your Program Team</p>
      </body>
      </html>
      """
      msg = self._create_html_content(subject, content)
      self._send_email(msg, student_email)

   def send_account_creation_email(self, user_email, user_first_name, user_id):
      """
      Sends an account creation email with the user ID and next steps.
      """
      subject = "Account Created – Your ID Number and Next Steps"
      content = f"""
      <html>
      <body>
         <p>Dear {user_first_name},</p>
         <p>We are excited to inform you that an account has been successfully created for you!</p> 
         <p>To get started, please use the unique ID number below to verify your identity and set up your account password.</p>
         <p><b>Your ID Number:</b> {user_id}</p>
         <p>Follow these steps to complete your registration:</p>
         <ol>
               <li>Visit our <a href="http://example.com/verification">account verification page</a> and enter your ID number.</li>
               <li>Create a secure password for your account.</li>
               <li>Confirm your details and finalize your registration.</li>
         </ol>
         <p>If you have any issues or need further assistance, feel free to reach out to our support team at <a href="mailto:studentscalaborators@gmail.com">studentscalaborators@gmail.com</a>.</p>
         <p>Thank you for choosing Our Company. We look forward to having you on board!</p>
         <br>
         <p>Best regards,</p>
         <p>Student Collaborators from UTECH</p>
      </body>
      </html>
      """
      msg = self._create_html_content(subject, content)
      self._send_email(msg, user_email)


