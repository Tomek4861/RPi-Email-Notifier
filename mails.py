import time

from simplegmail import Gmail


class MailManager:
    """Class to manage email checking"""
    def __init__(self):
        self.gmail = Gmail()
        self.emails = self.gmail.get_unread_messages()[:5]

    def check_for_new_emails(self):

        previous_emails = self.emails
        self.emails = self.gmail.get_unread_messages()[:5]

        previous_ids = [email.thread_id for email in previous_emails]
        new_emails = [email for email in self.emails if email.thread_id not in previous_ids]

        if new_emails:
            print("New emails found!", new_emails)

        return new_emails

    @property
    def email_count(self):
        return len(self.emails)


# mm = MailManager()
# while True:
#     print(mm.check_for_new_emails())
#     time.sleep(10)
