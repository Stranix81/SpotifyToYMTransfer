from SpotifyToYMTransfer.transfer import get_token_spotify, get_token_ym, transfer_playlists
import asyncio

def main():
    client_id = "your_client_id"
    redirect_url = "http://127.0.0.1/"
    scopes = "user-library-read, playlist-read-private"

    num_accounts = int(input("How many account pairs? "))

    spotify_tokens = []
    ym_tokens = []

    # getting tokens
    for _ in range(num_accounts):
        spotify_tokens.append(get_token_spotify(client_id, redirect_url, scopes))
        ym_tokens.append(get_token_ym())
    
    # run transfer
    asyncio.run(transfer_playlists(spotify_tokens, ym_tokens))

if __name__ == '__main__':
    main()
