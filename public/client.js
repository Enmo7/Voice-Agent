// Define DOM elements
const connectButton = document.getElementById('connect-button');
const statusText = document.getElementById('status-text');
const statusDot = document.getElementById('status-dot');
const visualizer = document.getElementById('visualizer');

let room;

connectButton.addEventListener('click', async () => {
    if (room && room.state === 'connected') {
        await room.disconnect();
        return;
    }
    await connectToRoom();
});

async function connectToRoom() {
    try {
        connectButton.disabled = true;
        statusText.innerText = "Connecting...";

        // 1. Request a token from our Python backend
        const response = await fetch('/getToken');
        const data = await response.json();

        if (!data.token) throw new Error("Failed to get token");

        // 2. Initialize the LiveKit Room
        room = new LivekitClient.Room({
            adaptiveStream: true,
            dynacast: true,
        });

        // 3. Handle incoming audio tracks (The Agent's voice)
        room.on(LivekitClient.RoomEvent.TrackSubscribed, (track, publication, participant) => {
            if (track.kind === 'audio') {
                // Attach the audio track to the DOM to hear the agent
                track.attach();
                visualizer.classList.add('active'); // Start the visualizer animation
            }
        });

        // Handle disconnection
        room.on(LivekitClient.RoomEvent.Disconnected, () => {
            updateUI(false);
        });

        // 4. Connect to the LiveKit server
        await room.connect(data.url, data.token);
        
        // 5. Enable the user's microphone
        await room.localParticipant.setMicrophoneEnabled(true);

        updateUI(true);

    } catch (error) {
        console.error("Error connecting:", error);
        statusText.innerText = "Error: " + error.message;
        connectButton.disabled = false;
    }
}

function updateUI(isConnected) {
    if (isConnected) {
        statusText.innerText = "Connected (Listening...)";
        connectButton.innerText = "Disconnect";
        connectButton.disabled = false;
        statusDot.classList.add('connected');
    } else {
        statusText.innerText = "Disconnected";
        connectButton.innerText = "Connect";
        connectButton.disabled = false;
        statusDot.classList.remove('connected');
        visualizer.classList.remove('active');
    }
}