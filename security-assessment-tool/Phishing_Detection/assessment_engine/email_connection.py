import csv
import imaplib
import email
from email.header import decode_header, make_header
from bs4 import BeautifulSoup


def collect_emails_and_scrape_urls(username, password, mailbox):
    # Connect to the mailbox
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    print("Logged into gmail provider")
    mail.select(mailbox)

    # Search for all emails in the mailbox
    _, search_data = mail.search(None, 'ALL')
    email_ids = search_data[0].split()
    print("Searching through mailbox")
    # Loop through all email IDs and extract the href URLs
    href_urls = []
    for email_id in email_ids:
        # Retrieve the email and parse the HTML content
        _, data = mail.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        try:
            subject = str(make_header(decode_header(email_message.__getitem__("subject"))))
        except:
            subject = "failed to get"
        try:
            sender = str(make_header(decode_header(email_message['From'])))
        except:
            sender = "failed to get"
        for part in email_message.walk():
            if part.get_content_type() == "text/html":
                # body = part.get_payload(decode=True).decode("utf-8")
                body = part.get_payload(decode=True)
            else:
                continue
        if body == "":
            continue
        # Use BeautifulSoup to parse the HTML content and extract all href URLs
        soup = BeautifulSoup(body, 'html.parser')

        # Find first a tag and get url out of it
        link = soup.find('a')
        try:
            url = [email_id, sender, subject, link.get('href')]
            header = ['email-id', 'sender', 'subject', 'url']
            href_urls.append(url)
            print("Found url: " + url[3])
            with open("Phishing_detection/assessment_engine/scrape_urls.csv", "w", newline='',
                      encoding="utf-8") as scrape_csv:
                csvwriter = csv.writer(scrape_csv, delimiter=',')
                csvwriter.writerow(header)
                csvwriter.writerows(href_urls)
        except:
            pass
    # Disconnect from the mailbox and return the list of href URLs
    mail.close()
    mail.logout()
    print("Finished scraping urls in mailbox!")
    # with open("Phishing_detection/assessment_engine/scrape_urls.csv", "w", newline='', encoding="utf-8") as scrape_csv:
    #     csvwriter = csv.writer(scrape_csv, delimiter=',')
    #     csvwriter.writerows(href_urls)

# if __name__ == '__main__':
#     username = 'lars.de.loenen@gmail.com'
#     password = 'diiwazblxakjnads'
#     mailbox = '[Gmail]/Spam'
#     href_urls = collect_emails_and_scrape_urls(username, password, mailbox)
#     print(href_urls)
