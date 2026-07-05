import concurrent.futures, random, requests

url = "https://gql.twitch.tv/gql"

def load_tokens(path):
    with open(path, "r") as f:
        return [l.strip() for l in f if l.strip()]

def send_join(session, raid_id, tokens):
    token = random.choice(tokens)
    if "|" in token:
        token = token.split("|", 1)[1].strip()
    
    headers = {
        "Authorization": "OAuth " + token,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Host": "gql.twitch.tv",
    }
    
    payload = [{
        "operationName": "JoinRaid",
        "variables": {"input": {"raidID": raid_id}},
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "c6a332a86d1087fbbb1a8623aa01bd1313d2386e7c63be60fdb2d1901f01a4ae"
            }
        }
    }]
    
    try:
        r = session.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code == 200
    except:
        return False

def main():
    raid_id = input("raid id ")
    amount = int(input("joins?"))
    tokens = load_tokens("tokens.txt")
    
    session = requests.Session()
    success = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as e:
        futures = [e.submit(send_join, session, raid_id, tokens) for _ in range(amount)]
        for f in concurrent.futures.as_completed(futures):
            if f.result():
                success += 1
    
    print(f"done {success}/{amount}")

if __name__ == "__main__":
    main()
