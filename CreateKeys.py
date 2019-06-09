from mastodon import Mastodon

name = 'クライアント名'
url = 'インスタンスのURL'
mail = 'メールアドレス'
pw = 'パスワード'

Mastodon.create_app(
     name,
     api_base_url = url,
     to_file = 'app_key.txt'
)

mastodon = Mastodon(
    client_id = 'app_key.txt',
    api_base_url = url
)
mastodon.log_in(
    mail,
    pw,
    to_file = 'user_key.txt'
)

