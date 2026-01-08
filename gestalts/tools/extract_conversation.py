from json import load

roles = {
  "User": "Rick",
  "AI Partner": "Aiko"
}

def valid_message(msg):
  if not 'create_time' in msg or msg['create_time'] is None: return False
  if not 'role' in msg or msg['role'] not in roles: return False
  if  not 'flattened' in msg or msg['flattened'] is None or len(msg['flattened'].strip()) == 0: return False
  return True


with open('/workspaces/home/tmp/conversation.json', 'r') as f:
  conversation = load(f)
messages = [msg for msg in conversation["messages"] if valid_message(msg)]
messages.sort(key=lambda m: m.get("create_time", 0))
with open('/workspaces/home/tmp/conversation.txt', 'w') as f:
  i  = 1
  for message in messages:
    name = roles.get(message["role"])
    text = message["flattened"].strip()
    time = message["timestamp"]
    f.write(f'[{i:05d}]{name}({time}): {text}\n\n')
    i = i + 1
