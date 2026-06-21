from app import app
c = app.test_client()
with c.session_transaction() as sess:
    sess['user_id'] = 1
    sess['username'] = 'test'
    sess['avatar'] = 'T'
r = c.get('/dashboard')
html = r.data.decode('utf-8', 'ignore')
print('STATUS:', r.status_code)
print('chat-fab in HTML:', 'chat-fab' in html)
print('chat-window in HTML:', 'chat-window' in html)
print('chatToggle in HTML:', 'chatToggle' in html)
# print snippet around chat-fab
idx = html.find('chat-fab')
if idx > 0:
    print('SNIPPET:', html[idx-20:idx+100])
