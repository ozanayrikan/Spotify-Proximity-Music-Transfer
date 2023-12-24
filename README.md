# Spotify Proximity Music Transfer

![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)

This FastAPI application facilitates automatic music transfer between a laptop and a phone using Spotify playback.

Proximity-Based Automatic Spotify Music Synchronization Between Computer and Phone


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [FAQ](#frequently-asked-questions)

## Installation

Follow these steps to install project dependencies:

1. Clone the repository:

    ```bash
    git clone https://github.com/ozanayrikan/Spotify-Proximity-Music-Transfer
    cd Spotify-Proximity-Music-Transfer
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
3. Set up environment variables:
         

    ```bash
    mv .env.example .env
    ```

    ```bash
   | Variable                        | Value                                     |
   |---------------------------------|-------------------------------------------|
   | BASE_URL                        | 'https://api.spotify.com/v1/'             |
   | CLIENT_ID                       | your_client_id                            |
   | CLIENT_SECRET                   | your_client_secret                        |
   | REDIRECT_URI                    | 'http://localhost:4444/callback'          |
   | TARGET_DEVICE_BLUETOOTH_ADDRESS | example: '00:00:00:00:00:00'              |
   | SCAN_INTERVAL                   | 3                                         |
   ```

   **Note:** Before proceeding, make sure to obtain your free Spotify API credentials from the [Spotify Developer Dashboard](https://developer.spotify.com/), and set them up in the `.env` file.







## Usage
Run the following command to start the FastAPI application:

    uvicorn main:app --reload --host 0.0.0.0 --port 4444

To start the application:

1. Open your browser and go to [http://localhost:4444](http://localhost:4444).
2. Log in to Spotify, and the application will automatically initiate a background task to continuously scan for Bluetooth devices and transfer playback based on signal strength.
3. You will experience seamless music transfer between your laptop and your phone.

Please note:

- The music transfer functionality is designed to work specifically between a laptop and a phone through Spotify playback.
- The application supports low-energy Bluetooth devices, such as a smartwatch, connected to the laptop as a Bluetooth device.

## Frequently Asked Questions

**Q: The project is not running, what should I do?**
A: First, make sure the dependencies are installed correctly. Also, ensure that your Spotify API keys are correct, and you have configured your Spotify application correctly.

**Q: Why is Bluetooth scanning not working?**
A: Ensure that the Bluetooth feature on your computer is turned on. This project utilizes low-level Bluetooth connectivity, and an external Bluetooth dongle is not required on laptops. We have successfully tested and run the project on Windows, using a variety of Bluetooth-enabled devices, including smartwatches, as examples of low-level Bluetooth connections. Please note that the functionality may vary, and the Bluetooth feature on some smartphones may not be fully compatible. Important: This functionality may not work reliably on smartphones.

### Q: I started Uvicorn, but I can't terminate it. What should I do?

If you are having trouble closing Uvicorn on Windows, you can use the Task Manager to terminate the process. Follow these steps:

1. **Open Task Manager:**
   - Right-click on the taskbar at the bottom right, or press Ctrl + Shift + Esc to open the Task Manager.

2. **Switch to the Details Tab:**
   - In the Task Manager window, switch to the "Details" tab.

3. **Locate Uvicorn:**
   - Find the Python application or process running Uvicorn. You can use the search among the names.

4. **Terminate Uvicorn Process:**
   - Once you locate the Uvicorn process, right-click on it and choose "End Task" to terminate it.

This should help you close Uvicorn when needed.