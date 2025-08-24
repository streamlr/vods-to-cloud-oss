# VODs To Cloud Open-Source

Upload your VODs to the cloud using this open-source solution. Self-hosted and customizable to fit your needs.

If you aren't a developer and need help with the setup, we'll offer paid support options in the future.

Project by _Streamlr_ and [diegodev18](https://diego18.pro)

## Get Started

1. Clone the repository

    ```bash
    git clone https://github.com/streamlr/vods-to-cloud-oss
    cd vods-to-cloud-oss
    ```

2. Create an Python virtual environment

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Set up your Twitch application and obtain the necessary credentials at [Twitch Developer Console](https://dev.twitch.tv/console/apps).

4. Configure the environment variables

    ```bash
    export TWITCH_CLIENT_ID=your_client_id
    export TWITCH_CLIENT_SECRET=your_client_secret
    export TWITCH_REDIRECT_URI=your_redirect_uri
    ```

    or configure your environment variables in the dockerfile file.

5. Create the project container

    ```bash
    docker build -t vods-to-cloud-oss .
    ```

6. Run the application

    ```bash
    docker run vods-to-cloud-oss -p 5000:8080
    ```

> This project is in development, so the documentation is not complete.

## Features

- [x] Get VODs
- [ ] VODs download

Types to save vods to add:

- [ ] S3 storage support
- [ ] Backblaze storage support
- [ ] YouTube upload support
- [ ] Local storage support
