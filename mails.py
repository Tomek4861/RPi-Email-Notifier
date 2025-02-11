from simplegmail import Gmail


class MailManager:
    """Class to manage email checking"""

    def __init__(self, fetched_emails_count=5):
        self.gmail = Gmail()
        self.fetched_emails_count = fetched_emails_count
        self.emails = self.gmail.get_unread_messages()[:self.fetched_emails_count]

    def check_for_new_emails(self):
        previous_emails = self.emails.copy()  # just in case
        self.emails = self.gmail.get_unread_messages()[:self.fetched_emails_count]

        previous_ids = [email.thread_id for email in previous_emails]
        new_emails = [email for email in self.emails if email.thread_id not in previous_ids]

        if new_emails:
            print("New emails found!", new_emails)

        return new_emails

    @property
    def unread_email_count(self):
        return len(self.emails)

