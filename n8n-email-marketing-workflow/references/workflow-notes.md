See: ~/Desktop/SMThelp_Data/CRM_Import/S70LD_Email_Marketing_Workflow.json
(Generated via n8n API: POST https://n8n.autoinsertion.com/api/v1/workflows)

Workflow nodes (11 total):
1. Schedule Trigger: every 3 days
2. Read Contact CSV: ~/Desktop/SMThelp_Data/CRM_Import/Mautic_Import_S70LD_Contacts.csv
3. Split In Batches: batch size 50
4. Email Subject (IF) node: country-based subject line logic
5. Switch Node: round-robin routing (sale→service→info→support→smthelp→sale)
6-10. Five Send Email nodes (one per sender)
11. Wait + Follow-up: 7 days later, same sender
12. Set node: mark contact as "emails_sent"

Each Send Email node needs SMTP credential manually bound in n8n UI.
